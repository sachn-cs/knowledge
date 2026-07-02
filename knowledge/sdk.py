"""Public SDK — the primary developer interface for working with OKF documents.

The SDK exposes the lifecycle of an OKF document through two main classes:
- Knowledge: the entry point for creating, loading, and verifying OKF docs
- OKFDocument: the primary object users interact with for operations
"""

from __future__ import annotations

from typing import Any

from knowledge.engine import VerificationEngine, VerificationResult
from knowledge.exceptions import (
    ParseError,
    UnsupportedSourceError,
)
from knowledge.models import KnowledgeGraph
from knowledge.okf import OKFParser, OKFSerializer
from knowledge.passes import (
    AliasResolutionPass,
    DuplicateDetectionPass,
    ExtractionPass,
    PassManager,
)
from knowledge.passes.scoring_pass import KnowledgeScore


class OKFDocument:
    """Represents an Open Knowledge Format document.

    This is the primary object users interact with. It wraps a
    KnowledgeGraph and provides lifecycle operations.
    """

    def __init__(
        self,
        graph: KnowledgeGraph,
        source: str | None = None,
        engine: VerificationEngine | None = None,
    ) -> None:
        self._graph = graph
        self._source = source
        self._engine = engine or VerificationEngine()
        self._last_verification: VerificationResult | None = None

    @property
    def graph(self) -> KnowledgeGraph:
        return self._graph

    @property
    def source(self) -> str | None:
        return self._source

    def save(self, path: str) -> None:
        """Serialize to OKF Markdown and write to a file."""
        serializer = OKFSerializer()
        content = serializer.serialize(self._graph)
        with open(path, "w") as f:
            f.write(content)

    def verify(
        self,
        threshold: float = 80.0,
        max_iterations: int = 5,
    ) -> VerificationResult:
        """Run the verification engine on this document."""
        result = self._engine.verify(
            self._graph,
            threshold=threshold,
            max_iterations=max_iterations,
        )
        self._graph = result.graph
        self._last_verification = result
        return result

    def inspect(self) -> dict[str, Any]:
        """Return a high-level overview of the document."""
        g = self._graph
        score = self._last_verification.score if self._last_verification else KnowledgeScore()
        return {
            "entity_count": len(g.entities),
            "concept_count": len(g.concepts),
            "fact_count": len(g.facts),
            "relationship_count": len(g.relationships),
            "evidence_count": len(g.evidence),
            "verification_score": score.overall,
            "source": self._source,
        }

    def score(self) -> KnowledgeScore:
        """Compute document quality scores."""
        from knowledge.passes.scoring_pass import ScoringPass

        result = ScoringPass().execute(self._graph)
        for d in result.diagnostics:
            if d.location == "scoring.quality" and d.severity.name == "INFORMATION":
                prefix = "Quality score: "
                msg = d.message[len(prefix):] if d.message.startswith(prefix) else d.message
                scores = {}
                for part in msg.split(", "):
                    if "=" in part:
                        key, val = part.split("=", 1)
                        scores[key.strip()] = float(val.replace("%", "").strip())
                return KnowledgeScore(
                    overall=scores.get("overall", 0.0),
                    completeness=scores.get("completeness", 0.0),
                    consistency=scores.get("consistency", 0.0),
                    evidence_quality=scores.get("evidence", 0.0),
                    ontology_quality=scores.get("ontology", 0.0),
                    metadata_completeness=scores.get("metadata", 0.0),
                )
        return KnowledgeScore()

    def diff(self, other: OKFDocument) -> dict[str, list[str]]:
        """Compute semantic differences with another document."""
        return self._graph.diff(other._graph)

    def merge(self, other: OKFDocument) -> OKFDocument:
        """Merge another document into this one."""
        merged = self._graph.merge(other._graph)
        return OKFDocument(graph=merged, source=self._source, engine=self._engine)

    def update(self, content: str, source: str = "unknown", fmt: str = "text") -> OKFDocument:
        """Extract knowledge from new content and merge it in."""
        mgr = PassManager()
        mgr.register(ExtractionPass())
        mgr.register(AliasResolutionPass())
        mgr.register(DuplicateDetectionPass())
        config = {"extraction.pipeline": {"content": content, "source": source, "format": fmt}}
        result = mgr.execute(self._graph, config=config)
        return OKFDocument(graph=result.graph, source=self._source, engine=self._engine)

    def delete(
        self,
        entity_id: str | None = None,
        relationship_id: str | None = None,
        fact_id: str | None = None,
        concept_id: str | None = None,
    ) -> OKFDocument:
        """Remove knowledge elements safely."""
        g = self._graph
        if entity_id:
            g = g.remove_entity(entity_id)
            # Remove related relationships
            for rel in list(g.relationships.values()):
                if rel.source_id == entity_id or rel.target_id == entity_id:
                    g = g.remove_relationship(rel.id)
        if relationship_id:
            g = g.remove_relationship(relationship_id)
        if fact_id:
            g = g.remove_fact(fact_id)
        if concept_id:
            g = g.remove_concept(concept_id)
        return OKFDocument(graph=g, source=self._source, engine=self._engine)


class Knowledge:
    """Primary entry point for the knowledge SDK.

    Responsible for creating, loading, and verifying OKF documents.
    """

    def __init__(self, engine: VerificationEngine | None = None) -> None:
        self._engine = engine or VerificationEngine()

    def create(
        self,
        input: str,
        fmt: str = "text",
        verify: bool = True,
    ) -> OKFDocument:
        """Create a new OKF document from a source string or file path."""
        content: str
        source: str

        if input.startswith("file://") or input.startswith("http://") or input.startswith("https://"):
            raise UnsupportedSourceError(f"Remote sources not yet supported: {input}")

        # Try as file path first
        try:
            with open(input) as f:
                content = f.read()
            source = input
            if input.endswith(".md") or input.endswith(".markdown"):
                fmt = "markdown"
        except (FileNotFoundError, IsADirectoryError, OSError):
            content = input
            source = "inline"

        doc = OKFDocument(graph=KnowledgeGraph(), source=source, engine=self._engine)
        doc = doc.update(content, source=source, fmt=fmt)

        if verify:
            doc.verify()

        return doc

    def read(self, path: str) -> OKFDocument:
        """Load an existing OKF Markdown document."""
        try:
            with open(path) as f:
                content = f.read()
        except FileNotFoundError:
            raise ParseError(f"File not found: {path}")

        parser = OKFParser()
        try:
            graph = parser.parse(content)
        except Exception as e:
            raise ParseError(f"Failed to parse OKF document: {e}")

        return OKFDocument(graph=graph, source=path, engine=self._engine)

    def update(self, doc: OKFDocument, input: str, fmt: str = "text") -> OKFDocument:
        """Update an existing document with new knowledge."""
        return doc.update(input, source=doc.source or "unknown", fmt=fmt)

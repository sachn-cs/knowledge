"""Deterministic extractors that produce knowledge elements from source text.

Each extractor focuses on one responsibility:
- EntityExtractor: discovers named entities
- ConceptExtractor: discovers abstract concepts
- FactExtractor: extracts factual statements
- RelationshipExtractor: identifies relationships between entities
- EvidenceExtractor: captures source evidence blocks

Extractors use deterministic algorithms (regex, heuristics) rather
than AI to maximize reproducibility.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from datetime import datetime

from knowledge.models import (
    Concept,
    Entity,
    Evidence,
    Fact,
    Provenance,
    Relationship,
    VerificationState,
)
from knowledge.models.base import Metadata


@dataclass(frozen=True)
class ExtractionResult:
    """The output of a full extraction pipeline.

    Contains all discovered knowledge elements along with metadata
    about the extraction process.
    """

    entities: list[Entity] = field(default_factory=list)
    concepts: list[Concept] = field(default_factory=list)
    facts: list[Fact] = field(default_factory=list)
    relationships: list[Relationship] = field(default_factory=list)
    evidence: list[Evidence] = field(default_factory=list)


def _make_id(prefix: str, content: str) -> str:
    """Generate a deterministic, stable identifier."""
    raw = f"{prefix}:{content.strip().lower()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def _make_provenance(source: str, extractor: str) -> Provenance:
    return Provenance(
        source_id=_make_id("src", source),
        extracted_at=datetime.now(),
        extractor=extractor,
    )


# Pattern for single capitalized words and multi-word capitalized phrases
_ENTITY_PATTERN = re.compile(r"\b([A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*)\b")

# Common non-entity words to filter out
_SKIP_WORDS: frozenset[str] = frozenset({
    "both", "this", "that", "these", "those", "here", "there", "when",
    "what", "which", "where", "who", "whom", "whose", "why", "how",
    "also", "very", "just", "then", "than", "some", "each", "every",
    "many", "much", "more", "most", "few", "less", "such", "only",
    "while", "after", "before", "during", "through", "between",
    "among", "above", "below", "under", "over", "into", "onto",
    "upon", "within", "without", "across", "beyond", "about",
    "around", "along", "beneath", "beside", "toward", "towards",
})
# Pattern for sentences (fact candidates)
_SENTENCE_PATTERN = re.compile(r"[A-Z][^.!?]*[.!?]")
# Pattern for "X is a Y" or "X is Y" constructions
_IS_A_PATTERN = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+is\s+(?:a|an|the)?\s*([A-Za-z][^,.;!?]+)"
)
# Pattern for "X Ys Z" (verb relationships)
_ACTION_PATTERN = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s+"
    r"(?:uses|depends on|extends|implements|contains|creates|"
    r"manages|requires|supports|provides|enables|integrates with)"
    r"\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)"
)


class EntityExtractor:
    """Discovers named entities from source text.

    Uses deterministic heuristics: capitalized multi-word phrases,
    repeated terms, and known naming patterns.
    """

    def extract(self, content: str, source: str = "unknown") -> list[Entity]:
        seen: set[str] = set()
        entities: list[Entity] = []

        matches = _ENTITY_PATTERN.findall(content)
        for match in matches:
            name = match.strip()
            normalized = name.lower()
            if normalized in seen or normalized in _SKIP_WORDS:
                continue
            seen.add(normalized)

            entity = Entity(
                id=_make_id("ent", name),
                name=name,
                description=None,
                confidence=0.5,
                verification_state=VerificationState.PENDING,
                provenance=_make_provenance(source, "entity_extractor"),
                metadata=Metadata(tags=["extracted"]),
            )
            entities.append(entity)

        return entities


class ConceptExtractor:
    """Discovers abstract concepts from source text.

    Concepts are identified as domain-specific terms that appear
    in descriptive or categorical contexts.
    """

    # Common concept-indicating patterns
    _CONCEPT_PATTERN = re.compile(
        r"\b([A-Z][a-zA-Z]*(?:\s+[a-zA-Z]+){0,3})\s+"
        r"(?:is|are|refers to|describes|involves|encompasses)\s+"
    )

    def extract(self, content: str, source: str = "unknown") -> list[Concept]:
        seen: set[str] = set()
        concepts: list[Concept] = []

        matches = self._CONCEPT_PATTERN.findall(content)
        for match in matches:
            name = match.strip()
            if not name:
                continue
            normalized = name.lower()
            if normalized in seen:
                continue
            seen.add(normalized)

            concept = Concept(
                id=_make_id("concept", name),
                name=name,
                description=None,
                confidence=0.4,
                verification_state=VerificationState.PENDING,
                provenance=_make_provenance(source, "concept_extractor"),
                metadata=Metadata(tags=["extracted"]),
            )
            concepts.append(concept)

        return concepts


class FactExtractor:
    """Extracts factual statements from source text.

    Facts are identified as complete sentences that make verifiable
    claims. Each fact is linked to its source evidence.
    """

    def extract(self, content: str, ev_ids: list[str], source: str = "unknown") -> list[Fact]:
        seen: set[str] = set()
        facts: list[Fact] = []
        sentence_matches = _SENTENCE_PATTERN.findall(content)

        for sentence in sentence_matches:
            statement = sentence.strip()
            if not statement:
                continue
            normalized = statement.lower()
            if normalized in seen:
                continue
            seen.add(normalized)

            fact = Fact(
                id=_make_id("fact", statement),
                statement=statement,
                evidence_refs=ev_ids[:],
                confidence=0.6,
                verification_state=VerificationState.PENDING,
                provenance=_make_provenance(source, "fact_extractor"),
                metadata=Metadata(tags=["extracted"]),
            )
            facts.append(fact)

        return facts


class RelationshipExtractor:
    """Identifies relationships between entities.

    Uses pattern matching to find relational constructions like
    "X depends on Y", "X implements Y", etc.
    """

    _RELATION_TYPES = {
        "uses": "uses",
        "depends on": "depends_on",
        "extends": "extends",
        "implements": "implements",
        "contains": "contains",
        "creates": "creates",
        "manages": "manages",
        "requires": "requires",
        "supports": "supports",
        "provides": "provides",
        "enables": "enables",
        "integrates with": "integrates_with",
    }

    def extract(
        self,
        content: str,
        entity_names: set[str],
        source: str = "unknown",
    ) -> list[Relationship]:
        relationships: list[Relationship] = []
        seen: set[str] = set()

        for verb, rel_type in self._RELATION_TYPES.items():
            sorted_names = sorted(entity_names, key=len, reverse=True)
            name_pattern = "|".join(re.escape(e) for e in sorted_names)
            pattern = re.compile(
                rf"\b({name_pattern})\s+{re.escape(verb)}\s+({name_pattern})"
            )
            matches = pattern.findall(content)
            for src_name, tgt_name in matches:
                key = f"{src_name}:{rel_type}:{tgt_name}"
                if key in seen:
                    continue
                seen.add(key)

                rel = Relationship(
                    id=_make_id("rel", key),
                    source_id=_make_id("ent", src_name),
                    target_id=_make_id("ent", tgt_name),
                    relationship_type=rel_type,
                    evidence_refs=[],
                    confidence=0.5,
                    verification_state=VerificationState.PENDING,
                    provenance=_make_provenance(source, "relationship_extractor"),
                    metadata=Metadata(tags=["extracted"]),
                )
                relationships.append(rel)

        return relationships


class EvidenceExtractor:
    """Captures source evidence from content.

    Evidence blocks are the raw text segments that support knowledge
    claims. They are immutable references that knowledge elements
    point to.
    """

    _PARAGRAPH_PATTERN = re.compile(r"(?:^|\n\n)([^\n][\s\S]*?)(?=\n\n|$)")

    def extract(self, content: str, source: str = "unknown") -> list[Evidence]:
        seen: set[str] = set()
        evidence_list: list[Evidence] = []

        paragraphs = self._PARAGRAPH_PATTERN.findall(content)
        for para in paragraphs:
            text = para.strip()
            if len(text) < 20:
                continue
            normalized = text.lower()
            if normalized in seen:
                continue
            seen.add(normalized)

            ev = Evidence(
                id=_make_id("ev", text),
                content=text,
                source=source,
                confidence=1.0,
                verification_state=VerificationState.PENDING,
                provenance=_make_provenance(source, "evidence_extractor"),
                metadata=Metadata(tags=["extracted"]),
            )
            evidence_list.append(ev)

        return evidence_list


class ExtractionPipeline:
    """Orchestrates the full extraction process.

    Runs all extractors in sequence and returns a combined
    ExtractionResult with cross-linked evidence references.
    """

    def __init__(self) -> None:
        self.entity_extractor = EntityExtractor()
        self.concept_extractor = ConceptExtractor()
        self.fact_extractor = FactExtractor()
        self.relationship_extractor = RelationshipExtractor()
        self.evidence_extractor = EvidenceExtractor()

    def extract(self, content: str, source: str = "unknown") -> ExtractionResult:
        evidence = self.evidence_extractor.extract(content, source)
        ev_ids = [e.id for e in evidence]

        entities = self.entity_extractor.extract(content, source)
        concepts = self.concept_extractor.extract(content, source)
        facts = self.fact_extractor.extract(content, ev_ids, source)
        entity_names = {e.name for e in entities}
        relationships = self.relationship_extractor.extract(content, entity_names, source)

        return ExtractionResult(
            entities=entities,
            concepts=concepts,
            facts=facts,
            relationships=relationships,
            evidence=evidence,
        )

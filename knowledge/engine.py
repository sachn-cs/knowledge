"""Verification Engine — the core component that protects knowledge integrity.

Every mutation passes through the engine before completion. It iteratively
validates, diagnoses, repairs, scores, and revalidates until convergence.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from pydantic import BaseModel, Field

from knowledge.models import KnowledgeGraph
from knowledge.passes import (
    Diagnostic,
    PassManager,
    Phase,
)
from knowledge.passes.base import KnowledgeScore
from knowledge.passes.scoring import ScoringPass


class VerificationResult(BaseModel, frozen=True):
    """The result of a verification cycle.

    Contains the final verified graph, quality scores, diagnostics,
    repairs applied, and metadata about the verification process.
    """

    graph: KnowledgeGraph
    score: KnowledgeScore = Field(default_factory=KnowledgeScore)
    diagnostics: list[Diagnostic] = Field(default_factory=list)
    repairs_applied: int = 0
    iteration_count: int = 1
    converged: bool = True
    threshold_met: bool = False


@dataclass
class VerificationEngine:
    """The verification engine that protects knowledge integrity.

    Owns the repair loop: validate → diagnose → repair → rescore → repeat.
    No component outside this engine may modify knowledge in response
    to validation failures.
    """

    pass_manager: PassManager = field(default_factory=PassManager)
    quality_threshold: float = 80.0
    max_iterations: int = 5
    repair_phases: list[Phase] = field(default_factory=lambda: [Phase.REPAIR])
    verification_phases: list[Phase] = field(
        default_factory=lambda: [
            Phase.ANALYSIS,
            Phase.VERIFICATION,
            Phase.SCORING,
        ]
    )

    def setup_default_passes(self) -> None:
        """Register the default set of compiler passes.

        Registers schema validation, structural validation, consistency
        validation, scoring, and repair passes. Silently skips any
        pass that is already registered.
        """
        from knowledge.passes.analysis import GraphStatisticsPass
        from knowledge.passes.consistency import ConsistencyValidationPass
        from knowledge.passes.repair import (
            AttachProvenancePass,
            FixEvidenceRefsPass,
            MergeDuplicateEntitiesPass,
            NormalizeConfidencePass,
        )
        from knowledge.passes.schema import SchemaValidationPass
        from knowledge.passes.structural import StructuralValidationPass
        from knowledge.passes.verification import (
            EvidenceValidationPass,
            OntologyValidationPass,
            SemanticValidationPass,
        )

        for pass_ in [
            GraphStatisticsPass(),
            SchemaValidationPass(),
            StructuralValidationPass(),
            ConsistencyValidationPass(),
            SemanticValidationPass(),
            EvidenceValidationPass(),
            OntologyValidationPass(),
            ScoringPass(),
            MergeDuplicateEntitiesPass(),
            AttachProvenancePass(),
            FixEvidenceRefsPass(),
            NormalizeConfidencePass(),
        ]:
            try:
                self.pass_manager.register(pass_)
            except ValueError:
                pass

    def verify(
        self,
        graph: KnowledgeGraph,
        config: dict[str, Any] | None = None,
        threshold: float | None = None,
        max_iterations: int | None = None,
    ) -> VerificationResult:
        """Run the full verification lifecycle.

        Iteratively validates, diagnoses, repairs, and rescored the
        knowledge graph until convergence or max iterations.

        Args:
            graph: The knowledge graph to verify.
            config: Optional pass-specific configuration.
            threshold: Quality threshold (0-100). Defaults to
                ``self.quality_threshold``.
            max_iterations: Maximum verification iterations.
                Defaults to ``self.max_iterations``.

        Returns:
            A VerificationResult with the final graph, diagnostics,
            scores, and convergence metadata.
        """
        if not self.pass_manager.registered_ids:
            self.setup_default_passes()

        threshold = threshold if threshold is not None else self.quality_threshold
        max_iterations = max_iterations if max_iterations is not None else self.max_iterations
        current_graph = graph
        all_diagnostics: list[Diagnostic] = []
        total_repairs = 0

        for iteration in range(1, max_iterations + 1):
            # Verify
            v_result = self.pass_manager.execute(
                current_graph, config=config, phases=self.verification_phases
            )
            all_diagnostics.extend(v_result.diagnostics)

            score = v_result.score or KnowledgeScore()
            if score.overall >= threshold:
                return VerificationResult(
                    graph=v_result.graph,
                    score=score,
                    diagnostics=all_diagnostics,
                    repairs_applied=total_repairs,
                    iteration_count=iteration,
                    converged=True,
                    threshold_met=True,
                )

            # Repair
            r_result = self.pass_manager.execute(
                v_result.graph, config=config, phases=self.repair_phases
            )
            total_repairs += r_result.total_repairs
            all_diagnostics.extend(r_result.diagnostics)

            if r_result.graph == current_graph:
                final_score = self.compute_final_score(r_result.graph)
                return VerificationResult(
                    graph=r_result.graph,
                    score=final_score,
                    diagnostics=all_diagnostics,
                    repairs_applied=total_repairs,
                    iteration_count=iteration,
                    converged=True,
                    threshold_met=final_score.overall >= threshold,
                )

            current_graph = r_result.graph

        # Max iterations reached
        final_score = self.compute_final_score(current_graph)
        return VerificationResult(
            graph=current_graph,
            score=final_score,
            diagnostics=all_diagnostics,
            repairs_applied=total_repairs,
            iteration_count=max_iterations,
            converged=False,
            threshold_met=final_score.overall >= threshold,
        )

    @staticmethod
    def compute_final_score(graph: KnowledgeGraph) -> KnowledgeScore:
        """Compute the final quality score for a graph.

        Runs a standalone ScoringPass to produce an independent
        quality assessment after the verification loop ends.

        Args:
            graph: The knowledge graph to score.

        Returns:
            A KnowledgeScore with quality metrics.
        """
        result = ScoringPass().execute(graph)
        return result.score or KnowledgeScore()

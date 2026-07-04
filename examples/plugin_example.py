"""Example plugin — a custom scoring pass.

This demonstrates how to write a compiler pass that can be registered
with the PassManager and used in the verification pipeline.
"""

from typing import Any

from knowledge.models import KnowledgeGraph
from knowledge.passes import CompilerPass, PassResult, Phase


class CoverageScoringPass(CompilerPass):
    """Scores entity description coverage."""

    id = "scoring.coverage"
    phase = Phase.SCORING
    version = "0.1.0"
    description = "Score entity description coverage"

    def execute(
        self,
        graph: KnowledgeGraph,
        config: dict[str, Any] | None = None,
    ) -> PassResult:
        total = len(graph.entities) or 1
        covered = sum(1 for e in graph.entities.values() if e.description)
        score_value = (covered / total) * 100.0

        from knowledge.passes import Diagnostic, KnowledgeScore, Severity

        score = KnowledgeScore(overall=round(score_value, 1))
        diag = Diagnostic(
            severity=Severity.INFORMATION,
            message=f"Coverage score: {score_value:.1f}%",
            location="scoring.coverage",
        )
        return PassResult(graph=graph, diagnostics=[diag], score=score)

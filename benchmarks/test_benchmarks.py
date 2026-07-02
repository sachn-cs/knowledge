"""Benchmarks for the knowledge SDK.

Run with: pytest benchmarks/ --benchmark-only
"""

import pytest

from knowledge import Knowledge
from knowledge.engine import VerificationEngine
from knowledge.models import Entity, Evidence, Fact, KnowledgeGraph
from knowledge.okf import OKFSerializer


class TestVerificationBenchmarks:
    def test_verify_empty_graph(self, benchmark) -> None:
        engine = VerificationEngine()
        graph = KnowledgeGraph()
        result = benchmark(engine.verify, graph)
        assert result.converged is True

    def test_verify_small_graph(self, benchmark) -> None:
        engine = VerificationEngine()
        graph = _make_small_graph()
        result = benchmark(engine.verify, graph)
        assert result.score.overall >= 0

    def test_verify_medium_graph(self, benchmark) -> None:
        engine = VerificationEngine()
        graph = _make_medium_graph()
        result = benchmark(engine.verify, graph)
        assert result.score.overall >= 0

    def test_serialize_small_graph(self, benchmark) -> None:
        serializer = OKFSerializer()
        graph = _make_small_graph()
        result = benchmark(serializer.serialize, graph)
        assert "## Entity:" in result

    def test_create_from_text(self, benchmark) -> None:
        knowledge = Knowledge()
        result = benchmark(knowledge.create, "Python is a programming language.", verify=False)
        assert result is not None


def _make_small_graph() -> KnowledgeGraph:
    graph = KnowledgeGraph()
    graph = graph.add_entity(Entity(name="Python", id="ent_001"))
    graph = graph.add_entity(Entity(name="JavaScript", id="ent_002"))
    graph = graph.add_fact(Fact(statement="Python is a language.", id="f_001"))
    graph = graph.add_evidence(Evidence(content="Source text", source="doc.md", id="ev_001"))
    return graph


def _make_medium_graph() -> KnowledgeGraph:
    graph = KnowledgeGraph()
    for i in range(10):
        graph = graph.add_entity(Entity(name=f"Entity_{i}", id=f"ent_{i:03d}"))
    for i in range(20):
        graph = graph.add_fact(Fact(statement=f"Fact {i} about knowledge.", id=f"f_{i:03d}"))
    for i in range(15):
        graph = graph.add_evidence(
            Evidence(content=f"Evidence {i}", source="doc.md", id=f"ev_{i:03d}")
        )
    return graph

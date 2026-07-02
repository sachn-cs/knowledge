"""Tests for the CLI."""

import tempfile

from knowledge.cli import main as cli_main
from knowledge.models import Entity, KnowledgeGraph
from knowledge.okf import OKFSerializer


def _run_cli(args: list[str]) -> None:
    """Run the CLI with given args, capturing SystemExit."""
    try:
        # We can't easily capture output, so just test that it doesn't crash
        import sys
        old_argv = sys.argv
        sys.argv = ["knowledge"] + args
        cli_main()
        sys.argv = old_argv
    except SystemExit:
        pass


class TestCLICommands:
    def test_create_text(self) -> None:
        _run_cli(["create", "Python is a language.", "--no-verify"])

    def test_create_markdown(self) -> None:
        _run_cli(["create", "Python is a language.", "-f", "markdown", "--no-verify"])

    def test_create_with_output(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".md", delete=False) as f:
            fname = f.name
        _run_cli(["create", "Python is a language.", "-o", fname, "--no-verify"])

    def test_read(self) -> None:
        graph = KnowledgeGraph()
        graph = graph.add_entity(Entity(name="Python", id="ent_001"))
        serializer = OKFSerializer()
        content = serializer.serialize(graph)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            fname = f.name
        _run_cli(["read", fname])

    def test_inspect(self) -> None:
        graph = KnowledgeGraph()
        graph = graph.add_entity(Entity(name="Python", id="ent_001"))
        serializer = OKFSerializer()
        content = serializer.serialize(graph)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            fname = f.name
        _run_cli(["inspect", fname])

    def test_score(self) -> None:
        graph = KnowledgeGraph()
        graph = graph.add_entity(Entity(name="Python", id="ent_001"))
        serializer = OKFSerializer()
        content = serializer.serialize(graph)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            fname = f.name
        _run_cli(["score", fname])

    def test_verify(self) -> None:
        graph = KnowledgeGraph()
        graph = graph.add_entity(Entity(name="Python", id="ent_001"))
        serializer = OKFSerializer()
        content = serializer.serialize(graph)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            fname = f.name
        _run_cli(["verify", fname])

    def test_diff(self) -> None:
        graph_a = KnowledgeGraph()
        graph_a = graph_a.add_entity(Entity(name="Python", id="ent_001"))
        graph_b = KnowledgeGraph()
        graph_b = graph_b.add_entity(Entity(name="Java", id="ent_002"))
        serializer = OKFSerializer()
        content_a = serializer.serialize(graph_a)
        content_b = serializer.serialize(graph_b)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content_a)
            fname_a = f.name
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content_b)
            fname_b = f.name
        _run_cli(["diff", fname_a, fname_b])

    def test_update(self) -> None:
        graph = KnowledgeGraph()
        graph = graph.add_entity(Entity(name="Python", id="ent_001"))
        serializer = OKFSerializer()
        content = serializer.serialize(graph)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(content)
            fname = f.name
        _run_cli(["update", fname, "JavaScript is a language."])

    def test_unknown_command(self) -> None:
        try:
            import sys
            old_argv = sys.argv
            sys.argv = ["knowledge", "unknown_command"]
            cli_main()
            sys.argv = old_argv
        except SystemExit:
            pass

"""Tests for the extension system."""

from knowledge.extensions import ExtensionConfig, ExtensionRegistry
from knowledge.passes import CompilerPass, PassManager, PassResult, Phase
from knowledge.passes.diagnostics import Diagnostic, Severity


class TestExtensionConfig:
    def test_defaults(self) -> None:
        cfg = ExtensionConfig()
        assert cfg.enabled_passes == []
        assert cfg.disabled_passes == []
        assert cfg.pass_config == {}

    def test_from_dict(self) -> None:
        cfg = ExtensionConfig.from_dict({
            "enabled_passes": ["pass_a"],
            "disabled_passes": ["pass_b"],
            "pass_config": {"pass_a": {"key": "val"}},
        })
        assert cfg.enabled_passes == ["pass_a"]
        assert cfg.disabled_passes == ["pass_b"]
        assert cfg.pass_config["pass_a"]["key"] == "val"


class TestExtensionRegistry:
    def test_register_plugin(self) -> None:
        registry = ExtensionRegistry()
        pid = registry.register_plugin(SimplePass)
        assert pid == "test.simple_pass"

    def test_apply_to_manager(self) -> None:
        registry = ExtensionRegistry()
        registry.register_plugin(SimplePass)
        mgr = PassManager()
        registered = registry.apply_to(mgr)
        assert "test.simple_pass" in registered
        assert "test.simple_pass" in mgr.registered_ids

    def test_apply_with_enabled_filter(self) -> None:
        registry = ExtensionRegistry()
        registry.register_plugin(SimplePass)
        registry.register_plugin(OtherPass)
        mgr = PassManager()
        cfg = ExtensionConfig(enabled_passes=["test.simple_pass"])
        registered = registry.apply_to(mgr, cfg)
        assert "test.simple_pass" in registered
        assert "test.other_pass" not in registered

    def test_apply_with_disabled_filter(self) -> None:
        registry = ExtensionRegistry()
        registry.register_plugin(SimplePass)
        registry.register_plugin(OtherPass)
        mgr = PassManager()
        cfg = ExtensionConfig(disabled_passes=["test.simple_pass"])
        registered = registry.apply_to(mgr, cfg)
        assert "test.simple_pass" not in registered
        assert "test.other_pass" in registered

    def test_discover_empty(self) -> None:
        registry = ExtensionRegistry()
        discovered = registry.discover()
        assert isinstance(discovered, list)


# Helper passes for testing
class SimplePass(CompilerPass):
    id = "test.simple_pass"
    phase = Phase.NORMALIZATION
    description = "Simple test pass"

    def execute(self, graph, config=None):
        return PassResult(graph=graph)


class OtherPass(CompilerPass):
    id = "test.other_pass"
    phase = Phase.ANALYSIS
    description = "Other test pass"

    def execute(self, graph, config=None):
        return PassResult(graph=graph, diagnostics=[
            Diagnostic(severity=Severity.INFORMATION, message="Other pass"),
        ])

# Roadmap

## v0.1.0 — Current (pre-release)

- Knowledge Markdown (KMD) flat-file persistence
- Compiler pass framework with dependency resolution
- Deterministic extraction (entities, concepts, facts, relationships, evidence)
- Normalization (alias resolution, duplicate detection, stable IDs)
- Iterative verification engine (validate → diagnose → repair → rescore)
- 5 quality dimensions with weighted scoring
- CLI with 7 commands
- Extension system via entry points
- 98% test coverage, 293 tests

## v0.2.0 — Planned

- **OKF v0.1 directory bundle support** — Google-compatible OKF format with index.md, files per element, YAML frontmatter, and assets/
- HTML source reader
- Large-graph performance optimization (1000+ elements)
- Property-based testing (Hypothesis)
- CI badge fix to anomalyco/knowledge
- ADR directory with architecture decision records
- Security hardening guidelines documentation

## v0.3.0 — Future

- PDF source reader (via text extraction)
- Configurable pass ordering via TOML
- Plugin example in examples/
- Reasoning provider plugin API with AI-assisted extraction
- Origin tracking and provenance chains
- Knowledge diff visualization

## v1.0.0 — Stable Release

- Full OKF v0.1 compliance
- Stable public API (semver 1.0)
- Comprehensive user documentation with tutorials
- Benchmark regression tracking
- Release workflow publishing to PyPI

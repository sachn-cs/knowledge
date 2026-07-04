# knowledge

[![Python 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)]()
[![CI](https://github.com/anomalyco/knowledge/actions/workflows/ci.yml/badge.svg)](https://github.com/anomalyco/knowledge/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)]()
[![Status](https://img.shields.io/badge/status-pre--release-orange)]()

**A Python SDK for knowledge engineering — create, verify, and evolve structured knowledge with automated quality assurance.**

`knowledge` treats a knowledge document as a **living artifact**: structured, versioned, verified, and continuously improvable. Every mutation passes through a verification engine that validates, diagnoses, repairs, and rescores until a quality threshold is met.

---

## Quick Start

```python
from knowledge import Knowledge

knowledge = Knowledge()
doc = knowledge.create("Python is a programming language.")
doc.save("knowledge.md")
```

```bash
# Same thing from the CLI
knowledge create "Python is a programming language." -o knowledge.md
knowledge score knowledge.md
```

---

## Why `knowledge`?

Traditional document tools are **dumb files** — they store text but understand nothing about its structure or quality. `knowledge` is different:

- **Structured by default** — Extracts entities, concepts, facts, relationships, and evidence from plain text or Markdown.
- **Verified on every mutation** — A compiler-pass pipeline validates quality, diagnoses issues, repairs problems, and rescores until your threshold is met.
- **Deterministic** — Same input always produces the same output. No hidden state, no randomness in the pipeline.
- **Extensible** — Write custom compiler passes and plug them in via entry points.

---

## Features

- **Knowledge Markdown (KMD)** — Human-readable, diff-friendly persistence format
- **Compiler pass architecture** — Validation, normalization, deduplication, repair, and scoring
- **5 quality dimensions** — Completeness, consistency, evidence quality, ontology quality, metadata completeness
- **Iterative verification** — The engine loops: validate → diagnose → repair → rescore → repeat until converged
- **Dependency-aware passes** — Passes declare what they need; the engine resolves the DAG
- **CLI + Python SDK** — Use from the terminal or embed in your application
- **Plugin system** — Register custom passes via Python entry points
- **98% test coverage** — 288 tests, clean mypy, clean ruff

---

## Installation

```bash
# From source (PyPI release coming in v0.1.0)
pip install git+https://github.com/sachn-cs/knowledge.git
```

```bash
# With dev dependencies
pip install -e ".[dev]"
```

---

## Usage

### Python API

```python
from knowledge import Knowledge, OKFDocument

# Create knowledge from text
knowledge = Knowledge()
doc = knowledge.create("Python is a programming language. "
                        "It was created by Guido van Rossum.")

# Inspect what was extracted
info = doc.inspect()
print(f"Entities: {info['entity_count']}, Facts: {info['fact_count']}")

# Score quality
score = doc.score()
print(f"Quality score: {score.overall:.1f}%")

# Verify and repair automatically
result = doc.verify(threshold=80.0)
print(f"Converged: {result.converged}, Repairs: {result.repairs_applied}")

# Persist
doc.save("knowledge.md")

# Load it back
doc2 = knowledge.read("knowledge.md")

# Compare two documents
diff = doc.diff(doc2)

# Merge knowledge from multiple sources
doc3 = knowledge.create("JavaScript is for web development.")
merged = doc.merge(doc3)
```

### CLI

```
$ knowledge create "Python is a language." -o python.md
Created and saved to python.md

$ knowledge score python.md
Overall:           72.5%
Completeness:      75.0%
Consistency:       90.0%
Evidence Quality:  50.0%
Ontology Quality:  80.0%
Metadata:          60.0%

$ knowledge verify python.md
Score: 85.3%
Converged: True
Threshold met: True
Iterations: 2
Repairs applied: 1
  [INFO] Attached provenance to 3 elements

$ knowledge diff before.md after.md
  Entities Added: ent_002
  Facts Added: f_002

$ knowledge read python.md
Entities: 1
Concepts: 0
Facts: 1
Relationships: 0
Evidence: 1
```

---

## How It Works

```
Knowledge Sources (text, markdown, files)
        |
        v
+----------------------+
| Extraction           |  Entities, concepts, facts, relationships, evidence
+----------------------+
        |
        v
+----------------------+
| Knowledge Model      |  Canonical, validated data model (Pydantic)
+----------------------+
        |
        v
+----------------------+
| Verification Engine  |  Iterative: validate -> diagnose -> repair -> rescore
+----------------------+
        |
        v
+----------------------+
| Serialization        |  KMD (flat Markdown), OKF v0.1 (planned)
+----------------------+
        |
        v
    Verified Knowledge Document
```

Every mutation passes through verification. The engine runs a DAG of compiler passes, each with a specific responsibility:

| Phase | Passes |
|-------|--------|
| Schema | Type checks, required fields, structural integrity |
| Analysis | Alias resolution, duplicate detection |
| Consistency | Semantic consistency, relation target validity |
| Scoring | Completeness, consistency, evidence, ontology, metadata |
| Repair | Confidence normalization, provenance attachment, entity merging |

---

## Documentation

| Resource | Description |
|----------|-------------|
| [User Guide](docs/user_guide.md) | Step-by-step walkthrough |
| [API Reference](docs/api.md) | Full public API documentation |
| [Architecture](docs/architecture.md) | System design and layer descriptions |
| [Plugin Guide](docs/plugin_guide.md) | Writing and registering custom passes |
| [ADR Log](docs/adr/) | Architecture decision records |
| [SPEC.md](SPEC.md) | Complete specification |
| [ROADMAP.md](ROADMAP.md) | Version roadmap and planned features |

---

## Project Status

**v0.1.0 (pre-release)** — Core functionality complete. Not yet on PyPI.

| Milestone | Status |
|-----------|--------|
| Core Domain Model | ✅ |
| KMD Persistence | ✅ |
| Compiler Framework | ✅ |
| Extraction (text + markdown) | ✅ |
| Verification Engine | ✅ |
| Repair Engine | ✅ |
| CLI | ✅ |
| Plugin System | ✅ |
| Documentation | ✅ |
| Large-Graph Benchmarks | ✅ |
| OKF v0.1 Bundle Support | 🔜 v0.2.0 |
| PyPI Release | 🔜 v0.1.0 |

---

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check knowledge/ tests/
mypy knowledge/
```

```bash
# Benchmarks
pytest benchmarks/ --benchmark-only
```

---

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) to get started.

Report security vulnerabilities to **sachncs@gmail.com** — do not open a public issue.

---

## License

MIT

---

*Built with [Pydantic](https://docs.pydantic.dev/), [Typer](https://typer.tiangolo.com/) (CLI), and a lot of compiler-pass inspiration.*

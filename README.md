# knowledge

[![Python 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)]()
[![CI](https://github.com/sachn-cs/knowledge/actions/workflows/ci.yml/badge.svg)](https://github.com/sachn-cs/knowledge/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)]()
[![Status](https://img.shields.io/badge/status-pre--release-orange)]()

**A Python package for knowledge engineering.**

`knowledge` is an open-source Python SDK for creating, maintaining, verifying, and
evolving **Open Knowledge Format (OKF)** documents.

Unlike traditional document generation tools, `knowledge` treats an OKF document
as a **living artifact** — structured, versioned, verified, and
continuously improvable.

Every mutation passes through a verification engine that validates, diagnoses,
repairs, and rescores until a quality threshold is met.

---

## Status

**v0.1.0 (pre-release)** — All 14 milestones complete. Not yet available on PyPI.

| Milestone | Status |
|---|---|
| Project Foundation | ✅ Complete |
| Core Domain Model | ✅ Complete |
| OKF Support | ✅ Complete |
| Compiler Framework | ✅ Complete |
| Knowledge Extraction | ✅ Complete |
| Normalization | ✅ Complete |
| Verification Engine | ✅ Complete |
| Semantic Verification | ✅ Complete |
| Repair Engine | ✅ Complete |
| Public SDK | ✅ Complete |
| CLI | ✅ Complete |
| Extension System | ✅ Complete |
| Documentation | ✅ Complete |
| Release Preparation | ✅ Complete |

---

## Quick Start

```python
from knowledge import Knowledge

# Create knowledge from text
knowledge = Knowledge()
okf = knowledge.create("Python is a programming language.")
okf.verify()
okf.save("knowledge.md")
```

## CLI

```bash
# Create from text
knowledge create "Python is a language." -o knowledge.md

# Verify
knowledge verify knowledge.md

# Score
knowledge score knowledge.md

# Diff
knowledge diff before.md after.md
```

## Installation

```bash
# Not yet on PyPI — install from source:
pip install git+https://github.com/sachn-cs/knowledge.git
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check knowledge/ tests/
mypy knowledge/
```

## Documentation

- [User Guide](docs/user_guide.md) — Step-by-step usage
- [Architecture](docs/architecture.md) — System design and layer overview
- [API Reference](docs/api.md) — Public API documentation
- [Plugin Guide](docs/plugin_guide.md) — Extending the SDK
- [SPEC.md](SPEC.md) — Full specification and roadmap

## Examples

See [examples/basic_usage.py](examples/basic_usage.py) for a complete walkthrough.

## License

MIT

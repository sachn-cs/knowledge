# knowledge SDK

**A Python package for knowledge engineering.**

`knowledge` is an open-source Python SDK for creating, maintaining, verifying, and
evolving **Open Knowledge Format (OKF)** documents.

Unlike traditional document generation tools, `knowledge` treats an OKF document
as a **living artifact** — structured, versioned, verified, and
continuously improvable.

## Installation

```bash
# Not yet on PyPI — install from source:
pip install git+https://github.com/sachn-cs/knowledge.git
```

## Quick Start

```python
from knowledge import Knowledge

# Create knowledge from text
knowledge = Knowledge()
okf = knowledge.create("Python is a programming language.")
okf.verify()
okf.save("knowledge.md")
```

## Key Concepts

- **Open Knowledge Format (OKF)** — The canonical persistence format for knowledge.
- **Knowledge Graph** — The internal representation used by the SDK. Immutable operations produce new instances.
- **Verification Engine** — The iterative quality gate for all knowledge mutations. Validates, diagnoses, repairs, and rescores.
- **Compiler Passes** — Independent, composable transformation and validation steps with explicit dependencies.

## Status — v0.1.0 (pre-release)

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

## CLI

```bash
# Create knowledge from text
knowledge create "Python is a programming language." --no-verify

# Read and verify an OKF document
knowledge verify path/to/knowledge.md

# Compute quality scores
knowledge score path/to/knowledge.md

# Compare two OKF documents
knowledge diff before.md after.md
```

## Next Steps

- [Architecture](architecture.md) — System design and layer overview
- [API Reference](api.md) — Full public API documentation
- [User Guide](user_guide.md) — Step-by-step usage guide
- [Plugin Guide](plugin_guide.md) — Extending the SDK

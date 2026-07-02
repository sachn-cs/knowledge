# knowledge SDK

**Knowledge is software.**

`knowledge` is an open-source Python SDK for creating, maintaining, verifying, and
evolving **Open Knowledge Format (OKF)** documents.

## Installation

```bash
pip install knowledge-sdk
```

## Quick Start

```python
from knowledge import Knowledge

knowledge = Knowledge()

okf = knowledge.create("sources/my-document.md")
okf.verify()
okf.save("knowledge.md")
```

## Key Concepts

- **Open Knowledge Format (OKF)** — The canonical persistence format for knowledge.
- **Knowledge Graph** — The internal representation used by the SDK.
- **Verification Engine** — The iterative quality gate for all knowledge mutations.
- **Compiler Passes** — Independent, composable transformation and validation steps.

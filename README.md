# knowledge

**Knowledge is software.**

`knowledge` is an open-source Python SDK for creating, maintaining, verifying, and
evolving **Open Knowledge Format (OKF)** documents.

## Status

Early development. Not ready for production use.

## Quick Start

```python
from knowledge import Knowledge

knowledge = Knowledge()

okf = knowledge.create("sources/my-document.md")
okf.verify()
okf.save("knowledge.md")
```

## Installation

```bash
pip install knowledge-sdk
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check src/
mypy src/
```

## License

MIT

# knowledge

[![Python 3.12+](https://img.shields.io/badge/python-3.12%20%7C%203.13-blue)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green)]()

**Create OKF bundles from HTML sources.**

`knowledge` downloads a URL or reads a file, parses HTML into sections by headings, and writes each section as a Markdown concept file in an [OKF v0.1](docs/adr/0002-bundle-format-v0-1.md) directory bundle.

---

## Quick Start

```bash
knowledge create https://google.github.io/styleguide/pyguide.html style-guide/
```

Output: `style-guide/index.md` + one `.md` per section.

## Installation

```bash
pip install git+https://github.com/anomalyco/knowledge.git
pip install -e ".[dev]"   # with dev dependencies
```

## CLI

```bash
knowledge create <url-or-file> <output-dir>
```

## Python API

```python
from knowledge import Knowledge

Knowledge().create_bundle(
    "https://google.github.io/styleguide/pyguide.html",
    "style-guide/",
)
```

## Development

```bash
pip install -e ".[dev]"
pytest
ruff check knowledge/ tests/
mypy knowledge/ tests/
```

## License

MIT

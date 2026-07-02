# API Reference

The public API is under active development.

## Knowledge

```python
from knowledge import Knowledge

knowledge = Knowledge()
```

### `create(input)`

Creates a new OKF document from one or more knowledge sources.

### `read(path)`

Loads an existing OKF Markdown document.

### `update(okf, input)`

Updates an existing OKF document with additional knowledge.

## OKFDocument

The primary object returned by the SDK.

### `verify(threshold=95)`

Runs the verification engine.

### `save(path)`

Writes an OKF document.

### `inspect()`

Returns a high-level overview of the document.

### `score()`

Computes document quality.

### `diff(previous)`

Computes semantic differences.

### `merge(other)`

Combines two verified OKF documents.

### `delete(entity)`, `delete(relationship=id)`

Removes knowledge safely.

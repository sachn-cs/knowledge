# Architecture

## Overview

The **knowledge** SDK follows a three-layer architecture:

```
┌──────────────────────────────────────────┐
│              CLI (knowledge/)            │
│       argparse-based subcommands         │
├──────────────────────────────────────────┤
│            SDK Layer (sdk.py)             │
│     Knowledge class — public API         │
│     read_source(), fetch_url()           │
├────────────────┬─────────────────────────┤
│  LLM Layer     │  Serialization Layer     │
│  (llm/)        │  (kmd/)                 │
│                │                          │
│  LLMExtractor  │  BundleSerializer       │
│  Knowledge-    │  yaml_escape()           │
│  BundleManager │  validate()             │
├────────────────┴─────────────────────────┤
│          Domain Models (models.py)        │
│       Concept, KnowledgeGraph (Pydantic)  │
└──────────────────────────────────────────┘
```

## Data Flow

### Create Bundle

```
Source URL/file
    │
    ▼
read_source() / fetch_url()
    │  (downloads or reads)
    ▼
Raw HTML/Markdown text
    │
    ▼
LLMExtractor.extract()
    │  (split headings → LLM per section → validate JSON)
    ▼
KnowledgeGraph (in-memory)
    │
    ▼
BundleSerializer.serialize()
    │  (write YAML frontmatter + Markdown body)
    ▼
OKF v0.1 directory bundle
```

### Update Bundle

Same flow, but the output directory is the *existing* bundle path (it is
overwritten completely — this is not an incremental merge).

### Remove Concepts

```
Bundle directory
    │
    ▼
KnowledgeBundleManager.read_bundle()
    │  (parse .md files → KnowledgeGraph)
    ▼
KnowledgeGraph.remove_concept(id)
    │  (returns new graph without the ID)
    ▼
BundleSerializer.serialize()
    │  (write back to same directory)
    ▼
Updated bundle
```

## Key Design Decisions

### Immutable Models

`Concept` and `KnowledgeGraph` are frozen Pydantic models. Every mutation
returns a new instance. This makes the models safe to share across threads
and simple to reason about in pipelines.

### Section-Based Extraction

Rather than sending the entire document in a single LLM call, we split
by headings first. This:

- Keeps each prompt within common context windows.
- Avoids truncation of long documents.
- Produces naturally bounded concepts (one per heading).

### litellm as Single LLM Interface

We use [litellm](https://litellm.ai) exclusively — no separate provider
abstractions. The model string (e.g. `"gpt-4o"`, `"claude-3-opus-20240229"`,
`"ollama/llama3"`) determines the provider, API endpoint, and authentication.

### No YAML Parser Dependency

Frontmatter is written and parsed using simple line-based conventions
rather than a full YAML parser. This avoids adding PyYAML as a dependency
for a very limited schema (key-value pairs only). The `yaml_escape` /
`yaml_unescape` pair handles control characters for round-trip fidelity.

## Error Handling

All SDK exceptions inherit from `KnowledgeError`:

- `FetchError` — source cannot be fetched or read.
- `ValidationError` — bundle structural validation fails.

The CLI catches all exceptions at the `main()` boundary, logs the error
message, and exits with code 1.

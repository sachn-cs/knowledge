# ADR-002: Implement OKF v0.1 bundle format in v0.1.0

**Status:** Accepted

**Date:** 2026-07-04

**Drivers:** @anomalyco

**Supersedes:** ADR-001

## Context

ADR-001 deferred the OKF v0.1 directory-bundle format to v0.2.0. Two factors
motivate revisiting this decision:

1. **Real-world demand:** The Google Python Style Guide bundle at
   `examples/google-python-style-guide/` demonstrated that OKF bundles are
   the primary output users want from `knowledge create`. A flat KMD file is
   not suitable for documentation consumption.

2. **Section-aware extraction:** Processing HTML sources by section headings
   produces higher-quality concepts than tag-stripped flat text. The bundle
   format naturally maps to this section-per-concept structure.

Since the internal `KnowledgeGraph` model is format-agnostic, adding bundle
support requires only a new serializer (not model changes). The section-aware
HTML reader is an orthogonal improvement to the source-reader layer.

## Options Considered

### Option A: Implement bundle + section-aware extraction now

- **Pro:** Satisfies real user workflow (`knowledge create <url> -o <dir>`).
- **Pro:** Bundle serializer reuses existing `Concept` model — no data loss.
- **Pro:** Section-aware HTML reader is a new source reader (like
  `MarkdownSourceReader`), not a pipeline rewrite.
- **Pro:** The example bundle at `examples/` validates the output format.
- **Con:** Adds surface area before v0.1.0 release.
- **Con:** `OKFDocument.save()` needs a second output path (directory vs file).

### Option B: Keep deferring to v0.2.0

- **Pro:** No new code before release.
- **Con:** `knowledge create <url> -o <dir>` still produces a flat KMD file
  instead of the documented example bundle.
- **Con:** Users must use a separate (removed) scripts to generate bundles.

### Option C: Only implement bundle serializer, skip section-aware extraction

- **Pro:** Less code.
- **Con:** Extracted concepts from HTML are still low-quality (entities like
  "NoneType", "Pros") because flat tag-stripping loses section structure.

## Decision

**Accept Option A.** Implement both the OKF v0.1 bundle serializer and the
section-aware HTML source reader in v0.1.0.

## Implementation

### Bundle serializer (`knowledge/kmd/bundle.py`)

- `BundleSerializer(graph, output_dir)` writes each `Concept` to a Markdown
  file with YAML frontmatter (`id`, `title`, `type`, `tags`, `source`).
- Concepts are grouped into subdirectories by `tags` matching known category
  prefixes (e.g. `language` → `rules/language/`).
- Auto-generates `index.md` for each directory.
- Writes `type: concept` for leaf entries, `type: index` for directory
  indexes, `type: bundle` for the root index.

### Section-aware HTML source reader (`knowledge/extraction/sources.py`)

- `HTMLSourceReader` uses Python's `html.parser.HTMLParser` to split HTML
  content by `<h2>`, `<h3>`, `<h4>` headings.
- Returns a list of `(heading_text, section_content_plaintext, heading_level)`
  tuples.
- Each section becomes a separate `Concept` with section-aware naming.

### SDK integration (`knowledge/sdk.py`)

- `OKFDocument.save(path, fmt="kmd")`: accepts `fmt="bundle"` for directory
  output, `fmt="kmd"` for flat KMD (default).
- `Knowledge.create(input)`: if the source is HTML with section headings,
  creates one concept per section and writes the full bundle.

### CLI (`knowledge/cli.py`)

- `knowledge create <input> -o <dir> --format bundle` writes OKF bundle.
- `knowledge create <input> -o <file>.kmd` (default) writes flat KMD.
- `knowledge create <input> -o <dir>` auto-selects bundle when `-o` looks
  like a directory or has no extension.

## Consequences

### Positive

- `knowledge create <url> -o examples/` produces the documented bundle format.
- Section-aware extraction produces meaningful concepts from HTML sources.
- The existing `KnowledgeGraph` model, `ExtractionPass`, and extraction
  pipeline are unchanged — only serialization and source reading are added.
- The bundle format is validated by the example at `examples/`.

### Negative

- `OKFDocument.save()` gains a format parameter, changing its public API.
- Bundle output requires filesystem directory I/O, which is more complex than
  flat file writes.
- HTML section parsing is heuristic — not all HTML sources have clean
  heading structures.

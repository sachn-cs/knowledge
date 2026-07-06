# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Comprehensive module-level docstrings across all 10 source files.
- `.editorconfig` for consistent editor settings.
- `.gitattributes` for line-ending normalization.
- `.env.example` documenting supported environment variables.
- `.github/ISSUE_TEMPLATE/bug_report.md` and `feature_request.md`.
- `.github/PULL_REQUEST_TEMPLATE.md`.
- `.github/dependabot.yml` for automated dependency updates.
- `.github/FUNDING.yml` with sponsor placeholders.
- `docs/getting-started.md`, `docs/architecture.md`, `docs/faq.md` —
  user-facing documentation guides.
- `DEFAULT_MODEL` constant in `knowledge.version` for centralized model
  identifier management.
- `path_map` propagation through `KnowledgeBundleManager` and `Knowledge`
  SDK, enabling tag-based subdirectory grouping from the public API.

### Changed

- **LICENSE**: Updated copyright year to 2026.
- **README.md**: Complete rewrite with badges, features table, configuration
  docs, tech stack, and improved quick-start examples. Corrected Ollama env
  var documentation (`OLLAMA_HOST`).
- **CONTRIBUTING.md**: Expanded from 5 lines to full guide with branch naming,
  commit conventions, PR process, and coding standards.
- **CODE_OF_CONDUCT.md**: Added contact email (`sachncs@gmail.com`).
- **SECURITY.md**: Expanded with supported versions, response timeline,
  disclosure policy, and security best practices.
- **pyproject.toml**: Updated development status from "Planning" to "3 - Alpha";
  added `vulture` to dev dependencies; removed redundant `black` dependency.
  Aligned `black` line-length to 100 (matching ruff config).
- **docs/index.md**: Rewritten with links to new docs and MkDocs-friendly
  homepage structure.
- **docs/adr/README.md**: Updated index with clearer status descriptions.
- **mkdocs.yml**: Updated navigation to match current docs structure.
- Fixed repository URLs from `anomalyco/knowledge` to `sachn-cs/knowledge`
  across all files. Removed made-up `knowledge-sdk.dev` documentation URL.
- **ROADMAP.md**: Aligned with current codebase state (OKF v0.1 already
  implemented; removed stale entries describing a different project).

### Fixed

- **BundleSerializer**: Intermediate directories with no direct entries
  are no longer linked from the root index, preventing broken links
  (`style-rules/index.md` false positive).
- **BundleSerializer**: `links_in_index` regex restricted to `[text](url)`
  Markdown pattern instead of matching any parenthesized content, reducing
  false-positive link warnings.
- **BundleSerializer**: `serialize` now removes stale `.md` files from
  previous writes, preventing orphan accumulation.
- **Knowledge.read_source**: URL scheme detection uses `urlparse()` instead
  of `str.startswith()`, supporting case-insensitive `HTTP://` per RFC 3986.
- **fetch_url**: Charset extraction from `Content-Type` simplified to a
  single expression, removing duplicate stripping.
- **LLMExtractor**: Prompt template changed from `str.format()` to
  `string.Template.safe_substitute()`, preventing `KeyError` crashes on
  section headings containing curly braces.
- **CLI**: Extracted duplicated source-label truncation logic into shared
  `_source_label()` / `_shorten_label()` helpers with named constants.
- **Test suite**: Version format test now matches PEP 440 prefix instead
  of requiring exactly 3 dot-separated parts. Moved misplaced
  `test_add_concept_replaces_existing` from `TestBundleSerializer` to
  `TestKnowledgeGraph`. Added `test_validate_clean_bundle_counts_files`
  for stronger validation coverage.

### Removed

- Dead `ValidationError` exception class (defined but never raised).
- Orphan `.gitignore` entries (`style-guide/`, `examples/`).

## [0.1.0] — 2026-07-05

### Added

- Core Pydantic models: `Concept`, `KnowledgeGraph` (frozen/immutable).
- OKF v0.1 bundle serializer (`BundleSerializer`) with YAML frontmatter,
  tag-based subdirectory grouping, and structural validation.
- LLM-based extraction (`LLMExtractor`) using litellm:
  - HTML heading (`<h2>`–`<h4>`) and Markdown heading (`##`) splitting.
  - Section-aware prompt construction.
  - Pydantic response validation with `model_validate_json`.
- Resilient URL fetching (`fetch_url`) with:
  - Exponential-backoff retries (3 attempts).
  - 50 MiB size limit (content-length and actual bytes).
  - Charset detection from `Content-Type` header.
  - HTTP error classification (retry 429/5xx, bail on 4xx).
- `Knowledge` SDK class (create, create_bundle, update, remove).
- `KnowledgeBundleManager` with create/update/remove operations.
- CLI (`knowledge` command) with create, update, remove subcommands
  and `--model` flag.
- `ParseConceptFile` with YAML round-trip support (`yaml_escape` /
  `yaml_unescape`).
- Bundle validation (link resolution, orphan detection).
- Concept ID slug validation (`^[a-z][a-z0-9-]*$`).
- Test suite: 66 tests (BundleSerializer, SDK, CLI, models, fetch_url,
  parse_concept_file).
- GitHub Actions CI (ruff, mypy, pytest with coverage, build).
- GitHub Actions release workflow (PyPI publishing on tag).
- MkDocs documentation skeleton.
- Architecture Decision Records (ADR-001, ADR-002).

### Fixed

- HTML comment injection in heading splitting (strip `<!-- -->` before
  matching).
- ATX heading trailing `#` not stripped (e.g. `## Title ##`).
- litellm exception scope too narrow (`APIError` only → all exceptions).
- `Content-Length` parse crash on malformed header.
- Charset quote characters preserved in `Content-Type` decoding.
- YAML injection via control characters.
- Unparseable concept files causing silent data loss (now logged as
  warning).

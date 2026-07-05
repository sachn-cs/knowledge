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

### Changed

- **LICENSE**: Updated copyright year to 2026.
- **README.md**: Complete rewrite with badges, features table, configuration
  docs, tech stack, and improved quick-start examples.
- **CONTRIBUTING.md**: Expanded from 5 lines to full guide with branch naming,
  commit conventions, PR process, and coding standards.
- **CODE_OF_CONDUCT.md**: Added contact email (`sachncs@gmail.com`).
- **SECURITY.md**: Expanded with supported versions, response timeline,
  disclosure policy, and security best practices.
- **pyproject.toml**: Updated development status from "Planning" to "3 - Alpha";
  added `black` and `vulture` to dev dependencies; added vulture config.
- **docs/index.md**: Rewritten with links to new docs and MkDocs-friendly
  homepage structure.
- **docs/adr/README.md**: Updated index with clearer status descriptions.
- **mkdocs.yml**: Updated navigation to match current docs structure.
- Fixed repository URLs from `anomalyco/knowledge` to `sachn-cs/knowledge`
  across all files. Removed made-up `knowledge-sdk.dev` documentation URL.

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

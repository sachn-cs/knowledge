# Architecture

The `knowledge` SDK is organized into independent layers with clear boundaries.

## Architectural Layers

```
Knowledge Sources
        │
        ▼
+----------------------+
| Knowledge Extraction |
+----------------------+
        │
        ▼
+----------------------+
| Canonical Knowledge  |
| Model                |
+----------------------+
        │
        ▼
+----------------------+
| OKF Generator        |
+----------------------+
        │
        ▼
+----------------------+
| Verification Engine  |
+----------------------+
        │
        ▼
Verified OKF Document
```

### 1. Source Layer

Responsible for reading external information from Markdown, PDF, HTML, JSON,
plain text, URLs, directories, and future sources.

### 2. Extraction Layer

Converts raw information into structured knowledge — entities, concepts,
relationships, facts, evidence, and provenance.

### 3. Canonical Knowledge Model

The internal representation used throughout the SDK. Every operation works
against this model.

### 4. OKF Layer

Responsible only for parsing and serializing OKF documents.

### 5. Verification Layer

The iterative quality gate protecting knowledge integrity.

### 6. Public API Layer

Exposes the lifecycle of an OKF document through a minimal, predictable API.

## Compiler Pipeline

```
Sources → Parser Passes → Extraction Passes → Normalization Passes →
Analysis Passes → Verification Passes → Repair Passes → Scoring Passes →
OKF Serialization
```

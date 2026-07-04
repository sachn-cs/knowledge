# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in the `knowledge` SDK,
please report it by emailing the maintainers at **security@anomalyco.dev**.

Do **not** open a public GitHub issue for security vulnerabilities.

## Response Timeline

- We will acknowledge receipt within 48 hours.
- We will provide an initial assessment within 5 business days.
- We will coordinate a fix and release timeline based on severity.

## Scope

The following are considered in scope for security reports:

- Remote code execution or command injection
- Unauthorized file system access via document parsing
- Injection attacks via crafted KMD documents
- Denial of service through resource exhaustion (e.g. billion-laughs, zip bombs)

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 0.1.x   | ✅ Active development |

## Security Hardening Guidelines

### Input Validation

- **Always verify untrusted documents.** Run every document from an
  untrusted source through the verification engine before use:
  ```python
  from knowledge import Knowledge
  knowledge = Knowledge()
  doc = knowledge.read("untrusted_doc.md")
  doc.verify(threshold=80.0)
  ```
- **Set a quality threshold.** Lower thresholds admit lower-quality
  knowledge. For untrusted input, use the default (80.0) or higher.
- **Sandbox the parser.** The KMD parser is deterministic and performs
  no I/O beyond reading the file. However, crafted documents with
  extremely long lines or deeply nested structures may consume memory.
  Run document parsing in a resource-limited environment when handling
  untrusted content.

### Supply Chain

- **Pin dependencies.** Use exact versions in production:
  ```bash
  pip install knowledge==0.1.0 pydantic==2.x
  ```
- **Verify integrity.** For production use, install from a pinned git
  commit hash or a signed PyPI release when available.
- **Keep pydantic updated.** Pydantic is the sole runtime dependency
  with a non-trivial attack surface. Monitor its security advisories.

### Deployment

- **Run in a sandboxed environment.** Use containers (Docker), virtual
  environments, or OS-level sandboxes when processing untrusted KMD
  documents.
- **Limit file system access.** The SDK reads and writes files only
  when explicitly instructed. Restrict the working directory to prevent
  path traversal:
  ```python
  import os
  safe_dir = "/safe/knowledge/"
  doc.save(os.path.join(safe_dir, "output.md"))
  ```
- **Set resource limits.** On Linux, use `ulimit` to cap memory and
  file descriptor usage when running batch verification:
  ```bash
  ulimit -v 1048576  # 1 GB virtual memory
  knowledge verify large_doc.md
  ```

### Secrets Management

- **Do not embed secrets in documents.** The SDK stores metadata and
  provenance but has no built-in encryption. Treat KMD documents as
  plaintext.
- **Use environment variables** for API keys or tokens if integrating
  with external reasoning providers.

### Monitoring

- **Log verification failures.** Failed verification may indicate
  malformed or malicious input:
  ```python
  result = doc.verify()
  if not result.threshold_met:
      logging.warning("Document failed verification: %s", doc.source)
  ```
- **Track diagnostic patterns.** Unexpected diagnostic patterns across
  many documents may indicate an attempted injection or data-poisoning
  attack.

## Best Practices

- Validate all KMD documents from untrusted sources via the verification engine
- Run the knowledge SDK in a sandboxed environment when processing untrusted input
- Keep dependencies updated (particularly pydantic)
- Pin dependency versions in production deployments
- Monitor verification diagnostics for anomalous patterns

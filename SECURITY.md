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
- Injection attacks via crafted OKF documents
- Denial of service through resource exhaustion

## Supported Versions

| Version | Supported          |
|---------|-------------------|
| 0.1.x   | ✅ Active development |

## Best Practices

- Validate all OKF documents from untrusted sources via the verification engine
- Run the knowledge SDK in a sandboxed environment when processing untrusted input
- Keep dependencies updated (particularly pydantic)

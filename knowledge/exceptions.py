"""Structured exception hierarchy for the knowledge SDK.

Every SDK operation that can fail raises a subclass of `KnowledgeError`.
Callers may catch the base type for a broad catch, or specific subtypes
to handle distinct failure modes (fetch vs validation) separately.

Exception hierarchy::

    KnowledgeError
    ├── FetchError       — source cannot be fetched or read
    └── ValidationError  — bundle integrity check failed
"""


class KnowledgeError(Exception):
    """Base exception for all SDK errors.

    Catch this type when you want to handle any SDK-originated failure
    uniformly.  For finer-grained handling catch ``FetchError`` or
    ``ValidationError`` instead.
    """


class FetchError(KnowledgeError):
    """The source document could not be fetched or read.

    Raised by :func:`~knowledge.sdk.Knowledge.read_source` and
    :func:`~knowledge.sdk.fetch_url` when:

    * A URL returns a non-retryable HTTP error (4xx except 429).
    * All retry attempts for network/HTTP errors are exhausted.
    * The response body exceeds :obj:`~knowledge.sdk.MAX_BODY_SIZE`.
    * The local file path does not exist or cannot be read.

    The exception message includes the URL or file path and the reason
    for the failure.
    """


class ValidationError(KnowledgeError):
    """An OKF bundle failed structural validation.

    Raised during bundle writing or validation when:

    * Concept files contain duplicate IDs (should not happen with the
      current :class:`~knowledge.models.KnowledgeGraph` implementation
      which enforces unique dict keys).
    * The :class:`~knowledge.kmd.bundle.BundleSerializer.validate`
      method finds orphan files, broken links, or a missing index.
    """

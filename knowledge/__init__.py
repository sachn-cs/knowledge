"""knowledge: An open-source Python SDK for Open Knowledge Format (OKF) documents."""

from knowledge.engine import VerificationEngine, VerificationResult
from knowledge.exceptions import (
    KnowledgeError,
    MergeConflictError,
    ParseError,
    SchemaValidationError,
    SemanticValidationError,
    UnsupportedSourceError,
    VerificationError,
)
from knowledge.okf import OKFParser, OKFSerializer
from knowledge.passes import (
    CompilerPass,
    Diagnostic,
    PassManager,
    PassResult,
    Phase,
    Severity,
)
from knowledge.sdk import Knowledge, OKFDocument
from knowledge.version import __version__

__all__ = [
    "__version__",
    "Knowledge",
    "OKFDocument",
    "VerificationEngine",
    "VerificationResult",
    "KnowledgeError",
    "ParseError",
    "SchemaValidationError",
    "SemanticValidationError",
    "VerificationError",
    "MergeConflictError",
    "UnsupportedSourceError",
    "OKFParser",
    "OKFSerializer",
    "Phase",
    "CompilerPass",
    "PassResult",
    "Severity",
    "Diagnostic",
    "PassManager",
]

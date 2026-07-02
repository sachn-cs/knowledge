"""Tests for exception types."""

from knowledge.exceptions import (
    KnowledgeError,
    MergeConflictError,
    ParseError,
    SchemaValidationError,
    SemanticValidationError,
    UnsupportedSourceError,
    VerificationError,
)


class TestExceptions:
    def test_knowledge_error(self) -> None:
        err = KnowledgeError("base error")
        assert str(err) == "base error"
        assert isinstance(err, Exception)

    def test_parse_error(self) -> None:
        err = ParseError("bad format")
        assert isinstance(err, KnowledgeError)

    def test_schema_validation_error(self) -> None:
        err = SchemaValidationError("schema error")
        assert isinstance(err, KnowledgeError)

    def test_semantic_validation_error(self) -> None:
        err = SemanticValidationError("semantic error")
        assert isinstance(err, KnowledgeError)

    def test_verification_error(self) -> None:
        err = VerificationError("verification error")
        assert isinstance(err, KnowledgeError)

    def test_merge_conflict_error(self) -> None:
        err = MergeConflictError("merge conflict")
        assert isinstance(err, KnowledgeError)

    def test_unsupported_source_error(self) -> None:
        err = UnsupportedSourceError("unsupported")
        assert isinstance(err, KnowledgeError)

    def test_all_subclass_knowledge_error(self) -> None:
        exceptions = [
            ParseError,
            SchemaValidationError,
            SemanticValidationError,
            VerificationError,
            MergeConflictError,
            UnsupportedSourceError,
        ]
        for exc in exceptions:
            assert issubclass(exc, KnowledgeError)

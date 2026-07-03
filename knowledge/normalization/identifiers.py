"""Stable, deterministic identifier generation for knowledge elements.

Identifiers must survive updates, verification, repair, formatting,
and serialization. Identity represents meaning — not position inside
a document.
"""

from __future__ import annotations

import hashlib
import re


class StableIdGenerator:
    """Generates deterministic, content-addressed identifiers.

    The same content always produces the same ID. This ensures
    stability across serialization cycles and enables duplicate
    detection.
    """

    @staticmethod
    def generate(prefix: str, content: str, salt: str = "") -> str:
        raw = f"{prefix}:{content.strip().lower()}{salt}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @staticmethod
    def is_valid(element_id: str) -> bool:
        return bool(re.match(r"^[a-f0-9]{16}$", element_id))


class CanonicalIdGenerator:
    """Generates canonical identifiers for normalized knowledge elements.

    Unlike StableIdGenerator which uses raw content, this generator
    strips whitespace, normalizes casing, and applies other
    normalizations before hashing.
    """

    @staticmethod
    def normalize_name(name: str) -> str:
        return re.sub(r"\s+", " ", name.strip().lower())

    @staticmethod
    def generate(prefix: str, name: str) -> str:
        normalized = CanonicalIdGenerator.normalize_name(name)
        raw = f"{prefix}:{normalized}"
        return hashlib.sha256(raw.encode()).hexdigest()[:16]

    @staticmethod
    def entity_id(name: str) -> str:
        return CanonicalIdGenerator.generate("ent", name)

    @staticmethod
    def concept_id(name: str) -> str:
        return CanonicalIdGenerator.generate("concept", name)

    @staticmethod
    def fact_id(statement: str) -> str:
        return CanonicalIdGenerator.generate("fact", statement)

    @staticmethod
    def relationship_id(source: str, rel_type: str, target: str) -> str:
        """Generate a deterministic relationship ID from its parts."""
        return CanonicalIdGenerator.generate("rel", f"{source}:{rel_type}:{target}")

    @staticmethod
    def evidence_id(content: str) -> str:
        """Generate a deterministic evidence ID from content."""
        return CanonicalIdGenerator.generate("ev", content)

    @staticmethod
    def source_id(source: str) -> str:
        """Generate a deterministic source ID."""
        return CanonicalIdGenerator.generate("src", source)

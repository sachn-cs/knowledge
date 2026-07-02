"""Source readers for knowledge extraction.

Source readers acquire raw content from various input formats.
They never perform semantic analysis — only format-specific parsing
to produce a canonical SourceDocument.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class SourceDocument:
    """Canonical representation of a source document.

    Contains the raw text content along with metadata about its origin.
    """

    content: str
    source: str
    metadata: dict[str, str] = field(default_factory=dict)


class TextSourceReader:
    """Reads plain text content into a SourceDocument."""

    def read(self, content: str, source: str = "text") -> SourceDocument:
        return SourceDocument(content=content, source=source, metadata={"format": "text"})


class MarkdownSourceReader:
    """Reads Markdown content, stripping formatting to produce plain text.

    Preserves structural information (headings) as metadata while
    removing Markdown syntax for downstream extraction.
    """

    # Regex to remove inline formatting
    _LINK_PATTERN = re.compile(r"\[([^\]]+)\]\([^)]+\)")
    _BOLD_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
    _ITALIC_PATTERN = re.compile(r"(?<!\*)\*([^*]+)\*(?!\*)")
    _CODE_PATTERN = re.compile(r"`([^`]+)`")
    _HEADING_PATTERN = re.compile(r"^#{1,6}\s+(.*)", re.MULTILINE)

    def read(self, content: str, source: str = "markdown") -> SourceDocument:
        text = content
        text = self._LINK_PATTERN.sub(r"\1", text)
        text = self._BOLD_PATTERN.sub(r"\1", text)
        text = self._ITALIC_PATTERN.sub(r"\1", text)
        text = self._CODE_PATTERN.sub(r"\1", text)
        headings = self._HEADING_PATTERN.findall(content)

        return SourceDocument(
            content=text,
            source=source,
            metadata={
                "format": "markdown",
                "headings": ", ".join(h.strip() for h in headings),
            },
        )

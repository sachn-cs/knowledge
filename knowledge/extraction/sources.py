"""HTML section parser — splits HTML by heading tags."""

from __future__ import annotations

import re
from dataclasses import dataclass
from html.parser import HTMLParser


@dataclass(frozen=True)
class SourceSection:
    """A single section extracted from an HTML document.

    Attributes:
        heading: The section heading text (HTML stripped).
        content: Plain text content of the section.
        level: The heading level (2 for <h2>, 3 for <h3>, etc.).
    """

    heading: str
    content: str
    level: int


class HTMLSourceReader:
    """Reads HTML content, extracting sections by headings.

    Parses HTML into structured sections based on <h2>, <h3>, <h4>
    heading tags. Each section contains the plain text between
    headings.
    """

    HEADING_TAGS = frozenset({"h2", "h3", "h4"})

    def read_sections(self, content: str) -> list[SourceSection]:
        """Parse HTML into structured sections by heading tags.

        Args:
            content: The raw HTML content.
            source: Identifier for the source document (unused).

        Returns:
            A list of SourceSection tuples (heading, plain_text, level).
        """
        parser = _HTMLSectionParser()
        parser.feed(content)
        parser.close()
        sections: list[SourceSection] = []
        for heading, body, level in parser.sections:
            plain = re.sub(r"<[^>]+>", " ", body)
            plain = re.sub(r" {2,}", " ", plain).strip()
            h_text = re.sub(r"<[^>]+>", " ", heading)
            h_text = re.sub(r" {2,}", " ", h_text).strip()
            sections.append(SourceSection(heading=h_text, content=plain, level=level))
        return sections


class _HTMLSectionParser(HTMLParser):
    """Internal HTML parser that extracts sections by heading tags."""

    def __init__(self, *, convert_charrefs: bool = True) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self.sections: list[tuple[str, str, int]] = []
        self._current_heading: str = ""
        self._current_body: list[str] = []
        self._current_level: int = 0
        self._in_heading: bool = False
        self._skip_tags: frozenset[str] = frozenset(
            {"script", "style", "nav", "footer", "header"}
        )
        self._skip_depth: int = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_lower = tag.lower()
        if tag_lower in self._skip_tags:
            self._skip_depth += 1
            return
        if self._skip_depth > 0:
            return
        if tag_lower in HTMLSourceReader.HEADING_TAGS:
            self._finalize_current_section()
            self._in_heading = True
            self._current_heading = ""
            self._current_level = int(tag_lower[1])

    def handle_endtag(self, tag: str) -> None:
        tag_lower = tag.lower()
        if tag_lower in self._skip_tags:
            self._skip_depth -= 1
            return
        if self._skip_depth > 0:
            return
        if tag_lower in HTMLSourceReader.HEADING_TAGS:
            self._in_heading = False

    def handle_data(self, data: str) -> None:
        if self._skip_depth > 0:
            return
        if self._in_heading:
            self._current_heading += data
        else:
            self._current_body.append(data)

    def _finalize_current_section(self) -> None:
        if self._current_heading.strip():
            body = "".join(self._current_body).strip()
            if body:
                self.sections.append(
                    (self._current_heading.strip(), body, self._current_level)
                )
        self._current_heading = ""
        self._current_body = []
        self._current_level = 0

"""Minimal SDK — creates OKF bundles from URLs or file paths."""

from __future__ import annotations

import os
import re
from urllib.request import urlopen

from knowledge.extraction.sources import HTMLSourceReader, SourceSection
from knowledge.kmd.bundle import BundleSerializer
from knowledge.models import Concept, KnowledgeGraph

_HTML_PATTERN = re.compile(r"^\s*(?:<!DOCTYPE\s+html|<html)\s", re.IGNORECASE)
_H2_PATTERN = re.compile(r"<h2[^>]*>.*?</h2>", re.IGNORECASE | re.DOTALL)


class Knowledge:
    """Entry point for creating OKF bundles from sources."""

    def __init__(self) -> None:
        pass

    def create(self, input: str, path_map: dict[str, str] | None = None) -> KnowledgeGraph:
        """Fetch and parse content, returning a KnowledgeGraph of section concepts.

        Args:
            input: URL (http/https) or file path to read.
            path_map: Optional tag→subdirectory mapping for bundle organization.

        Returns:
            A KnowledgeGraph with one Concept per HTML section heading.
        """
        if input.startswith("http://") or input.startswith("https://"):
            raw = urlopen(input).read().decode("utf-8")
        else:
            with open(input, encoding="utf-8") as f:
                raw = f.read()

        if _is_html(raw):
            return _parse_html(raw, path_map or {})

        raise ValueError("Only HTML sources are supported for bundle creation")

    def create_bundle(
        self, input: str, output_dir: str, path_map: dict[str, str] | None = None
    ) -> None:
        """Create an OKF bundle from a source and write it to a directory.

        Args:
            input: URL or file path.
            output_dir: Output directory for the bundle.
            path_map: Optional tag→subdirectory mapping.
        """
        graph = self.create(input, path_map=path_map)
        os.makedirs(output_dir, exist_ok=True)
        BundleSerializer(path_map=path_map).serialize(graph, output_dir)


def _is_html(content: str) -> bool:
    stripped = content.lstrip()
    return bool(_HTML_PATTERN.match(stripped)) or bool(_H2_PATTERN.search(content))


def _heading_slug(heading: str) -> str:
    slug = heading.lower()
    slug = re.sub(r"^\d+(?:\.\d+)*\s+", "", slug)
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug if slug else "section"


def _parse_html(raw: str, path_map: dict[str, str]) -> KnowledgeGraph:
    reader = HTMLSourceReader()
    sections = reader.read_sections(raw)

    graph = KnowledgeGraph()

    for section in sections:
        slug = _heading_slug(section.heading)
        tags = _section_tags(section, sections)
        concept = Concept(
            id=slug,
            name=section.heading,
            description=section.content if section.content else None,
            tags=tags,
        )
        graph = graph.add_concept(concept)

    return graph


def _section_tags(section: SourceSection, all_sections: list[SourceSection]) -> list[str]:
    tags: list[str] = []
    if section.level > 2:
        parent_slug = ""
        for s in all_sections:
            if s.level == 2:
                parent_slug = _heading_slug(s.heading)
            if s is section:
                break
        if parent_slug:
            tags.append(parent_slug)
    else:
        tags.append(_heading_slug(section.heading))
    return tags

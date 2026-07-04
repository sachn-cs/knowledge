"""OKF v0.1 directory-bundle serializer.

Converts a KnowledgeGraph into a directory of Markdown files with
YAML frontmatter, one file per concept, organized into subdirectories
by tag-based grouping.

    output_dir/
      index.md          -- root bundle index (type: bundle)
      <subdir>/
        index.md        -- group index (type: index)
        <concept>.md    -- concept file (type: concept)
"""

from __future__ import annotations

import os
from collections import defaultdict

from knowledge.models import Concept, KnowledgeGraph


class BundleSerializer:
    """Serializes a KnowledgeGraph into an OKF v0.1 directory bundle."""

    def __init__(self, path_map: dict[str, str] | None = None) -> None:
        self.path_map = path_map or {}

    def serialize(self, graph: KnowledgeGraph, output_dir: str) -> None:
        path_groups: dict[str, list[tuple[str, str]]] = defaultdict(list)
        flat_concepts: list[tuple[str, str]] = []

        for cid, concept in sorted(graph.concepts.items()):
            subdir = self._find_path(concept.tags)
            entry = (cid, concept.name)
            if subdir:
                path_groups[subdir].append(entry)
            else:
                flat_concepts.append(entry)

        all_dirs: set[str] = set()
        for subdir in path_groups:
            parts = subdir.split("/")
            for i in range(1, len(parts) + 1):
                all_dirs.add("/".join(parts[:i]))

        for subdir, entries in sorted(path_groups.items()):
            target = os.path.join(output_dir, subdir)
            os.makedirs(target, exist_ok=True)
            for cid, _name in entries:
                self._write_concept(target, graph.concepts[cid])

        for _cid, _name in flat_concepts:
            self._write_concept(output_dir, graph.concepts[_cid])

        for subdir in sorted(all_dirs):
            target = os.path.join(output_dir, subdir)
            raw_entries = path_groups.get(subdir, [])
            if not raw_entries:
                continue
            title = self._dir_title(subdir)
            index_entries: list[tuple[str, str, str]] = [
                (cid, name, "") for cid, name in raw_entries
            ]
            self._write_index(target, title, "index", index_entries)

        root_entries: list[tuple[str, str, str]] = [
            (cid, name, "") for cid, name in flat_concepts
        ]
        for subdir in sorted(all_dirs):
            title = self._dir_title(subdir)
            root_entries.append((subdir, title, subdir))
        self._write_index(output_dir, "Knowledge Bundle", "bundle", root_entries)

    def _find_path(self, tags: list[str]) -> str:
        for tag in tags:
            if tag in self.path_map:
                return self.path_map[tag]
        return ""

    @staticmethod
    def _dir_title(subdir: str) -> str:
        parts = subdir.replace("-", " ").replace("_", " ").split("/")
        return " / ".join(p.title() for p in parts)

    def _write_concept(self, directory: str, concept: Concept) -> None:
        tag_list = ", ".join(concept.tags) if concept.tags else ""
        frontmatter_lines = [
            "---",
            f"id: {concept.id}",
            f"title: \"{concept.name}\"",
            "type: concept",
        ]
        if tag_list:
            frontmatter_lines.append(f"tags: [{tag_list}]")
        frontmatter_lines.append("")
        frontmatter_lines.append("---")

        body_lines = [""]
        if concept.description:
            body_lines.append(f"## {concept.name}")
            body_lines.append("")
            body_lines.append(concept.description)

        content = "\n".join(frontmatter_lines + body_lines) + "\n"
        filepath = os.path.join(directory, f"{concept.id}.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_index(
        self,
        directory: str,
        title: str,
        index_type: str,
        entries: list[tuple[str, str, str]],
    ) -> None:
        frontmatter_lines = [
            "---",
            f"id: {self._index_id(directory, title)}",
            f"title: \"{title}\"",
            f"type: {index_type}",
            "",
            "---",
        ]

        body_lines = [
            "",
            f"# {title}",
            "",
        ]
        for eid, name, link_path in entries:
            if link_path:
                body_lines.append(f"- [{name}]({link_path}/index.md)")
            else:
                body_lines.append(f"- [{name}]({eid}.md)")

        content = "\n".join(frontmatter_lines + body_lines) + "\n"
        filepath = os.path.join(directory, "index.md")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _index_id(directory: str, title: str) -> str:
        base = (
            os.path.basename(directory.rstrip("/"))
            if directory and directory not in (".", "")
            else title.lower()
        )
        return base.replace(" ", "-").replace("/", "-").lower()

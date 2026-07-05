"""Bundle management — create, update, and remove operations.

This module bridges the LLM extraction layer
(:class:`~knowledge.llm.extractor.LLMExtractor`) with the OKF
serialization layer (:class:`~knowledge.kmd.bundle.BundleSerializer`),
providing the three core operations:

* :meth:`KnowledgeBundleManager.create` — extract and write a new bundle.
* :meth:`KnowledgeBundleManager.update` — re-extract and overwrite.
* :meth:`KnowledgeBundleManager.remove` — read, remove concepts, write.

Each operation returns the number of concept files written, which is
used by the CLI for progress feedback.

Reading bundles
---------------
:func:`read_bundle` walks a bundle directory, parsing each ``.md``
concept file back into a :class:`~knowledge.models.Concept` via
:func:`parse_concept_file`.  Files whose frontmatter is missing or
malformed are logged and skipped (rather than aborting the operation).
"""

from __future__ import annotations

import logging
import os
import re

from knowledge.exceptions import KnowledgeError
from knowledge.kmd.bundle import BundleSerializer
from knowledge.llm.extractor import LLMExtractor
from knowledge.models import Concept, KnowledgeGraph

logger = logging.getLogger(__name__)


class KnowledgeBundleManager:
    """High-level operations for LLM-based knowledge bundles.

    Usage
    -----
    ::

        manager = KnowledgeBundleManager(model="gpt-4o")
        count = manager.create(raw_text, "./my-bundle")
        count = manager.update(raw_text, "./my-bundle")
        count = manager.remove(["section-a"], "./my-bundle")
    """

    def __init__(self, model: str = "gpt-4o") -> None:
        """Initialise the manager.

        Args:
            model: A litellm-compatible model identifier.
                Defaults to ``"gpt-4o"``.
        """
        self.model = model

    def create(self, source_text: str, output_dir: str) -> int:
        """Extract concepts from *source_text* and write a new OKF bundle.

        The output directory is created if it does not exist.

        Args:
            source_text: The raw document text (HTML or Markdown).
            output_dir: Directory to write the bundle into.

        Returns:
            Number of concept files written.
        """
        extractor = LLMExtractor(model=self.model)
        graph = extractor.extract(source_text)
        os.makedirs(output_dir, exist_ok=True)
        return BundleSerializer().serialize(graph, output_dir)

    def update(self, source_text: str, bundle_dir: str) -> int:
        """Re-extract concepts from *source_text* and overwrite *bundle_dir*.

        This is a **complete replacement** — all concept files are
        regenerated from scratch.  The previous bundle contents are
        discarded.

        Args:
            source_text: The raw document text (HTML or Markdown).
            bundle_dir: Existing bundle directory to overwrite.

        Returns:
            Number of concept files written.
        """
        extractor = LLMExtractor(model=self.model)
        graph = extractor.extract(source_text)
        os.makedirs(bundle_dir, exist_ok=True)
        return BundleSerializer().serialize(graph, bundle_dir)

    def remove(self, concept_ids: list[str], bundle_dir: str) -> int:
        """Remove specific concepts from *bundle_dir* by ID.

        The bundle is read back from disk, concepts matching the given
        IDs are removed, and the result is written back.  Non-existent
        IDs are silently ignored (idempotent).

        Args:
            concept_ids: Concept IDs to remove.
            bundle_dir: Existing bundle directory to modify.

        Returns:
            Number of concept files written after removal.
        """
        graph = self.read_bundle(bundle_dir)
        for cid in concept_ids:
            graph = graph.remove_concept(cid)
        os.makedirs(bundle_dir, exist_ok=True)
        return BundleSerializer().serialize(graph, bundle_dir)

    @staticmethod
    def read_bundle(bundle_dir: str) -> KnowledgeGraph:
        """Read an existing bundle directory back into a ``KnowledgeGraph``.

        Walks the directory tree and parses every ``.md`` file that is
        not ``index.md`` via :func:`parse_concept_file`.  Unparseable
        files are logged at ``WARNING`` level and skipped.

        Args:
            bundle_dir: The bundle directory to read.

        Returns:
            A ``KnowledgeGraph`` containing all successfully parsed
            concepts.

        Raises:
            KnowledgeError: If *bundle_dir* does not contain an
                ``index.md`` file (heuristic for "not a valid bundle").
        """
        graph = KnowledgeGraph()
        index_path = os.path.join(bundle_dir, "index.md")
        if not os.path.isfile(index_path):
            raise KnowledgeError(f"No bundle found at {bundle_dir}")

        for root, _, files in os.walk(bundle_dir):
            for file in files:
                if file == "index.md" or not file.endswith(".md"):
                    continue
                filepath = os.path.join(root, file)
                concept = parse_concept_file(filepath)
                if concept is not None:
                    graph = graph.add_concept(concept)
                else:
                    logger.warning("Skipping unparseable concept file: %s", filepath)

        return graph


def yaml_unescape(value: str) -> str:
    """Reverse the :func:`~knowledge.kmd.bundle.BundleSerializer.yaml_escape` transform.

    This function is the inverse of the
    :meth:`~knowledge.kmd.bundle.BundleSerializer.yaml_escape` used
    during serialization.  Applying both in sequence produces the
    original string::

        yaml_unescape(yaml_escape(s)) == s

    Unescaping handles (in order):

    1. ``\\n`` → newline
    2. ``\\r`` → carriage return
    3. ``\\t`` → tab
    4. ``\\"`` → literal double quote
    5. ``\\\\`` → literal backslash
    6. ``\\xNN`` → arbitrary byte by hex value (e.g. ``\\x00`` → NUL)

    The ordering is important: ``\\\\`` is unescaped *after* ``\\n``,
    etc. so that an escaped backslash preceding an ``n`` is not
    misinterpreted as a newline.

    Args:
        value: A YAML-escaped string (as produced by
            :func:`~knowledge.kmd.bundle.BundleSerializer.yaml_escape`).

    Returns:
        The original unescaped string.
    """
    value = value.replace("\\n", "\n")
    value = value.replace("\\r", "\r")
    value = value.replace("\\t", "\t")
    value = value.replace('\\"', '"')
    value = value.replace("\\\\", "\\")
    value = re.sub(
        r"\\x([0-9a-fA-F]{2})",
        lambda m: chr(int(m.group(1), 16)),
        value,
    )
    return value


def parse_concept_file(filepath: str) -> Concept | None:
    """Parse a single concept ``.md`` file back into a :class:`~knowledge.models.Concept`.

    The file is expected to have YAML frontmatter delimited by ``---``
    lines::

        ---
        id: some-slug
        title: "Some Title"
        type: concept
        tags: ["tag-a", "tag-b"]
        ---

        ## Some Title

        Body content follows here.

    Parsing is **naive** (line-based) — it handles the limited subset of
    YAML used by the :class:`~knowledge.kmd.bundle.BundleSerializer`.
    Multi-line values, nested structures, and arbitrary YAML are not
    supported.

    Args:
        filepath: Path to the ``.md`` file.

    Returns:
        A :class:`~knowledge.models.Concept` instance if the frontmatter
        can be parsed and contains at least an ``id`` and ``title``,
        otherwise ``None``.
    """
    try:
        with open(filepath, encoding="utf-8") as f:
            content = f.read()
    except OSError as exc:
        logger.warning("Skipping unreadable concept file %s: %s", filepath, exc)
        return None

    frontmatter_match = re.match(r"^---\s*\n(.+?)\n---", content, re.DOTALL)
    if not frontmatter_match:
        return None

    fm_lines = frontmatter_match.group(1).split("\n")
    metadata: dict[str, str | list[str]] = {}
    for line in fm_lines:
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"')
            value = yaml_unescape(value)
            if key == "tags":
                raw = value.strip("[]").strip()
                value = [yaml_unescape(t.strip().strip('"')) for t in raw.split(",")] if raw else []
            metadata[key] = value

    cid = metadata.get("id")
    name = metadata.get("title")
    if not cid or not name:
        return None

    body = content[frontmatter_match.end() :].strip()
    # Strip leading h1/h2 if present
    body = re.sub(r"^#+\s+.*", "", body, count=1).strip()

    raw_tags = metadata.get("tags", [])
    tags: list[str] = raw_tags if isinstance(raw_tags, list) else []
    return Concept(
        id=str(cid),
        name=str(name),
        description=body if body else None,
        tags=tags,
    )

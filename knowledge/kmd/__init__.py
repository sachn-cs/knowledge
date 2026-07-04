"""Knowledge Markdown (KMD) persistence layer.

KMD is a flat Markdown format for serializing KnowledgeGraphs.
It uses ``## Section: id`` headings and ``- **field**: value`` lines.
"""

from knowledge.kmd.parser import KMDParser
from knowledge.kmd.serializer import KMDSerializer

__all__ = [
    "KMDParser",
    "KMDSerializer",
]

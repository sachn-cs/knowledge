"""Alias resolution — detecting when different names refer to the same entity.

Deprecated: Use ``DuplicateDetector.deduplicate_entities`` instead.
Functionality has been consolidated into ``knowledge.normalization.dedup``
to eliminate duplicate merge logic.
"""

from knowledge.normalization.dedup import DuplicateDetector

AliasResolver = DuplicateDetector

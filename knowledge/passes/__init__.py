"""Compiler pass framework for the knowledge SDK."""

from knowledge.passes.analysis import GraphStatisticsPass
from knowledge.passes.base import CompilerPass, KnowledgeScore, PassResult, Phase
from knowledge.passes.consistency import ConsistencyValidationPass
from knowledge.passes.diagnostics import Diagnostic, Severity
from knowledge.passes.extraction import ExtractionPass
from knowledge.passes.manager import PassManager, PipelineResult
from knowledge.passes.normalization import AliasResolutionPass, DuplicateDetectionPass
from knowledge.passes.repair import (
    AttachProvenancePass,
    FixEvidenceRefsPass,
    MergeDuplicateEntitiesPass,
    NormalizeConfidencePass,
)
from knowledge.passes.schema import SchemaValidationPass
from knowledge.passes.scoring import ScoringPass
from knowledge.passes.structural import StructuralValidationPass
from knowledge.passes.verification import (
    EvidenceValidationPass,
    OntologyValidationPass,
    SemanticValidationPass,
)

__all__ = [
    "Phase",
    "CompilerPass",
    "PassResult",
    "Severity",
    "Diagnostic",
    "PassManager",
    "PipelineResult",
    "ExtractionPass",
    "AliasResolutionPass",
    "DuplicateDetectionPass",
    "SemanticValidationPass",
    "OntologyValidationPass",
    "EvidenceValidationPass",
    "SchemaValidationPass",
    "StructuralValidationPass",
    "ConsistencyValidationPass",
    "ScoringPass",
    "GraphStatisticsPass",
    "KnowledgeScore",
    "MergeDuplicateEntitiesPass",
    "AttachProvenancePass",
    "FixEvidenceRefsPass",
    "NormalizeConfidencePass",
]

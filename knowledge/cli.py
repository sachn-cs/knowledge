"""CLI for the knowledge SDK.

Commands: create, read, update, verify, inspect, score, diff
"""

from __future__ import annotations

import argparse
import sys

from knowledge import Knowledge
from knowledge.okf import OKFSerializer


def _get_knowledge() -> Knowledge:
    return Knowledge()


def cmd_create(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.create(args.input, fmt=args.format, verify=not args.no_verify)
    if args.output:
        doc.save(args.output)
        print(f"Created and saved to {args.output}")
    else:
        serializer = OKFSerializer()
        print(serializer.serialize(doc.graph))


def cmd_read(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.read(args.path)
    info = doc.inspect()
    print(f"Entities: {info['entity_count']}")
    print(f"Concepts: {info['concept_count']}")
    print(f"Facts: {info['fact_count']}")
    print(f"Relationships: {info['relationship_count']}")
    print(f"Evidence: {info['evidence_count']}")
    if info["source"]:
        print(f"Source: {info['source']}")


def cmd_update(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.read(args.document)
    doc = knowledge.update(doc, args.input, fmt=args.format)
    if args.output:
        doc.save(args.output)
        print(f"Updated and saved to {args.output}")
    else:
        serializer = OKFSerializer()
        print(serializer.serialize(doc.graph))


def cmd_verify(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.read(args.path)
    result = doc.verify(threshold=args.threshold)
    print(f"Score: {result.score.overall:.1f}%")
    print(f"Converged: {result.converged}")
    print(f"Threshold met: {result.threshold_met}")
    print(f"Iterations: {result.iteration_count}")
    print(f"Repairs applied: {result.repairs_applied}")
    for d in result.diagnostics:
        level = d.severity.value.upper()
        print(f"  [{level}] {d.message}")
    if args.output and result.graph:
        doc.save(args.output)
        print(f"Verified document saved to {args.output}")


def cmd_inspect(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.read(args.path)
    info = doc.inspect()
    for key, value in info.items():
        print(f"{key.replace('_', ' ').title()}: {value}")


def cmd_score(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc = knowledge.read(args.path)
    score = doc.score()
    print(f"Overall:           {score.overall:.1f}%")
    print(f"Completeness:      {score.completeness:.1f}%")
    print(f"Consistency:       {score.consistency:.1f}%")
    print(f"Evidence Quality:  {score.evidence_quality:.1f}%")
    print(f"Ontology Quality:  {score.ontology_quality:.1f}%")
    print(f"Metadata:          {score.metadata_completeness:.1f}%")


def cmd_diff(args: argparse.Namespace) -> None:
    knowledge = _get_knowledge()
    doc_a = knowledge.read(args.document_a)
    doc_b = knowledge.read(args.document_b)
    changes = doc_a.diff(doc_b)
    for category, items in changes.items():
        if items:
            label = category.replace("_", " ").title()
            for item in items:
                print(f"  {label}: {item}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="knowledge — Open Knowledge Format SDK CLI",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create a new OKF document")
    p_create.add_argument("input", help="Source content or file path")
    p_create.add_argument("-f", "--format", default="text", choices=["text", "markdown"])
    p_create.add_argument("-o", "--output", help="Output file path")
    p_create.add_argument("--no-verify", action="store_true", help="Skip verification")
    p_create.set_defaults(func=cmd_create)

    p_read = sub.add_parser("read", help="Read an existing OKF document")
    p_read.add_argument("path", help="Path to OKF document")
    p_read.set_defaults(func=cmd_read)

    p_update = sub.add_parser("update", help="Update an OKF document with new knowledge")
    p_update.add_argument("document", help="Path to existing OKF document")
    p_update.add_argument("input", help="New source content or file path")
    p_update.add_argument("-f", "--format", default="text", choices=["text", "markdown"])
    p_update.add_argument("-o", "--output", help="Output file path")
    p_update.set_defaults(func=cmd_update)

    p_verify = sub.add_parser("verify", help="Verify an OKF document")
    p_verify.add_argument("path", help="Path to OKF document")
    p_verify.add_argument("-t", "--threshold", type=float, default=80.0, help="Quality threshold")
    p_verify.add_argument("-o", "--output", help="Output file path for repaired document")
    p_verify.set_defaults(func=cmd_verify)

    p_inspect = sub.add_parser("inspect", help="Inspect an OKF document")
    p_inspect.add_argument("path", help="Path to OKF document")
    p_inspect.set_defaults(func=cmd_inspect)

    p_score = sub.add_parser("score", help="Score an OKF document")
    p_score.add_argument("path", help="Path to OKF document")
    p_score.set_defaults(func=cmd_score)

    p_diff = sub.add_parser("diff", help="Diff two OKF documents")
    p_diff.add_argument("document_a", help="First OKF document")
    p_diff.add_argument("document_b", help="Second OKF document")
    p_diff.set_defaults(func=cmd_diff)

    args = parser.parse_args()
    try:
        args.func(args)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

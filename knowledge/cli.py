"""Minimal CLI — only ``create`` for OKF bundles."""

from __future__ import annotations

import argparse
import sys
import traceback

from knowledge import Knowledge


def cmd_create(args: argparse.Namespace) -> None:
    """Create an OKF bundle from an HTML source."""
    knowledge = Knowledge()
    knowledge.create_bundle(args.input, args.output)
    print(f"Created bundle at {args.output}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="knowledge — OKF bundle creation tool",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_create = sub.add_parser("create", help="Create an OKF bundle from a URL or file")
    p_create.add_argument("input", help="URL or file path")
    p_create.add_argument("output", help="Output directory for the bundle")
    p_create.set_defaults(func=cmd_create)

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except Exception:
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

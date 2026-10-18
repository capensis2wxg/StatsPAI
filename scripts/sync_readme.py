#!/usr/bin/env python3
"""Synchronize the GitHub-compatible README.md copy from README.qmd."""

from __future__ import annotations

import argparse
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCE = REPO_ROOT / "README.qmd"
DESTINATION = REPO_ROOT / "README.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="fail if README.md differs from README.qmd",
    )
    args = parser.parse_args()

    source = SOURCE.read_bytes()
    destination = DESTINATION.read_bytes() if DESTINATION.exists() else None
    if destination == source:
        print("README.md is synchronized with README.qmd.")
        return 0
    if args.check:
        parser.error("README.md is out of sync; run python scripts/sync_readme.py")

    DESTINATION.write_bytes(source)
    print("Synchronized README.md from README.qmd.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

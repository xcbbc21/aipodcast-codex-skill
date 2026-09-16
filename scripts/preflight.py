#!/usr/bin/env python3
"""Check the local aipodcast runtime without exposing credentials."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path
from typing import Mapping


REQUIRED_FLAGS = {"--text", "--no-rescript", "--voice", "--language", "--no-progress"}


def has_required_flags(help_text: str) -> bool:
    return all(flag in help_text for flag in REQUIRED_FLAGS)


def resolve_python(
    requested: Path | None,
    *,
    environ: Mapping[str, str] = os.environ,
    current_python: Path = Path(sys.executable),
) -> Path:
    if requested is not None:
        return requested
    configured = environ.get("AIPODCAST_PYTHON")
    return Path(configured) if configured else current_python


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--python",
        type=Path,
        help="interpreter to check; defaults to AIPODCAST_PYTHON or the current Python",
    )
    args = parser.parse_args()
    python = resolve_python(args.python)

    errors: list[str] = []
    if not python.is_file():
        errors.append(f"interpreter not found: {python}")
        help_text = ""
    else:
        result = subprocess.run(
            [str(python), "-m", "aipodcast.cli", "generate", "--help"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        help_text = result.stdout
        if result.returncode != 0:
            errors.append("aipodcast CLI help command failed")
        elif not has_required_flags(help_text):
            missing = ", ".join(sorted(REQUIRED_FLAGS - set(help_text.split())))
            errors.append(f"CLI is missing required flags: {missing}")

    key_present = bool(os.environ.get("MINIMAX_API_KEY") or os.environ.get("AIPODCAST_API_KEY"))
    print(f"API key configured: {'yes' if key_present else 'no'}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("PASS: local aipodcast runtime is ready")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

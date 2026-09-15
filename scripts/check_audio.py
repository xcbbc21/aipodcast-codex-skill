#!/usr/bin/env python3
"""Check an audio file's duration and report long silent passages when available."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path


DURATION_RE = re.compile(r"estimated duration:\s*([0-9.]+)\s*sec", re.IGNORECASE)
SILENCE_RE = re.compile(r"silence_duration:\s*([0-9.]+)", re.IGNORECASE)


def parse_duration_seconds(afinfo_output: str) -> float | None:
    match = DURATION_RE.search(afinfo_output)
    return float(match.group(1)) if match else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spoken_text", type=Path)
    parser.add_argument("audio", type=Path)
    parser.add_argument("--skip-silence-check", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not args.spoken_text.is_file():
        errors.append(f"spoken text does not exist: {args.spoken_text}")
    if not args.audio.is_file() or args.audio.stat().st_size == 0:
        errors.append(f"audio is missing or empty: {args.audio}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    afinfo = subprocess.run(
        ["afinfo", str(args.audio)], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False
    )
    duration = parse_duration_seconds(afinfo.stdout)
    if afinfo.returncode != 0 or duration is None:
        print("ERROR: unable to decode audio duration with afinfo")
        return 1

    spoken_chars = len(re.sub(r"\s+", "", args.spoken_text.read_text(encoding="utf-8")))
    print(f"duration seconds: {duration:.2f}")
    print(f"spoken characters: {spoken_chars}")
    if duration > 0:
        print(f"observed characters per minute: {spoken_chars / duration * 60:.1f}")

    if not args.skip_silence_check and shutil.which("ffmpeg"):
        silence = subprocess.run(
            ["ffmpeg", "-hide_banner", "-i", str(args.audio), "-af", "silencedetect=noise=-45dB:d=2", "-f", "null", "-"],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        long_silences = [float(value) for value in SILENCE_RE.findall(silence.stdout) if float(value) >= 2]
        if long_silences:
            print("REVIEW: long silence durations: " + ", ".join(f"{item:.2f}s" for item in long_silences))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

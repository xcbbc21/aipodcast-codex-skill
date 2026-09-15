#!/usr/bin/env python3
"""Review a TTS-ready Markdown file and optionally export spoken plain text."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


URL_RE = re.compile(r"https?://\S+", re.IGNORECASE)
TITLE_RE = re.compile(r"^#\s+", re.MULTILINE)
METADATA_RE = re.compile(r"^>\s*", re.MULTILINE)
RAW_FOOTNOTE_RE = re.compile(r"[①②③④⑤⑥⑦⑧⑨⑩]")
MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]*\)")


def render_spoken_text(text: str) -> str:
    """Remove archive-only Markdown while retaining audible paragraphs."""
    paragraphs: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith(">"):
            continue
        stripped = MARKDOWN_LINK_RE.sub(r"\1", stripped)
        stripped = re.sub(r"^[-*+]\s+", "", stripped)
        stripped = re.sub(r"^\d+[.)、]\s+", "", stripped)
        stripped = URL_RE.sub("", stripped)
        stripped = RAW_FOOTNOTE_RE.sub("", stripped)
        stripped = re.sub(r"\s+", " ", stripped).strip()
        if stripped:
            paragraphs.append(stripped)
    return "\n\n".join(paragraphs)


def analyze_text(text: str, mode: str, coverage_path: str | None = None) -> dict[str, object]:
    errors: list[str] = []
    warnings: list[str] = []
    title_count = len(TITLE_RE.findall(text))
    if title_count != 1:
        errors.append(f"应恰好保留一个一级标题，当前为 {title_count} 个")
    if METADATA_RE.search(text):
        errors.append("含有元信息引用块；请移出实际朗读稿")
    if URL_RE.search(text):
        errors.append("含有 URL；请移入来源记录或改写为必要事实")
    if RAW_FOOTNOTE_RE.search(text):
        errors.append("含有裸脚注符号；请处理脚注内容后再导出")
    if mode == "fidelity" and not coverage_path:
        errors.append("精读模式需要逐讲覆盖表")
    if coverage_path and not Path(coverage_path).is_file():
        errors.append(f"覆盖表不存在：{coverage_path}")
    if "第一,被看见的收益" in text or "如果没有这项安排,那些人" in text:
        warnings.append("检测到旧式万能题干；请依据本讲内容重写结尾")

    spoken = render_spoken_text(text)
    number_or_english_lines = [
        line for line in spoken.splitlines() if len(re.findall(r"[A-Za-z0-9%]", line)) >= 8
    ]
    return {
        "errors": errors,
        "warnings": warnings,
        "title_count": title_count,
        "archive_chars": len(re.sub(r"\s+", "", text)),
        "spoken_chars": len(re.sub(r"\s+", "", spoken)),
        "dense_lines": number_or_english_lines,
        "spoken_text": spoken,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--mode", choices=("fidelity", "authored", "adaptation"), default="authored")
    parser.add_argument("--coverage", type=Path)
    parser.add_argument("--export-spoken", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    if not args.input.is_file():
        print(f"ERROR: input does not exist: {args.input}", file=sys.stderr)
        return 2
    result = analyze_text(
        args.input.read_text(encoding="utf-8"),
        mode=args.mode,
        coverage_path=str(args.coverage) if args.coverage else None,
    )
    if args.export_spoken:
        args.export_spoken.write_text(str(result["spoken_text"]) + "\n", encoding="utf-8")
    if args.json:
        printable = {key: value for key, value in result.items() if key != "spoken_text"}
        print(json.dumps(printable, ensure_ascii=False, indent=2))
    else:
        print(f"archive characters: {result['archive_chars']}")
        print(f"spoken characters: {result['spoken_chars']}")
        for line in result["dense_lines"]:
            print(f"REVIEW DENSE LINE: {line}")
        for warning in result["warnings"]:
            print(f"WARNING: {warning}")
        for error in result["errors"]:
            print(f"ERROR: {error}")
    return 1 if result["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

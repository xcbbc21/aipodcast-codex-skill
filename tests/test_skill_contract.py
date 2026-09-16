#!/usr/bin/env python3
"""Structural contract for the aipodcast skill entrypoint."""

from __future__ import annotations

import sys
from pathlib import Path


def require(text: str, phrase: str, errors: list[str]) -> None:
    if phrase not in text:
        errors.append(f"missing required guidance: {phrase}")


def forbid(text: str, phrase: str, errors: list[str]) -> None:
    if phrase in text:
        errors.append(f"contains retired fixed-template guidance: {phrase}")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: test_skill_contract.py PATH_TO_SKILL")
        return 2

    skill = Path(sys.argv[1])
    text = skill.read_text(encoding="utf-8")
    errors: list[str] = []

    require(text, "name: aipodcast", errors)
    require(text, "原书精读", errors)
    require(text, "逐讲覆盖表", errors)
    require(text, "双向语义复核", errors)
    require(text, "默认一个主思考问题", errors)
    require(text, "自然收束", errors)
    require(text, "上一讲回顾", errors)
    require(text, "第一讲不强行回顾", errors)
    require(text, "最小语义单元", errors)
    require(text, "存在待复核项时不得标记完成", errors)
    require(text, "疑似过度压缩", errors)
    require(text, "--no-rescript", errors)
    require(text, "references/fidelity-mode.md", errors)
    require(text, "references/narration-design.md", errors)

    forbid(text, "常规讲 **1800-2100 字**", errors)
    forbid(text, "末尾\"三个问题\"工具", errors)
    forbid(text, "每集约 6-8 分钟成品", errors)

    if errors:
        print("FAIL")
        for error in errors:
            print(f"- {error}")
        return 1

    print("PASS: skill contract satisfied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

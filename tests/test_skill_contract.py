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
    spoken_reference = skill.parent / "references" / "spoken-text.md"
    spoken_text = spoken_reference.read_text(encoding="utf-8")
    changelog = skill.parent / "CHANGELOG.md"
    readme = skill.parent / "README.md"
    errors: list[str] = []

    require(text, "name: aipodcast", errors)
    require(text, 'version: "1.2.1"', errors)
    require(text, "原书精读", errors)
    require(text, "逐讲覆盖表", errors)
    require(text, "双向语义复核", errors)
    require(text, "默认一个主思考问题", errors)
    require(text, "自然收束", errors)
    require(text, "上一讲回顾", errors)
    require(text, "第一讲不强行回顾", errors)
    require(text, "纯音频", errors)
    require(text, "不朗读图号", errors)
    require(text, "最小语义单元", errors)
    require(text, "存在待复核项时不得标记完成", errors)
    require(text, "疑似过度压缩", errors)
    require(text, "--no-rescript", errors)
    require(text, "references/fidelity-mode.md", errors)
    require(text, "references/narration-design.md", errors)
    require(spoken_text, "图表只是重复正文", errors)
    require(spoken_text, "独有信息", errors)
    require(spoken_text, "同步视频", errors)

    if not changelog.is_file():
        errors.append("missing CHANGELOG.md")
    else:
        changelog_text = changelog.read_text(encoding="utf-8")
        require(changelog_text, "## 1.2.1 - 2026-09-16", errors)

    if not readme.is_file():
        errors.append("missing README.md")
    else:
        readme_text = readme.read_text(encoding="utf-8")
        require(readme_text, "# aipodcast", errors)
        require(readme_text, "## 三种工作模式", errors)
        require(readme_text, "## 安装与更新", errors)
        require(readme_text, "## 纯音频中的图表处理", errors)
        require(readme_text, "check_tts_ready.py", errors)
        require(readme_text, "CHANGELOG.md", errors)
        require(readme_text, "v1.2.1", errors)

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

from __future__ import annotations

import subprocess
import tempfile
import unittest
from pathlib import Path

from scripts.check_audio import parse_duration_seconds
from scripts.check_tts_ready import analyze_text, render_spoken_text
from scripts.preflight import has_required_flags


class TtsReadyChecksTest(unittest.TestCase):
    def test_valid_document_has_one_title_and_no_hard_errors(self) -> None:
        text = "# 第一讲\n\n这是一段可直接朗读的正文。"
        result = analyze_text(text, mode="authored")
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["title_count"], 1)
        self.assertEqual(render_spoken_text(text), "这是一段可直接朗读的正文。")

    def test_fidelity_mode_requires_coverage_file_when_requested(self) -> None:
        text = "# 第一讲\n\n作者提出一个条件性结论。"
        result = analyze_text(text, mode="fidelity", coverage_path=None)
        self.assertIn("精读模式需要逐讲覆盖表", result["errors"])

    def test_fidelity_rejects_pending_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            coverage = Path(tmp) / "coverage.md"
            coverage.write_text("| U01 | 待复核 |\n", encoding="utf-8")
            result = analyze_text(
                "# 第一讲\n\n正文。", mode="fidelity", coverage_path=coverage
            )
            self.assertTrue(any("待复核" in item for item in result["errors"]))

    def test_fidelity_cli_flags_severe_unapproved_compression(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "source.md"
            script = root / "script.md"
            coverage = root / "coverage.md"
            source.write_text("原文内容。" * 300, encoding="utf-8")
            script.write_text("# 标题\n\n" + "口播内容。" * 30, encoding="utf-8")
            coverage.write_text("| U01 | 已核验 |\n", encoding="utf-8")
            checker = Path(__file__).parents[1] / "scripts" / "check_tts_ready.py"
            result = subprocess.run(
                [
                    "python3", str(checker), str(script), "--mode", "fidelity",
                    "--coverage", str(coverage), "--source", str(source),
                ],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("疑似过度压缩", result.stdout)

    def test_metadata_and_url_are_reported(self) -> None:
        text = "# 第一讲\n> 页码：10\n\n请访问 https://example.com。"
        result = analyze_text(text, mode="authored")
        self.assertTrue(any("元信息" in item for item in result["errors"]))
        self.assertTrue(any("URL" in item for item in result["errors"]))

    def test_audio_only_rejects_spoken_figure_numbers(self) -> None:
        text = "# 第三讲\n\n见图一之五，美元储备占比持续下降。"
        result = analyze_text(text, mode="authored")
        self.assertTrue(any("图表编号" in item for item in result["errors"]))

    def test_explicit_visual_mode_allows_figure_numbers(self) -> None:
        text = "# 第三讲\n\n请看图一之五，美元储备占比持续下降。"
        result = analyze_text(text, mode="authored", allow_visual_references=True)
        self.assertEqual(result["errors"], [])

    def test_audio_only_allows_semantic_chart_evidence_without_visual_navigation(self) -> None:
        text = "# 第三讲\n\n数据显示，美元储备占比从约百分之六十五降至百分之五十七。"
        result = analyze_text(text, mode="authored")
        self.assertEqual(result["errors"], [])


class AudioAndPreflightHelpersTest(unittest.TestCase):
    def test_duration_parser_accepts_afinfo_output(self) -> None:
        self.assertEqual(parse_duration_seconds("estimated duration: 12.500000 sec"), 12.5)

    def test_required_cli_flags_are_all_present(self) -> None:
        help_text = "--text --no-rescript --voice --language --no-progress"
        self.assertTrue(has_required_flags(help_text))
        self.assertFalse(has_required_flags("--text --voice --language"))


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import unittest

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

    def test_metadata_and_url_are_reported(self) -> None:
        text = "# 第一讲\n> 页码：10\n\n请访问 https://example.com。"
        result = analyze_text(text, mode="authored")
        self.assertTrue(any("元信息" in item for item in result["errors"]))
        self.assertTrue(any("URL" in item for item in result["errors"]))


class AudioAndPreflightHelpersTest(unittest.TestCase):
    def test_duration_parser_accepts_afinfo_output(self) -> None:
        self.assertEqual(parse_duration_seconds("estimated duration: 12.500000 sec"), 12.5)

    def test_required_cli_flags_are_all_present(self) -> None:
        help_text = "--text --no-rescript --voice --language --no-progress"
        self.assertTrue(has_required_flags(help_text))
        self.assertFalse(has_required_flags("--text --voice --language"))


if __name__ == "__main__":
    unittest.main()

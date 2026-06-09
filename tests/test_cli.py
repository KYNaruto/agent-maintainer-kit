from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.cli import main


class CliErrorHandlingTest(unittest.TestCase):
    def test_malformed_issue_json_returns_friendly_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            path.write_text('{"title":', encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                result = main(["triage", str(path)])

            self.assertEqual(result, 2)
            self.assertIn("amk: error:", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())

    def test_missing_transcript_returns_friendly_error(self) -> None:
        stderr = io.StringIO()

        with contextlib.redirect_stderr(stderr):
            result = main(["transcript", "/does/not/exist.jsonl"])

        self.assertEqual(result, 2)
        self.assertIn("amk: error:", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_invalid_policy_config_returns_friendly_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            config = Path(directory) / "amk.config.json"
            transcript = Path(directory) / "transcript.jsonl"
            config.write_text('{"policy":{"risky_command_regexes":"invalid"}}\n', encoding="utf-8")
            transcript.write_text('{"type":"note","message":"example"}\n', encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                result = main(["transcript", str(transcript), "--config", str(config)])

            self.assertEqual(result, 2)
            self.assertIn("policy values must be arrays", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()


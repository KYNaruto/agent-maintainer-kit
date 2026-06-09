from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.cli import main
from agent_maintainer_kit.constants import EXIT_CHECK_FAILED, EXIT_INPUT_ERROR, VERSION


class CliErrorHandlingTest(unittest.TestCase):
    def test_malformed_issue_json_returns_friendly_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            path.write_text('{"title":', encoding="utf-8")
            stderr = io.StringIO()

            with contextlib.redirect_stderr(stderr):
                result = main(["triage", str(path)])

            self.assertEqual(result, EXIT_INPUT_ERROR)
            self.assertIn("amk: error:", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())

    def test_missing_transcript_returns_friendly_error(self) -> None:
        stderr = io.StringIO()

        with contextlib.redirect_stderr(stderr):
            result = main(["transcript", "/does/not/exist.jsonl"])

        self.assertEqual(result, EXIT_INPUT_ERROR)
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

            self.assertEqual(result, EXIT_INPUT_ERROR)
            self.assertIn("policy values must be arrays", stderr.getvalue())
            self.assertNotIn("Traceback", stderr.getvalue())

    def test_version_option_reports_package_version(self) -> None:
        stdout = io.StringIO()

        with contextlib.redirect_stdout(stdout), self.assertRaises(SystemExit) as raised:
            main(["--version"])

        self.assertEqual(raised.exception.code, 0)
        self.assertEqual(stdout.getvalue().strip(), f"amk {VERSION}")

    def test_doctor_returns_check_failed_when_score_is_too_low(self) -> None:
        with tempfile.TemporaryDirectory() as directory, contextlib.redirect_stdout(io.StringIO()):
            result = main(["doctor", directory, "--min-score", "100"])

        self.assertEqual(result, EXIT_CHECK_FAILED)

    def test_transcript_returns_check_failed_when_risk_is_found(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            transcript = Path(directory) / "transcript.jsonl"
            transcript.write_text(
                '{"type":"command","command":"rm -rf build","status":"success"}\n',
                encoding="utf-8",
            )

            with contextlib.redirect_stdout(io.StringIO()):
                result = main(["transcript", str(transcript), "--fail-on-risk"])

        self.assertEqual(result, EXIT_CHECK_FAILED)


if __name__ == "__main__":
    unittest.main()

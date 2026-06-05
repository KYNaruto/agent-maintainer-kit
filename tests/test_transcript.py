from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.transcript import analyze_transcript


class TranscriptTest(unittest.TestCase):
    def test_detects_risky_commands_and_verification(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "transcript.jsonl"
            path.write_text(
                "\n".join(
                    [
                        '{"type":"command","command":"python -m unittest discover -s tests","status":"success"}',
                        '{"type":"command","command":"rm -rf build","status":"success"}',
                        '{"type":"edit","path":"src/example.py"}',
                    ]
                )
                + "\n",
                encoding="utf-8",
            )

            report = analyze_transcript(path)

            self.assertEqual(report.event_counts["command"], 2)
            self.assertEqual(report.edited_paths, ("src/example.py",))
            self.assertEqual(report.risky_commands, ("rm -rf build",))
            self.assertEqual(report.verification_commands, ("python -m unittest discover -s tests",))


if __name__ == "__main__":
    unittest.main()


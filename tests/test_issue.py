from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.issue import build_issue_triage_report, load_issue, triage_issue


class IssueTriageTest(unittest.TestCase):
    def test_triages_bug_with_traceback_as_high_priority(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            path.write_text(
                '{"title":"Crash when parsing transcript","body":"Traceback from json parser","labels":[]}\n',
                encoding="utf-8",
            )

            triage = triage_issue(load_issue(path))
            report = build_issue_triage_report(triage)

            self.assertEqual(triage.priority, "high")
            self.assertIn("bug", triage.suggested_labels)
            self.assertIn("Issue Triage Report", report)

    def test_triages_security_issue(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "issue.json"
            path.write_text(
                '{"title":"Token leak in report","body":"The report includes a secret token","labels":[]}\n',
                encoding="utf-8",
            )

            triage = triage_issue(load_issue(path))

            self.assertEqual(triage.priority, "high")
            self.assertIn("security", triage.suggested_labels)


if __name__ == "__main__":
    unittest.main()


from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.checks import run_repo_checks
from agent_maintainer_kit.reporting import build_json_report, build_markdown_report, build_release_checklist


class ReportingTest(unittest.TestCase):
    def test_builds_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            markdown = build_markdown_report(run_repo_checks(root))

            self.assertIn("# Agent Maintainer Report", markdown)
            self.assertIn("Repository Readiness", markdown)
            self.assertIn("readme", markdown)

    def test_builds_json_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            rendered = build_json_report(run_repo_checks(root))

            self.assertIn('"repository_readiness"', rendered)
            self.assertIn('"score"', rendered)

    def test_builds_release_checklist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            checklist = build_release_checklist(run_repo_checks(root), version="0.1.0")

            self.assertIn("# Release Readiness Checklist: 0.1.0", checklist)
            self.assertIn("Maintainer Sign-Off", checklist)


if __name__ == "__main__":
    unittest.main()

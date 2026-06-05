from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.checks import run_repo_checks
from agent_maintainer_kit.reporting import build_markdown_report


class ReportingTest(unittest.TestCase):
    def test_builds_markdown_report(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")

            markdown = build_markdown_report(run_repo_checks(root))

            self.assertIn("# Agent Maintainer Report", markdown)
            self.assertIn("Repository Readiness", markdown)
            self.assertIn("readme", markdown)


if __name__ == "__main__":
    unittest.main()


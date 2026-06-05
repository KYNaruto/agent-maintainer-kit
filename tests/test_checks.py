from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from agent_maintainer_kit.checks import run_repo_checks


class RepoChecksTest(unittest.TestCase):
    def test_scores_repository_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Example\n", encoding="utf-8")
            (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
            (root / "pyproject.toml").write_text("[project]\nname='example'\n", encoding="utf-8")

            report = run_repo_checks(root)

            self.assertGreaterEqual(report.score, 40)
            self.assertIn("ci", {check.name for check in report.failed_checks})


if __name__ == "__main__":
    unittest.main()


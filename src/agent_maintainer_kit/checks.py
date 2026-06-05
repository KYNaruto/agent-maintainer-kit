from __future__ import annotations

from pathlib import Path

from .models import CheckResult, RepoReport


def _exists_any(root: Path, names: tuple[str, ...]) -> bool:
    return any((root / name).exists() for name in names)


def _has_issue_template(root: Path) -> bool:
    return (
        (root / ".github" / "ISSUE_TEMPLATE").exists()
        or (root / ".github" / "ISSUE_TEMPLATE.md").exists()
        or (root / ".github" / "issues.yml").exists()
    )


def _has_ci(root: Path) -> bool:
    workflows = root / ".github" / "workflows"
    return workflows.exists() and any(workflows.glob("*.yml")) or any(workflows.glob("*.yaml"))


def run_repo_checks(root: str | Path) -> RepoReport:
    repo_root = Path(root).resolve()
    checks = (
        CheckResult(
            "readme",
            _exists_any(repo_root, ("README.md", "README.rst", "README")),
            "Repository has a README.",
            weight=2,
        ),
        CheckResult(
            "license",
            _exists_any(repo_root, ("LICENSE", "LICENSE.md", "COPYING")),
            "Repository declares an open-source license.",
            weight=2,
        ),
        CheckResult(
            "contributing",
            _exists_any(repo_root, ("CONTRIBUTING.md", ".github/CONTRIBUTING.md")),
            "Repository documents contribution expectations.",
        ),
        CheckResult(
            "code_of_conduct",
            _exists_any(repo_root, ("CODE_OF_CONDUCT.md", ".github/CODE_OF_CONDUCT.md")),
            "Repository has a code of conduct.",
        ),
        CheckResult(
            "package_metadata",
            _exists_any(repo_root, ("pyproject.toml", "package.json", "Cargo.toml", "go.mod")),
            "Repository exposes package or project metadata.",
            weight=2,
        ),
        CheckResult(
            "ci",
            _has_ci(repo_root),
            "Repository has GitHub Actions workflow files.",
            weight=2,
        ),
        CheckResult(
            "issue_template",
            _has_issue_template(repo_root),
            "Repository has an issue template for triage.",
        ),
    )
    return RepoReport(root=repo_root, checks=checks)


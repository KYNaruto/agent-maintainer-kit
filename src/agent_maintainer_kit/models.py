from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    message: str
    weight: int = 1


@dataclass(frozen=True)
class RepoReport:
    root: Path
    checks: tuple[CheckResult, ...]

    @property
    def score(self) -> int:
        total = sum(check.weight for check in self.checks)
        if total == 0:
            return 0
        earned = sum(check.weight for check in self.checks if check.passed)
        return round((earned / total) * 100)

    @property
    def failed_checks(self) -> tuple[CheckResult, ...]:
        return tuple(check for check in self.checks if not check.passed)


@dataclass(frozen=True)
class CommandEvent:
    command: str
    status: str | None = None


@dataclass(frozen=True)
class TranscriptReport:
    path: Path
    event_counts: dict[str, int] = field(default_factory=dict)
    commands: tuple[CommandEvent, ...] = ()
    edited_paths: tuple[str, ...] = ()
    findings: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    risky_commands: tuple[str, ...] = ()

    @property
    def verification_commands(self) -> tuple[str, ...]:
        markers = ("test", "pytest", "unittest", "npm test", "yarn test", "cargo test", "go test")
        return tuple(
            event.command for event in self.commands if any(marker in event.command for marker in markers)
        )


from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DEFAULT_RISKY_COMMAND_REGEXES = (
    r"\brm\s+-rf\b",
    r"\bgit\s+reset\s+--hard\b",
    r"\bgit\s+clean\s+-fd",
    r"\bsudo\b",
    r">\s*/dev/(disk|rdisk)",
    r"\bchmod\s+-R\s+777\b",
)


@dataclass(frozen=True)
class Policy:
    risky_command_regexes: tuple[str, ...] = DEFAULT_RISKY_COMMAND_REGEXES

    def compiled_risky_command_regexes(self) -> tuple[re.Pattern[str], ...]:
        return tuple(re.compile(pattern) for pattern in self.risky_command_regexes)


def _as_string_tuple(value: Any) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list):
        raise ValueError("policy values must be arrays")
    return tuple(str(item) for item in value if str(item).strip())


def load_policy(path: str | Path | None = None) -> Policy:
    if path is None:
        return Policy()

    config_path = Path(path).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    if not isinstance(config, dict):
        raise ValueError(f"{config_path}: config must be a JSON object")

    policy_data = config.get("policy", {})
    if not isinstance(policy_data, dict):
        raise ValueError(f"{config_path}: policy must be a JSON object")

    literal_commands = _as_string_tuple(policy_data.get("risky_commands"))
    regex_commands = _as_string_tuple(policy_data.get("risky_command_regexes"))
    patterns = tuple(re.escape(command) for command in literal_commands) + regex_commands

    if not patterns:
        return Policy()

    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"{config_path}: invalid risky command regex {pattern!r}: {exc}") from exc

    return Policy(risky_command_regexes=patterns)


def discover_policy_path(repo_root: str | Path) -> Path | None:
    path = Path(repo_root).resolve() / "amk.config.json"
    return path if path.exists() else None


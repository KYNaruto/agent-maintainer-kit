from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import CommandEvent, TranscriptReport
from .policy import Policy, load_policy


def _is_risky_command(command: str, policy: Policy) -> bool:
    return any(pattern.search(command) for pattern in policy.compiled_risky_command_regexes())


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            event = json.loads(stripped)
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: invalid JSONL event: {exc}") from exc
        if not isinstance(event, dict):
            raise ValueError(f"{path}:{line_number}: event must be a JSON object")
        events.append(event)
    return events


def analyze_transcript(path: str | Path, policy: Policy | None = None) -> TranscriptReport:
    active_policy = policy or load_policy()
    transcript_path = Path(path).resolve()
    events = _read_jsonl(transcript_path)
    counts: dict[str, int] = {}
    commands: list[CommandEvent] = []
    edited_paths: list[str] = []
    findings: list[str] = []
    notes: list[str] = []
    risky_commands: list[str] = []

    for event in events:
        event_type = str(event.get("type", "unknown"))
        counts[event_type] = counts.get(event_type, 0) + 1

        if event_type == "command":
            command = str(event.get("command", ""))
            if command:
                commands.append(CommandEvent(command=command, status=event.get("status")))
                if _is_risky_command(command, active_policy):
                    risky_commands.append(command)
        elif event_type == "edit":
            path_value = event.get("path")
            if path_value:
                edited_paths.append(str(path_value))
        elif event_type == "finding":
            message = event.get("message") or event.get("title")
            if message:
                findings.append(str(message))
        elif event_type in {"note", "test"}:
            message = event.get("message") or event.get("name")
            if message:
                notes.append(str(message))

    return TranscriptReport(
        path=transcript_path,
        event_counts=counts,
        commands=tuple(commands),
        edited_paths=tuple(dict.fromkeys(edited_paths)),
        findings=tuple(findings),
        notes=tuple(notes),
        risky_commands=tuple(risky_commands),
    )

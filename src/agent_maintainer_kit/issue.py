from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class IssueInput:
    title: str
    body: str
    labels: tuple[str, ...] = ()


@dataclass(frozen=True)
class IssueTriage:
    issue: IssueInput
    suggested_labels: tuple[str, ...]
    priority: str
    maintainer_questions: tuple[str, ...]
    response_template: str


BUG_MARKERS = ("bug", "crash", "error", "exception", "traceback", "fails", "broken")
FEATURE_MARKERS = ("feature", "request", "support", "add", "enhancement")
SECURITY_MARKERS = ("security", "vulnerability", "exploit", "secret", "token", "injection")
DOC_MARKERS = ("docs", "documentation", "readme", "example")


def load_issue(path: str | Path) -> IssueInput:
    issue_path = Path(path).resolve()
    payload = json.loads(issue_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{issue_path}: issue input must be a JSON object")

    title = str(payload.get("title", "")).strip()
    body = str(payload.get("body", "")).strip()
    raw_labels = payload.get("labels", [])
    if not isinstance(raw_labels, list):
        raise ValueError(f"{issue_path}: labels must be an array")
    labels = tuple(str(label).strip() for label in raw_labels if str(label).strip())

    if not title:
        raise ValueError(f"{issue_path}: title is required")

    return IssueInput(title=title, body=body, labels=labels)


def _contains_any(text: str, markers: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(marker in lowered for marker in markers)


def triage_issue(issue: IssueInput) -> IssueTriage:
    text = f"{issue.title}\n{issue.body}"
    labels = set(issue.labels)

    if _contains_any(text, SECURITY_MARKERS):
        labels.add("security")
    if _contains_any(text, BUG_MARKERS):
        labels.add("bug")
    if _contains_any(text, FEATURE_MARKERS):
        labels.add("enhancement")
    if _contains_any(text, DOC_MARKERS):
        labels.add("documentation")

    if "security" in labels:
        priority = "high"
    elif "bug" in labels and ("traceback" in text.lower() or "crash" in text.lower()):
        priority = "high"
    elif "bug" in labels:
        priority = "medium"
    else:
        priority = "normal"

    questions: list[str] = []
    if "bug" in labels:
        questions.extend(
            [
                "Can you provide exact reproduction steps?",
                "What version and environment did this happen on?",
                "Can you include the full command output or traceback?",
            ]
        )
    if "enhancement" in labels:
        questions.append("What maintainer workflow would this improve?")
    if "security" in labels:
        questions.append("Can you share sensitive exploit details privately instead of posting them publicly?")
    if not questions:
        questions.append("What outcome would make this issue resolved?")

    response_template = _build_response_template(labels, priority, questions)
    return IssueTriage(
        issue=issue,
        suggested_labels=tuple(sorted(labels)),
        priority=priority,
        maintainer_questions=tuple(questions),
        response_template=response_template,
    )


def _build_response_template(labels: set[str], priority: str, questions: list[str]) -> str:
    label_text = ", ".join(sorted(labels)) if labels else "needs-triage"
    lines = [
        "Thanks for the report. I triaged this with Agent Maintainer Kit.",
        "",
        f"- Suggested labels: `{label_text}`",
        f"- Suggested priority: `{priority}`",
        "",
        "Maintainer follow-up:",
    ]
    lines.extend(f"- {question}" for question in questions)
    lines.append("")
    return "\n".join(lines)


def build_issue_triage_report(triage: IssueTriage) -> str:
    lines = [
        "# Issue Triage Report",
        "",
        f"Title: {triage.issue.title}",
        f"Suggested priority: **{triage.priority}**",
        "",
        "## Suggested Labels",
        "",
    ]
    if triage.suggested_labels:
        lines.extend(f"- `{label}`" for label in triage.suggested_labels)
    else:
        lines.append("- `needs-triage`")

    lines.extend(["", "## Maintainer Questions", ""])
    lines.extend(f"- {question}" for question in triage.maintainer_questions)
    lines.extend(["", "## Response Template", "", triage.response_template])
    return "\n".join(lines)


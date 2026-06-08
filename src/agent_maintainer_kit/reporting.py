from __future__ import annotations

import json
from datetime import UTC, datetime

from .models import RepoReport, TranscriptReport


def _status(value: bool) -> str:
    return "PASS" if value else "FAIL"


def build_markdown_report(
    repo_report: RepoReport,
    transcript_report: TranscriptReport | None = None,
) -> str:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    lines: list[str] = [
        "# Agent Maintainer Report",
        "",
        f"Generated: {generated_at}",
        f"Repository: `{repo_report.root}`",
        "",
        "## Repository Readiness",
        "",
        f"Score: **{repo_report.score}/100**",
        "",
        "| Check | Status | Detail |",
        "| --- | --- | --- |",
    ]

    for check in repo_report.checks:
        lines.append(f"| {check.name} | {_status(check.passed)} | {check.message} |")

    if repo_report.failed_checks:
        lines.extend(["", "### Recommended Fixes", ""])
        for check in repo_report.failed_checks:
            lines.append(f"- `{check.name}`: {check.message}")

    if transcript_report is not None:
        lines.extend(
            [
                "",
                "## Agent Transcript",
                "",
                f"Transcript: `{transcript_report.path}`",
                "",
                "### Event Counts",
                "",
            ]
        )
        for event_type, count in sorted(transcript_report.event_counts.items()):
            lines.append(f"- `{event_type}`: {count}")

        lines.extend(["", "### Commands", ""])
        if transcript_report.commands:
            for command in transcript_report.commands:
                suffix = f" ({command.status})" if command.status else ""
                lines.append(f"- `{command.command}`{suffix}")
        else:
            lines.append("- No commands recorded.")

        lines.extend(["", "### Verification", ""])
        if transcript_report.verification_commands:
            for command in transcript_report.verification_commands:
                lines.append(f"- `{command}`")
        else:
            lines.append("- No test or verification command detected.")

        lines.extend(["", "### Risk Review", ""])
        if transcript_report.risky_commands:
            for command in transcript_report.risky_commands:
                lines.append(f"- Review risky command: `{command}`")
        else:
            lines.append("- No risky command patterns detected.")

        if transcript_report.edited_paths:
            lines.extend(["", "### Edited Paths", ""])
            for path in transcript_report.edited_paths:
                lines.append(f"- `{path}`")

        if transcript_report.findings:
            lines.extend(["", "### Findings", ""])
            for finding in transcript_report.findings:
                lines.append(f"- {finding}")

    lines.append("")
    return "\n".join(lines)


def build_json_report(
    repo_report: RepoReport,
    transcript_report: TranscriptReport | None = None,
) -> str:
    payload: dict[str, object] = {
        "generated_at": datetime.now(UTC).isoformat(),
        "repository": str(repo_report.root),
        "repository_readiness": {
            "score": repo_report.score,
            "checks": [
                {
                    "name": check.name,
                    "passed": check.passed,
                    "message": check.message,
                    "weight": check.weight,
                }
                for check in repo_report.checks
            ],
        },
    }

    if transcript_report is not None:
        payload["transcript"] = {
            "path": str(transcript_report.path),
            "event_counts": transcript_report.event_counts,
            "commands": [
                {"command": event.command, "status": event.status}
                for event in transcript_report.commands
            ],
            "edited_paths": list(transcript_report.edited_paths),
            "findings": list(transcript_report.findings),
            "notes": list(transcript_report.notes),
            "risky_commands": list(transcript_report.risky_commands),
            "verification_commands": list(transcript_report.verification_commands),
        }

    return json.dumps(payload, indent=2, sort_keys=True)


def build_release_checklist(
    repo_report: RepoReport,
    transcript_report: TranscriptReport | None = None,
    version: str | None = None,
) -> str:
    generated_at = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
    title = f"# Release Readiness Checklist: {version}" if version else "# Release Readiness Checklist"
    lines = [
        title,
        "",
        f"Generated: {generated_at}",
        f"Repository: `{repo_report.root}`",
        "",
        "## Required Gates",
        "",
        f"- [{'x' if repo_report.score >= 90 else ' '}] Repository readiness score is at least 90.",
        f"- [{'x' if not repo_report.failed_checks else ' '}] Required repository checks pass.",
    ]

    if transcript_report is not None:
        lines.extend(
            [
                f"- [{'x' if transcript_report.verification_commands else ' '}] Verification commands are recorded.",
                f"- [{'x' if not transcript_report.risky_commands else ' '}] No risky command patterns are present.",
            ]
        )
    else:
        lines.extend(
            [
                "- [ ] Verification transcript is attached.",
                "- [ ] Risk review has been completed.",
            ]
        )

    lines.extend(["", "## Repository Checks", ""])
    for check in repo_report.checks:
        lines.append(f"- [{'x' if check.passed else ' '}] `{check.name}`: {check.message}")

    if transcript_report is not None:
        lines.extend(["", "## Verification Commands", ""])
        if transcript_report.verification_commands:
            for command in transcript_report.verification_commands:
                lines.append(f"- `{command}`")
        else:
            lines.append("- No verification command detected.")

        lines.extend(["", "## Risk Review", ""])
        if transcript_report.risky_commands:
            for command in transcript_report.risky_commands:
                lines.append(f"- Review required: `{command}`")
        else:
            lines.append("- No risky command patterns detected.")

        if transcript_report.findings:
            lines.extend(["", "## Findings", ""])
            for finding in transcript_report.findings:
                lines.append(f"- {finding}")

    lines.extend(
        [
            "",
            "## Maintainer Sign-Off",
            "",
            "- [ ] Changelog or release notes are prepared.",
            "- [ ] Documentation changes are included when behavior changed.",
            "- [ ] Final maintainer review is complete.",
            "",
        ]
    )
    return "\n".join(lines)


def build_review_comment(
    repo_report: RepoReport,
    transcript_report: TranscriptReport | None = None,
) -> str:
    readiness = "ready" if repo_report.score >= 90 and not repo_report.failed_checks else "needs review"
    lines = [
        "## Agent Maintainer Kit Review",
        "",
        f"Repository readiness: **{repo_report.score}/100** ({readiness})",
        "",
    ]

    if repo_report.failed_checks:
        lines.extend(["### Repository Gaps", ""])
        for check in repo_report.failed_checks:
            lines.append(f"- `{check.name}`: {check.message}")
        lines.append("")

    if transcript_report is not None:
        lines.extend(["### Agent Session", ""])
        lines.append(f"- Commands recorded: `{len(transcript_report.commands)}`")
        lines.append(f"- Edited paths: `{len(transcript_report.edited_paths)}`")
        lines.append(f"- Findings: `{len(transcript_report.findings)}`")
        lines.append("")

        lines.extend(["### Verification", ""])
        if transcript_report.verification_commands:
            for command in transcript_report.verification_commands:
                lines.append(f"- `{command}`")
        else:
            lines.append("- No verification command detected.")
        lines.append("")

        lines.extend(["### Risk Review", ""])
        if transcript_report.risky_commands:
            for command in transcript_report.risky_commands:
                lines.append(f"- Maintainer review required: `{command}`")
        else:
            lines.append("- No risky command patterns detected.")
        lines.append("")
    else:
        lines.extend(
            [
                "### Agent Session",
                "",
                "- No transcript attached.",
                "",
            ]
        )

    lines.extend(
        [
            "### Maintainer Action Items",
            "",
            "- [ ] Confirm the summary matches the change.",
            "- [ ] Confirm verification is sufficient for the risk of the change.",
            "- [ ] Confirm risky commands, if any, were intentional and reviewed.",
            "",
        ]
    )
    return "\n".join(lines)

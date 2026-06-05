from __future__ import annotations

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


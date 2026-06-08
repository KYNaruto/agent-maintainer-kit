from __future__ import annotations

import argparse
import json
from pathlib import Path

from .checks import run_repo_checks
from .policy import discover_policy_path, load_policy
from .reporting import build_json_report, build_markdown_report, build_release_checklist, build_review_comment
from .transcript import analyze_transcript


DEFAULT_CONFIG = {
    "project": "agent-maintainer-kit",
    "checks": {
        "require_readme": True,
        "require_license": True,
        "require_ci": True,
        "require_issue_template": True,
    },
    "policy": {
        "risky_commands": ["rm -rf", "git reset --hard", "sudo", "chmod -R 777"],
        "risky_command_regexes": ["curl .+ \\\\| sh", "git push --force"],
    },
}

EXAMPLE_TASK = {
    "title": "Review dependency update",
    "goal": "Use an agent to inspect a dependency update, run tests, and produce a maintainer report.",
    "required_checks": ["readme", "license", "ci"],
    "expected_outputs": ["summary", "risk_review", "verification_commands"],
}


def _write_json(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    root.mkdir(parents=True, exist_ok=True)
    config_path = root / "amk.config.json"
    task_dir = root / ".amk" / "tasks"
    task_dir.mkdir(parents=True, exist_ok=True)

    if not config_path.exists() or args.force:
        _write_json(config_path, DEFAULT_CONFIG)
    task_path = task_dir / "review-dependency-update.json"
    if not task_path.exists() or args.force:
        _write_json(task_path, EXAMPLE_TASK)

    print(f"Initialized Agent Maintainer Kit files in {root}")
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    report = run_repo_checks(args.path)
    print(f"Repository: {report.root}")
    print(f"Score: {report.score}/100")
    for check in report.checks:
        marker = "PASS" if check.passed else "FAIL"
        print(f"{marker} {check.name}: {check.message}")
    return 0 if report.score >= args.min_score else 1


def cmd_transcript(args: argparse.Namespace) -> int:
    policy = load_policy(args.config) if args.config else load_policy()
    report = analyze_transcript(args.path, policy=policy)
    print(f"Transcript: {report.path}")
    print("Event counts:")
    for event_type, count in sorted(report.event_counts.items()):
        print(f"  {event_type}: {count}")
    print(f"Commands: {len(report.commands)}")
    print(f"Edited paths: {len(report.edited_paths)}")
    print(f"Risky commands: {len(report.risky_commands)}")
    if report.risky_commands:
        for command in report.risky_commands:
            print(f"  REVIEW: {command}")
    return 1 if report.risky_commands and args.fail_on_risk else 0


def cmd_report(args: argparse.Namespace) -> int:
    repo_report = run_repo_checks(args.path)
    policy_path = Path(args.config).resolve() if args.config else discover_policy_path(args.path)
    policy = load_policy(policy_path) if policy_path else load_policy()
    transcript_report = analyze_transcript(args.transcript, policy=policy) if args.transcript else None
    rendered = (
        build_json_report(repo_report, transcript_report)
        if args.format == "json"
        else build_markdown_report(repo_report, transcript_report)
    )
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(rendered)
    return 0


def cmd_release(args: argparse.Namespace) -> int:
    repo_report = run_repo_checks(args.path)
    policy_path = Path(args.config).resolve() if args.config else discover_policy_path(args.path)
    policy = load_policy(policy_path) if policy_path else load_policy()
    transcript_report = analyze_transcript(args.transcript, policy=policy) if args.transcript else None
    checklist = build_release_checklist(repo_report, transcript_report, version=args.version)
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.write_text(checklist, encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(checklist)
    return 0


def cmd_comment(args: argparse.Namespace) -> int:
    repo_report = run_repo_checks(args.path)
    policy_path = Path(args.config).resolve() if args.config else discover_policy_path(args.path)
    policy = load_policy(policy_path) if policy_path else load_policy()
    transcript_report = analyze_transcript(args.transcript, policy=policy) if args.transcript else None
    comment = build_review_comment(repo_report, transcript_report)
    if args.output:
        output_path = Path(args.output).resolve()
        output_path.write_text(comment, encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(comment)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="amk",
        description="Agent-ready OSS maintenance checks and reports.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create starter config and task files.")
    init_parser.add_argument("path", nargs="?", default=".")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing starter files.")
    init_parser.set_defaults(func=cmd_init)

    doctor_parser = subparsers.add_parser("doctor", help="Run repository readiness checks.")
    doctor_parser.add_argument("path", nargs="?", default=".")
    doctor_parser.add_argument("--min-score", type=int, default=70)
    doctor_parser.set_defaults(func=cmd_doctor)

    transcript_parser = subparsers.add_parser("transcript", help="Analyze an agent JSONL transcript.")
    transcript_parser.add_argument("path")
    transcript_parser.add_argument("--config", help="Path to amk.config.json policy config.")
    transcript_parser.add_argument("--fail-on-risk", action="store_true")
    transcript_parser.set_defaults(func=cmd_transcript)

    report_parser = subparsers.add_parser("report", help="Generate a maintainer report.")
    report_parser.add_argument("path", nargs="?", default=".")
    report_parser.add_argument("--transcript")
    report_parser.add_argument("--config", help="Path to amk.config.json policy config.")
    report_parser.add_argument("--output")
    report_parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    report_parser.set_defaults(func=cmd_report)

    release_parser = subparsers.add_parser("release", help="Generate a release readiness checklist.")
    release_parser.add_argument("path", nargs="?", default=".")
    release_parser.add_argument("--transcript")
    release_parser.add_argument("--config", help="Path to amk.config.json policy config.")
    release_parser.add_argument("--version")
    release_parser.add_argument("--output")
    release_parser.set_defaults(func=cmd_release)

    comment_parser = subparsers.add_parser("comment", help="Generate a PR or issue review comment.")
    comment_parser.add_argument("path", nargs="?", default=".")
    comment_parser.add_argument("--transcript")
    comment_parser.add_argument("--config", help="Path to amk.config.json policy config.")
    comment_parser.add_argument("--output")
    comment_parser.set_defaults(func=cmd_comment)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)

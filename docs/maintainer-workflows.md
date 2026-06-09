# Maintainer Workflows

Agent Maintainer Kit supports repeatable workflows around coding agents.

## GitHub Actions Automation

The `Maintainer Report` workflow can be started manually from GitHub Actions. It generates maintainer artifacts that can be downloaded and attached to PR review or release notes:

- `maintainer-report.md`
- `maintainer-report.json`
- `review-comment.md`
- `release-checklist.md`

## PR Review Preparation

1. Run an agent session for a PR.
2. Export the session as JSONL transcript events.
3. Run `amk transcript`.
4. Run `amk report` and attach the report to the PR review notes.
5. Run `amk comment` to draft a concise PR or issue comment.

The maintainer can quickly see commands, edited paths, findings, verification commands, and risky command patterns.

```bash
amk comment . --transcript agent-session.jsonl --output review-comment.md
```

## Policy Configuration

Create an `amk.config.json` file to define project-specific risk rules:

```json
{
  "policy": {
    "risky_commands": ["git push --force"],
    "risky_command_regexes": ["curl .+ \\\\| sh"]
  }
}
```

Then run:

```bash
amk transcript agent-session.jsonl --config amk.config.json --fail-on-risk
```

## Issue Triage

Use `.amk/tasks/*.json` files to define repeatable agent tasks. A task should include the goal, expected outputs, and required checks.

This keeps agent sessions focused and gives contributors a clear path from issue report to maintainable output.

For issue-style JSON input, run:

```bash
amk triage examples/issue.json --output issue-triage.md
amk triage examples/issue.json --format json --output issue-triage.json
```

The Markdown report is suitable for maintainer review. The JSON report exposes the same suggested labels, priority, maintainer questions, and response template for CI or GitHub automation.

## Release Preparation

Before a release:

```bash
amk doctor .
amk report . --transcript release-session.jsonl --output release-maintainer-report.md
amk report . --transcript release-session.jsonl --format json --output release-maintainer-report.json
amk comment . --transcript release-session.jsonl --output release-review-comment.md
amk release . --transcript release-session.jsonl --version 0.1.0 --output release-checklist.md
```

The generated report can be used as a release checklist and review artifact.

## Security Review

`amk` flags commands that commonly require human review, such as destructive filesystem operations, hard git resets, broad permission changes, and privileged execution.

The tool does not execute transcript commands. It only reads transcript data and generates review output.

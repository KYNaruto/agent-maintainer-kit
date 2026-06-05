# Maintainer Workflows

Agent Maintainer Kit supports repeatable workflows around coding agents.

## PR Review Preparation

1. Run an agent session for a PR.
2. Export the session as JSONL transcript events.
3. Run `amk transcript`.
4. Run `amk report` and attach the report to the PR review notes.

The maintainer can quickly see commands, edited paths, findings, verification commands, and risky command patterns.

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

## Release Preparation

Before a release:

```bash
amk doctor .
amk report . --transcript release-session.jsonl --output release-maintainer-report.md
amk report . --transcript release-session.jsonl --format json --output release-maintainer-report.json
```

The generated report can be used as a release checklist and review artifact.

## Security Review

`amk` flags commands that commonly require human review, such as destructive filesystem operations, hard git resets, broad permission changes, and privileged execution.

The tool does not execute transcript commands. It only reads transcript data and generates review output.

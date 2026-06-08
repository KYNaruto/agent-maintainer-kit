# Agent Maintainer Kit

Agent Maintainer Kit (`amk`) is a framework-agnostic CLI for open-source maintainers who use coding agents in real repository workflows.

It helps maintainers answer practical questions before letting an agent touch a project:

- Is this repository ready for agent-assisted review, triage, and release work?
- Are required OSS files present and discoverable?
- Did an agent run use risky shell commands or skip verification?
- What should be included in a maintainer-facing activity report?

The project is intentionally dependency-free at runtime. It can run in constrained CI environments, local sandboxes, and repository checkouts without requiring a hosted agent platform.

## Maintainer Automation

The repository includes a manual GitHub Actions workflow, `Maintainer Report`, that generates maintainer artifacts from the example transcript:

- `maintainer-report.md`
- `maintainer-report.json`
- `review-comment.md`
- `release-checklist.md`

This workflow is intended as a template for OSS maintainers who want auditable agent-assisted PR review and release preparation.

Version tags also trigger a release workflow that tests the project, builds a wheel, generates a release checklist, and creates a GitHub Release.

## Maintainer Workflows

`amk` is designed for maintainers who want agent support without losing review discipline. It focuses on the maintenance work that is usually repetitive but still needs accountability:

- PR review preparation: summarize changed files, commands, tests, and findings from an agent session.
- Issue triage: define repeatable task specs that guide agents toward actionable maintainer notes.
- Release readiness: confirm that documentation, license, CI, and contribution surfaces are present.
- Security review: flag destructive shell commands and missing verification before a maintainer signs off.
- Project health reporting: generate Markdown reports that can be attached to PRs, releases, or maintainer logs.

## Features

- Repository readiness checks for README, license, package metadata, CI, issue templates, and contribution docs.
- Agent transcript analysis from JSONL event logs.
- Command risk detection for destructive shell patterns.
- Markdown report generation for PR review notes, release preparation, and maintainer logs.
- Release readiness checklist generation for maintainer sign-off.
- PR and issue review comment generation for maintainer automation.
- Issue triage reports with suggested labels, priority, and maintainer follow-up questions.
- `init` command that creates a starter `amk.config.json` and example task spec.

## Install

From a checkout:

```bash
python3 -m pip install -e .
```

Run directly without installing:

```bash
PYTHONPATH=src python3 -m agent_maintainer_kit --help
```

## Quick Start

Create a starter config in a repository:

```bash
amk init /path/to/repo
```

Run repository checks:

```bash
amk doctor /path/to/repo
```

Analyze an agent transcript:

```bash
amk transcript examples/transcript.jsonl
```

Analyze with a custom policy config:

```bash
amk transcript examples/transcript.jsonl --config examples/amk.config.json --fail-on-risk
```

Generate a combined maintainer report:

```bash
amk report /path/to/repo --transcript examples/transcript.jsonl --output maintainer-report.md
```

Generate machine-readable JSON for CI or custom dashboards:

```bash
amk report /path/to/repo --transcript examples/transcript.jsonl --format json --output maintainer-report.json
```

Generate a release readiness checklist:

```bash
amk release /path/to/repo --transcript examples/transcript.jsonl --version 0.1.0 --output release-checklist.md
```

Generate a PR or issue review comment:

```bash
amk comment /path/to/repo --transcript examples/transcript.jsonl --output review-comment.md
```

Generate an issue triage report:

```bash
amk triage examples/issue.json --output issue-triage.md
```

## Example Output

```text
Repository: /path/to/repo
Score: 100/100
PASS readme: Repository has a README.
PASS license: Repository declares an open-source license.
PASS ci: Repository has GitHub Actions workflow files.
PASS issue_template: Repository has an issue template for triage.
```

## Transcript Format

`amk` expects JSON Lines. Each line is one event:

```json
{"type":"command","command":"python -m pytest","status":"success"}
{"type":"edit","path":"src/example.py"}
{"type":"note","message":"Reviewed failing test and updated parser."}
```

Supported event types are `command`, `edit`, `note`, `test`, and `finding`. Unknown event types are preserved in counts but ignored by specialized analyzers.

## Policy Configuration

`amk.config.json` lets maintainers tune command-risk detection for their project:

```json
{
  "policy": {
    "risky_commands": ["rm -rf", "git reset --hard", "sudo"],
    "risky_command_regexes": ["curl .+ \\\\| sh", "git push --force"]
  }
}
```

`risky_commands` are treated as literal command fragments. `risky_command_regexes` are regular expressions for teams that need broader matching.

## Why This Exists

Agent-assisted OSS work is most useful when it reduces invisible maintainer load: PR review, issue triage, release preparation, documentation updates, test generation, and security review. Those workflows need repeatable checks and clear reports, not just one-off chat transcripts.

Agent Maintainer Kit provides a small, auditable layer that maintainers can run before and after agent sessions.

## OpenAI Codex Use Cases

This project is a natural fit for Codex-assisted open-source maintenance:

- Use Codex to review incoming PRs and convert agent transcripts into maintainer-facing reports.
- Use Codex to draft PR and issue comments that preserve maintainer review checkpoints.
- Use Codex to triage issues into labels, priority, and maintainer follow-up questions.
- Use Codex to generate tests for policy checks, transcript parsing, and report rendering.
- Use Codex to inspect risky agent command patterns and propose safer alternatives.
- Use Codex to draft release notes and documentation updates from structured activity logs.
- Use API credits to automate repository health reports for OSS maintainers at review time.

## Roadmap

- Configurable policy packs for different project types.
- GitHub issue and PR summary adapters.
- SARIF export for security-oriented findings.
- Release-note generation from agent and git activity.
- Optional OpenAI/Codex integration for maintainers who want hosted model workflows.

## Documentation

- [Maintainer workflows](docs/maintainer-workflows.md)
- [Policy configuration](docs/policy.md)
- [Release process](docs/releasing.md)
- [Codex for OSS application notes](docs/codex-for-oss.md)
- [Codex for OSS application packet](docs/application-packet.md)
- [Changelog](CHANGELOG.md)
- [Maintainers](MAINTAINERS.md)
- [Support](SUPPORT.md)

## License

MIT

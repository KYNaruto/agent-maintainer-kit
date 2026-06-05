# Agent Maintainer Kit

Agent Maintainer Kit (`amk`) is a framework-agnostic CLI for open-source maintainers who use coding agents in real repository workflows.

It helps maintainers answer practical questions before letting an agent touch a project:

- Is this repository ready for agent-assisted review, triage, and release work?
- Are required OSS files present and discoverable?
- Did an agent run use risky shell commands or skip verification?
- What should be included in a maintainer-facing activity report?

The project is intentionally dependency-free at runtime. It can run in constrained CI environments, local sandboxes, and repository checkouts without requiring a hosted agent platform.

## Features

- Repository readiness checks for README, license, package metadata, CI, issue templates, and contribution docs.
- Agent transcript analysis from JSONL event logs.
- Command risk detection for destructive shell patterns.
- Markdown report generation for PR review notes, release preparation, and maintainer logs.
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

Generate a combined maintainer report:

```bash
amk report /path/to/repo --transcript examples/transcript.jsonl --output maintainer-report.md
```

## Transcript Format

`amk` expects JSON Lines. Each line is one event:

```json
{"type":"command","command":"python -m pytest","status":"success"}
{"type":"edit","path":"src/example.py"}
{"type":"note","message":"Reviewed failing test and updated parser."}
```

Supported event types are `command`, `edit`, `note`, `test`, and `finding`. Unknown event types are preserved in counts but ignored by specialized analyzers.

## Why This Exists

Agent-assisted OSS work is most useful when it reduces invisible maintainer load: PR review, issue triage, release preparation, documentation updates, test generation, and security review. Those workflows need repeatable checks and clear reports, not just one-off chat transcripts.

Agent Maintainer Kit provides a small, auditable layer that maintainers can run before and after agent sessions.

## Roadmap

- Configurable policy packs for different project types.
- GitHub issue and PR summary adapters.
- SARIF export for security-oriented findings.
- Release-note generation from agent and git activity.
- Optional OpenAI/Codex integration for maintainers who want hosted model workflows.

## License

MIT

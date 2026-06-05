# Security Policy

Agent Maintainer Kit is designed to inspect maintainer workflows and agent transcripts. It should never execute commands found in a transcript.

## Supported Versions

The current `main` branch receives security fixes.

## Reporting a Vulnerability

Please open a GitHub issue with the `security` label if the report does not contain sensitive details. For sensitive reports, contact the maintainer privately before publishing exploit details.

Useful reports include:

- A transcript input that causes incorrect risk classification.
- A command pattern that should be flagged but is missed.
- A path, parsing, or report-rendering issue that could mislead maintainers.

## Security Principles

- Parse transcript data as untrusted input.
- Do not execute transcript commands.
- Keep risky command detection conservative.
- Prefer transparent reports over hidden scoring.


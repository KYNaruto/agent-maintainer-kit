# Roadmap

Agent Maintainer Kit is focused on helping open-source maintainers adopt coding agents safely and repeatably.

For the ordered milestone checklist, definitions of done, and recommended next commits, see the [Long-Term Maintainer Plan](docs/long-term-plan.md).

## 0.1.x

- Stabilize repository readiness checks.
- Improve transcript parsing and validation errors.
- Add more command-risk patterns for common shell workflows.
- Add examples for PR review, issue triage, and release preparation.

## 0.2.x

- Add configurable policy packs for Python, Swift, JavaScript, and Rust projects.
- Add GitHub issue and PR summary adapters.
- Add report templates for maintainers, contributors, and release notes.
- Improve machine-readable JSON output for CI and dashboards.

## 0.3.x

- Add SARIF export for security-oriented findings.
- Add optional OpenAI/Codex integration for maintainers who want model-assisted summaries.
- Add policy evaluation for verification coverage, risky commands, and missing review notes.

## Long-Term Goals

- Make agent-assisted OSS maintenance auditable by default.
- Help small maintainer teams reduce triage and review workload.
- Provide simple local tooling that does not require a specific agent platform.

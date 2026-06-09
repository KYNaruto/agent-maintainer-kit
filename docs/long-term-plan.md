# Long-Term Maintainer Plan

This plan turns the project roadmap into small, verifiable maintenance milestones. It is intentionally ordered so each phase produces useful OSS maintainer evidence before the next phase begins.

## Working Principles

- Ship one focused, tested improvement at a time.
- Keep all agent-assisted output reviewable by a human maintainer.
- Prefer structured, machine-readable outputs before hosted integrations.
- Document behavior and update the changelog in the same change.
- Do not claim adoption, impact, or security guarantees without evidence.

## Definition of Done

Every feature milestone is complete only when:

- [ ] The behavior has focused tests.
- [ ] CLI help and relevant documentation are updated.
- [ ] CI or a maintainer workflow exercises the behavior.
- [ ] `CHANGELOG.md` includes the change.
- [ ] Repository readiness remains `100/100`.
- [ ] The change is committed and pushed to `main`.

Every release milestone is complete only when:

- [ ] Version metadata and changelog are consistent.
- [ ] The full test suite passes.
- [ ] The wheel builds and installs successfully.
- [ ] A release readiness checklist is reviewed.
- [ ] An annotated tag is pushed.
- [ ] The GitHub Release page and artifacts are verified.

## Phase 1: Stable Local Maintainer Toolkit

Goal: make the dependency-free local CLI predictable enough for maintainers to adopt.

- [x] Repository readiness checks.
- [x] Agent transcript parsing.
- [x] Configurable risky-command policies.
- [x] Markdown and JSON maintainer reports.
- [x] PR/issue review comment drafts.
- [x] Markdown and JSON issue triage reports.
- [x] Release readiness checklists.
- [ ] Friendly CLI errors without Python tracebacks for expected input failures.
- [ ] JSON Schema files for transcript, issue input, config, and generated reports.
- [ ] Stable exit-code documentation for CI use.
- [ ] `--version` CLI option.

Exit criteria:

- Expected user input errors produce concise messages and non-zero exit codes.
- Structured input and output formats have versioned schemas.
- CI verifies all public commands and documented exit codes.

## Phase 2: Policy Packs and Security-Oriented Output

Goal: support real repository differences without making policies opaque.

- [ ] Built-in policy packs for Python, Swift, JavaScript, and Rust repositories.
- [ ] Configurable verification-command markers.
- [ ] Severity levels and rule identifiers for risky-command findings.
- [ ] SARIF output for security-oriented findings.
- [ ] Tests for policy precedence and invalid configurations.
- [ ] Security guidance for consuming untrusted transcripts and issue input.

Exit criteria:

- Maintainers can select or extend a policy pack.
- Every finding has a stable rule ID and severity.
- SARIF output is accepted by a standard SARIF parser.

## Phase 3: GitHub Maintainer Integration

Goal: turn local reports into optional GitHub workflows while preserving explicit maintainer approval.

- [ ] Adapter for GitHub issue event JSON.
- [ ] Adapter for GitHub pull-request event JSON.
- [ ] GitHub Action that generates, but does not automatically post, review comments.
- [ ] Optional approved-post workflow for issue and PR comments.
- [ ] Artifact retention and redaction guidance.
- [ ] Integration tests using sanitized GitHub event fixtures.

Exit criteria:

- A maintainer can generate triage and review artifacts from GitHub events.
- Posting comments requires an explicit workflow permission and maintainer choice.
- Fixtures contain no private repository data or secrets.

## Phase 4: Optional Codex Integration

Goal: add model-assisted summaries without making the local toolkit dependent on a hosted model.

- [ ] Provider-neutral interface for optional model-assisted operations.
- [ ] OpenAI/Codex adapter for PR summaries, issue triage drafts, and release notes.
- [ ] Prompts and outputs stored as auditable artifacts.
- [ ] Secret handling, cost controls, and token-budget documentation.
- [ ] Offline/local fallback remains available for every core workflow.
- [ ] Evaluation fixtures for summary accuracy and risky-command preservation.

Exit criteria:

- Core commands still work without network access or API credentials.
- Model-assisted output is clearly labeled and requires maintainer review.
- Automated evaluations catch missing verification or risk information.

## Phase 5: Community Adoption and Governance

Goal: prove usefulness through external maintenance activity rather than claims.

- [ ] Create good-first-issue candidates from this plan.
- [ ] Track external bug reports and feature requests.
- [ ] Document contributor and maintainer onboarding.
- [ ] Publish usage examples from at least two different repository types.
- [ ] Record release notes and migration guidance for breaking changes.
- [ ] Review governance, support, and security policies each quarter.

Exit criteria:

- At least one external repository uses the toolkit in a maintainer workflow.
- External feedback has resulted in a documented change.
- Releases follow a repeatable review and migration process.

## Next Five Focused Changes

These are the recommended next commits, in order:

1. Add friendly CLI error handling for malformed JSON and invalid config.
2. Add `--version` and document stable exit codes.
3. Add versioned JSON Schemas for issue and transcript inputs.
4. Add rule IDs and severity to risky-command findings.
5. Add a Python policy pack as the first policy-pack implementation.

## Weekly Maintenance Rhythm

- Review open issues and workflow failures.
- Pick one focused item from "Next Five Focused Changes."
- Add or update tests before merging.
- Run `doctor`, tests, and relevant CLI smoke checks.
- Update this plan when priorities or evidence change.
- Release only when a coherent set of user-facing changes is ready.

## Review Cadence

Review this plan:

- After each tagged release.
- After material external feedback.
- Before starting a new phase.
- At least once per month while the project is actively maintained.


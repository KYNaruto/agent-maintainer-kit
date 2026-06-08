# Documentation

Agent Maintainer Kit documentation is organized around maintainer workflows.

- [Maintainer workflows](maintainer-workflows.md): PR review, issue triage, release preparation, and security review.
- [Policy configuration](policy.md): Risk rules for command review.
- [Release process](releasing.md): Local quality gates and automated GitHub Releases.
- [Codex for OSS notes](codex-for-oss.md): Application-oriented project summary and credit usage.
- [Codex for OSS application packet](application-packet.md): Concise form-ready answers and evidence.

## Common Commands

```bash
amk doctor .
amk transcript examples/transcript.jsonl --config examples/amk.config.json
amk report . --transcript examples/transcript.jsonl --output maintainer-report.md
amk report . --transcript examples/transcript.jsonl --format json --output maintainer-report.json
amk comment . --transcript examples/transcript.jsonl --output review-comment.md
amk triage examples/issue.json --output issue-triage.md
amk release . --transcript examples/transcript.jsonl --version 0.1.0
```

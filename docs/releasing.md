# Releasing

Agent Maintainer Kit uses annotated git tags and a GitHub Actions release workflow.

## Release Preparation

1. Update `CHANGELOG.md`.
2. Confirm the version in `pyproject.toml` and `CITATION.cff`.
3. Run the local quality gates:

```bash
python3 -m unittest discover -s tests
PYTHONPATH=src python3 -m agent_maintainer_kit doctor . --min-score 100
PYTHONPATH=src python3 -m agent_maintainer_kit release . --transcript examples/transcript.jsonl --version 0.1.1
```

4. Create and push an annotated tag:

```bash
git tag -a v0.1.1 -m "Agent Maintainer Kit v0.1.1"
git push origin v0.1.1
```

## Automated Release

Pushing a `v*` tag triggers `.github/workflows/release.yml`. The workflow:

- Runs the test suite.
- Verifies repository, transcript, and issue-triage workflows.
- Builds a wheel.
- Generates a release readiness checklist.
- Creates a GitHub Release with generated notes and artifacts.

Human maintainer review remains required before creating and pushing a tag.

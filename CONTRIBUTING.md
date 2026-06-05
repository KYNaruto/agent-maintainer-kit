# Contributing

Thanks for helping improve Agent Maintainer Kit.

## Local Development

```bash
python3 -m pip install -e .
python3 -m unittest discover -s tests
```

## Design Principles

- Keep runtime dependencies at zero unless a feature clearly needs one.
- Prefer small, auditable checks over opaque scoring.
- Make reports useful to maintainers, not just agent operators.
- Treat security-sensitive command detection conservatively.

## Pull Requests

Please include:

- A short explanation of the maintainer workflow being improved.
- Tests for new checks, transcript parsing, or report output.
- Example input when adding a new event type or policy rule.

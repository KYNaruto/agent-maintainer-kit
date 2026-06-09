# Schema Version 1

These JSON Schema Draft 2020-12 files document the stable structured inputs accepted by Agent Maintainer Kit.

- `issue-input.schema.json`: one JSON object accepted by `amk triage`.
- `transcript-event.schema.json`: one JSON object per line in transcript JSONL files.

Unknown additional properties are allowed so agent providers and GitHub adapters can preserve metadata without breaking local analysis.

Unknown transcript event types are also allowed. Agent Maintainer Kit counts them but ignores them in specialized analyzers.

Schema paths are versioned. Incompatible structured-input changes require a new schema directory such as `schemas/v2/`.


# Structured Input Schemas

Agent Maintainer Kit publishes versioned JSON Schema Draft 2020-12 files for structured inputs.

## Version 1

- [Issue input schema](../schemas/v1/issue-input.schema.json): documents JSON accepted by `amk triage`.
- [Transcript event schema](../schemas/v1/transcript-event.schema.json): documents one JSON object per line in transcript JSONL files.

## Compatibility Rules

- Existing schema files are not changed incompatibly.
- Incompatible structured-input changes require a new directory such as `schemas/v2/`.
- Additional properties are allowed so integrations can preserve provider-specific metadata.
- Unknown transcript event types remain valid and are counted without specialized analysis.

## Transcript JSONL

A transcript file is JSON Lines rather than one JSON array. Validate each non-empty line independently against `transcript-event.schema.json`.

Example:

```json
{"type":"command","command":"python3 -m unittest discover -s tests","status":"success"}
```

## Dependency Policy

The schemas follow a standard format, but Agent Maintainer Kit does not require a JSON Schema library at runtime. Consumers may use the validator that best fits their CI or integration environment.

Install the optional validation dependency and verify the repository examples:

```bash
python3 -m pip install -e ".[validation]"
python3 tools/validate_schemas.py
```

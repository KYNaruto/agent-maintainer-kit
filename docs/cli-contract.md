# CLI Contract

This document defines the stable command-line behavior that CI and maintainer automation may rely on.

## Version

Print the installed CLI version:

```bash
amk --version
```

Example:

```text
amk 0.1.1
```

The CLI version, Python package version, `pyproject.toml` version, and release tag should remain consistent for tagged releases.

## Exit Codes

| Code | Name | Meaning |
| --- | --- | --- |
| `0` | `EXIT_SUCCESS` | The command completed successfully. |
| `1` | `EXIT_CHECK_FAILED` | The command ran successfully, but a requested quality or policy gate failed. |
| `2` | `EXIT_INPUT_ERROR` | The command could not run because arguments, files, JSON, configuration, encoding, or permissions were invalid. |

Examples of exit code `1`:

- `doctor` reports a score below `--min-score`.
- `transcript --fail-on-risk` detects a risky command.

Examples of exit code `2`:

- A required file does not exist.
- JSON or JSONL input is malformed.
- Policy configuration has an invalid shape or regular expression.
- An input file cannot be read.
- Command-line arguments are invalid.

Unexpected programming errors are not converted into input errors. They retain a traceback so maintainers can diagnose and fix the defect.

## Output Streams

- Normal reports and status output are written to stdout.
- Expected input errors are written to stderr as `amk: error: ...`.
- Expected input errors do not include Python tracebacks.

## Compatibility

Stable exit-code meanings and the `amk --version` format should not change within a minor release series. Any incompatible CLI contract change must be documented in the changelog and release notes.


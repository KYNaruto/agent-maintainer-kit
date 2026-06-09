from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas" / "v1"


def main() -> int:
    issue_schema = json.loads((SCHEMA_ROOT / "issue-input.schema.json").read_text(encoding="utf-8"))
    event_schema = json.loads((SCHEMA_ROOT / "transcript-event.schema.json").read_text(encoding="utf-8"))

    Draft202012Validator.check_schema(issue_schema)
    Draft202012Validator.check_schema(event_schema)

    issue = json.loads((ROOT / "examples" / "issue.json").read_text(encoding="utf-8"))
    Draft202012Validator(issue_schema).validate(issue)

    event_validator = Draft202012Validator(event_schema)
    transcript_lines = (ROOT / "examples" / "transcript.jsonl").read_text(encoding="utf-8").splitlines()
    for line_number, line in enumerate(transcript_lines, start=1):
        if line.strip():
            event_validator.validate(json.loads(line))
            print(f"Validated transcript event on line {line_number}")

    print("Schemas and examples are valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_ROOT = ROOT / "schemas" / "v1"


class SchemaTest(unittest.TestCase):
    def test_versioned_schemas_use_draft_2020_12(self) -> None:
        for path in SCHEMA_ROOT.glob("*.schema.json"):
            with self.subTest(schema=path.name):
                schema = json.loads(path.read_text(encoding="utf-8"))
                self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
                self.assertIn("/schemas/v1/", schema["$id"])
                self.assertTrue(schema["additionalProperties"])

    def test_issue_example_matches_declared_contract(self) -> None:
        schema = json.loads((SCHEMA_ROOT / "issue-input.schema.json").read_text(encoding="utf-8"))
        issue = json.loads((ROOT / "examples" / "issue.json").read_text(encoding="utf-8"))

        self.assertTrue(set(schema["required"]).issubset(issue))
        self.assertIsInstance(issue["title"], str)
        self.assertGreaterEqual(len(issue["title"]), schema["properties"]["title"]["minLength"])
        self.assertIsInstance(issue["body"], str)
        self.assertIsInstance(issue["labels"], list)
        self.assertTrue(all(isinstance(label, str) and label for label in issue["labels"]))

    def test_transcript_examples_match_declared_event_contracts(self) -> None:
        schema = json.loads((SCHEMA_ROOT / "transcript-event.schema.json").read_text(encoding="utf-8"))
        events = [
            json.loads(line)
            for line in (ROOT / "examples" / "transcript.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        event_requirements = {
            rule["if"]["properties"]["type"].get("const"): rule["then"].get("required", [])
            for rule in schema["allOf"]
            if "const" in rule["if"]["properties"]["type"]
        }

        for event in events:
            with self.subTest(event=event["type"]):
                self.assertIsInstance(event["type"], str)
                self.assertTrue(event["type"])
                for required in event_requirements.get(event["type"], []):
                    self.assertIn(required, event)


if __name__ == "__main__":
    unittest.main()


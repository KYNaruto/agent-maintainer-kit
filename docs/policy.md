# Policy Configuration

Agent Maintainer Kit uses policy configuration to adapt command-risk detection to each repository.

## Config File

`amk` looks for `amk.config.json` when generating reports for a repository. You can also pass a config explicitly:

```bash
amk transcript agent-session.jsonl --config amk.config.json
amk report . --transcript agent-session.jsonl --config amk.config.json
```

## Risk Rules

Use `risky_commands` for literal command fragments:

```json
{
  "policy": {
    "risky_commands": ["git push --force", "rm -rf"]
  }
}
```

Use `risky_command_regexes` for regular expressions:

```json
{
  "policy": {
    "risky_command_regexes": ["curl .+ \\\\| sh", "chmod -R [0-7]{3}"]
  }
}
```

## Default Policy

When no config is provided, `amk` flags common risky patterns such as destructive deletion, hard git resets, privileged execution, broad permission changes, and raw disk writes.

## Maintainer Guidance

Risk detection is intentionally conservative. A flagged command is not automatically wrong; it means a maintainer should review the command before accepting an agent-generated change or report.


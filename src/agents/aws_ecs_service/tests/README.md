# Tests Directory

This directory contains test files for the AWS ECS Deep Agent.

## Files

- `test_credential_sharing.py` - Comprehensive test suite for credential sharing functionality
  - Tests basic credential storage and retrieval
  - Tests isolation between contexts
  - Tests concurrent agent invocations
  - Tests the full subagent credential flow

## Running Tests

```bash
cd /path/to/graph-fleet
poetry run pytest src/agents/aws_ecs_service/tests/
```

Note: Some tests require the full agent dependencies (deepagents, langchain, etc.)

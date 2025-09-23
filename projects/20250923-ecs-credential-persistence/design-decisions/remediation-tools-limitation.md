# Design Decision: Remediation Tools Credential Loading

## Context
The remediation tools (`execute_ecs_fix` and `analyze_and_remediate`) have a different architecture than diagnostic tools:
- Diagnostic tools use `@tool` decorator and receive `state` parameter
- Remediation tools are factory functions that return callables, initialized with `credential_context`

## Problem
Remediation tools don't have access to the agent state at runtime, making it impossible to read credentials from the state files directly.

## Current Architecture
```python
# At agent creation time:
remediation_tool = execute_ecs_fix(credential_context)

# At runtime:
result = await remediation_tool(fix_type, parameters)
# No state parameter available here
```

## Temporary Solution
For the initial implementation, remediation tools will continue using the `credential_context` approach. This means:
1. Credentials saved to `aws_credentials.json` during diagnosis
2. Diagnostic tools read from the file (implemented)
3. Remediation tools still use credential_context (not changed)

## Future Enhancement Options
1. **Refactor remediation tools** to use `@tool` decorator and receive state
2. **Use environment variables** to pass credential file path
3. **Create a wrapper tool** that reads credentials and calls remediation tools
4. **Modify credential_context** to read from files as fallback

## Recommendation
For simplicity in the initial version, keep remediation tools unchanged. Focus on making diagnostic tools work with file-based credentials first.

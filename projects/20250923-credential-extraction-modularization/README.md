# Credential Extraction Modularization

**Project Start Date:** September 23, 2025  
**Status:** Planning Phase

## Project Overview

Modularize the duplicated AWS credential extraction logic from credentials.json that's currently repeated across multiple diagnostic wrapper functions into a reusable utility.

## Problem Statement

Currently, the same credential extraction logic is duplicated across multiple MCP wrapper functions in `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/diagnostic_wrappers.py`:

1. **describe_ecs_services_wrapped** (lines 91-124)
2. **describe_ecs_tasks_wrapped** (lines 265-298)  
3. **get_deployment_status_wrapped** (lines 477-510)

Each function contains identical code for:
- Checking if `aws_credentials.json` exists in files
- Parsing the JSON content
- Extracting `access_key_id`, `secret_access_key`, and `region`
- Handling parsing errors with consistent error messages

## Primary Goal

Extract the repeated credential loading/parsing logic into a shared utility function that can be imported and reused across all MCP wrapper functions, eliminating code duplication and making credential handling more maintainable.

## Technical Details

- **Technology Stack:** Python
- **Project Type:** refactoring
- **Affected Components:** MCP wrapper functions in `src/agents/aws_ecs_troubleshooter/tools/mcp_wrappers/`
- **Timeline:** 1-2 days
- **Dependencies:** None (internal refactoring)

## Success Criteria

- All credential extraction logic consolidated into a single reusable function
- No duplicated credential parsing code across wrapper functions
- Consistent error handling for credential-related issues
- Backwards compatibility maintained for existing functionality
- Improved maintainability and testability of credential handling

## Project Structure

```
projects/20250923-credential-extraction-modularization/
├── README.md                      # This file
├── next-task.md                   # Quick resume file
├── tasks/                         # Task breakdown and execution
├── checkpoints/                   # Project milestones
├── design-decisions/              # Architecture and design choices
├── coding-guidelines/             # Project-specific guidelines
├── wrong-assumptions/             # Learnings and corrections
└── dont-dos/                      # Anti-patterns to avoid
```

## Current Duplication Analysis

The duplicated code pattern follows this structure:

```python
# 1. Check file existence
files = state.get("files", {})
if "aws_credentials.json" not in files:
    # Return error message

# 2. Parse JSON content  
try:
    creds_data = json.loads(files["aws_credentials.json"])
    credentials = {
        "access_key_id": creds_data["access_key_id"],
        "secret_access_key": creds_data["secret_access_key"],
        "region": creds_data.get("region", "us-east-1")
    }
except Exception as e:
    # Return parsing error
```

This exact pattern appears 3 times with identical error messages and logic.

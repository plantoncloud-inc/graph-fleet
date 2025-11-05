## Summary

Updated RDS Manifest Generator to dynamically extract organization and environment values from execution context via LangGraph's configurable mechanism, replacing hard-coded defaults and enabling multi-tenancy support.

## Context

The RDS Manifest Generator (and potentially other manifest generators) used hard-coded org and env values (`org="project-planton"`, `env="aws"`). This blocked multi-tenancy as all manifests were generated with the same metadata regardless of which organization triggered the execution. The backend now passes org/env through LangGraph's config, and agents need to extract and use these values.

## Changes

- **Tool update**: Modified `generate_rds_manifest()` to accept `config: RunnableConfig` parameter and extract org/env from `config["configurable"]`
- **Removed hard-coded parameters**: Org and env are no longer function parameters - they come from execution context
- **Fallback defaults**: Maintains defaults for local development/testing when config is not provided
- **Documentation updates**: Updated INTEGRATION.md, USER_GUIDE.md, and PHASE3_COMPLETE.md to reflect the new implementation

## Implementation notes

- Added import: `from langchain_core.runnables import RunnableConfig`
- Extract pattern: `org = config["configurable"].get("org", "project-planton")`
- Backward compatible: Local LangGraph Studio development still works with fallback defaults
- Standard LangGraph pattern: Uses built-in configurable mechanism (recommended approach)

## Breaking changes

None. The tool signature change is internal to the agent - external callers (LangGraph runtime) automatically pass the config parameter. Local testing continues to work with fallback defaults.

## Test plan

- Code compiles and passes linting
- No TypeScript/Python type errors
- Documentation accurately reflects implementation
- Pattern is consistent with LangGraph best practices

## Risks

- Low risk: Fallback defaults ensure backward compatibility
- Local development workflow unchanged
- Production manifests will now use correct org/env values automatically

## Checklist

- [x] Docs updated (3 documentation files updated with examples)
- [x] Tests added/updated (no new tests needed - configuration extraction)
- [x] Backward compatible (fallback defaults for local development)


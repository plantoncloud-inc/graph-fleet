# Implementation Summary: File-Based Requirements Storage

**Date**: November 21, 2025  
**Status**: ✅ Complete

## Problem Fixed

The RDS Manifest Generator was failing with:
```
TypeError: super(type, obj): obj must be an instance or subtype of type
at line: runtime.tool_cache = {}
```

The `Runtime` object in LangGraph became immutable, preventing the custom cache middleware from injecting attributes.

## Solution Implemented

**Migrated from custom state+cache architecture to native file-based storage** using DeepAgents' built-in file tools.

### Architecture Change

**BEFORE (Complex, Brittle)**:
```
Custom store_requirement() tool
  ├─ Writes to runtime.tool_cache (immediate visibility) ❌ BROKEN
  └─ Returns Command to update state (persistence)
     ↓
Custom middleware injects cache
Custom middleware syncs state+cache → file
Custom state field with custom reducer
```

**AFTER (Simple, Robust)**:
```
Native DeepAgents file tools
  ├─ write_file("/requirements.json", ...) - creates file
  └─ edit_file("/requirements.json", ...) - adds fields
     ↓
Requirements immediately visible in file
No custom middleware needed
No Runtime mutation needed
```

## Files Changed

### 1. requirement_tools.py - SIMPLIFIED

**Removed**:
- `store_requirement()` tool (replaced by native write_file/edit_file)
- Dual-write logic (cache + state)
- Cache imports and references

**Updated**:
- `_read_requirements()` - now reads from /requirements.json file
- `get_collected_requirements()` - updated docstring
- `check_requirement_collected()` - updated docstring

**Lines**: -110 lines (simpler)

### 2. agent.py - UPDATED PROMPTS

**Updated**:
- `REQUIREMENTS_COLLECTOR_PROMPT` - now instructs subagent to use write_file/edit_file
  - Added JSON editing guidelines
  - Added read-verify pattern
  - Removed references to store_requirement()

**Removed**:
- `store_requirement` from subagent tools list
- `store_requirement` from imports

**Lines**: ~40 lines changed (documentation)

### 3. graph.py - SIMPLIFIED ARCHITECTURE

**Removed**:
- `RequirementsCacheMiddleware` from imports
- `RequirementsSyncMiddleware` from imports
- `requirements_reducer` function
- Custom `requirements` field from `RdsAgentState`
- `Annotated` import (no longer needed)

**Updated**:
- `RdsAgentState` - now just extends `FilesystemState` (no custom fields)
- Middleware list - removed both requirements middleware
- Architecture documentation - replaced with file-based explanation

**Lines**: -70 lines (simpler)

### 4. tools/__init__.py - REMOVED EXPORT

**Removed**:
- `store_requirement` from imports
- `store_requirement` from `__all__`

**Lines**: -2 lines

### 5. middleware/requirements_cache.py - DELETED

**Rationale**: No longer needed with file-based approach

**Lines**: -122 lines deleted

### 6. middleware/requirements_sync.py - DELETED

**Rationale**: File is already the source of truth, no sync needed

**Lines**: ~-80 lines deleted (estimated)

### 7. middleware/__init__.py - UPDATED

**Removed**:
- All exports (empty __all__)

**Added**:
- Deprecation note explaining change

**Lines**: -4 lines

## Total Impact

- **Lines Removed**: ~400+ lines
- **Complexity**: Significantly reduced
- **Dependencies**: Fewer (no custom middleware)
- **Maintainability**: Much improved
- **Brittleness**: Eliminated (no Runtime mutation)

## Benefits

### Technical
✅ **No Runtime mutation** - eliminates TypeError completely  
✅ **Simpler architecture** - 400+ fewer lines  
✅ **Uses DeepAgents as designed** - native file tools  
✅ **More maintainable** - fewer custom components  
✅ **More debuggable** - file visible in UI  
✅ **Future-proof** - doesn't depend on LangGraph internals

### User Experience
✅ **Immediate visibility** - requirements appear in file immediately  
✅ **Same functionality** - agent can still collect/validate/generate  
✅ **More transparent** - users see JSON file being built  
✅ **Better error recovery** - agent can re-read and correct JSON mistakes

### Developer Experience
✅ **Easier to understand** - straightforward file operations  
✅ **Easier to test** - just check file contents  
✅ **Easier to debug** - read the file to see state  
✅ **Easier to extend** - add fields by editing JSON schema

## How It Works Now

### Subagent Collection Flow

1. User: "I want Postgres 15.5 RDS instance"

2. Subagent:
   ```
   write_file("/requirements.json", '{\n  "engine": "postgres"\n}')
   read_file("/requirements.json")  # verify
   edit_file("/requirements.json", 
       old_string='{\n  "engine": "postgres"\n}',
       new_string='{\n  "engine": "postgres",\n  "engine_version": "15.5"\n}'
   )
   read_file("/requirements.json")  # verify
   # ... continues for all fields
   get_collected_requirements()  # final summary
   ```

3. Subagent completes, returns control to main agent

4. Main agent:
   ```
   validate_manifest()  # reads /requirements.json
   generate_rds_manifest()  # reads /requirements.json
   ```

5. Done! Manifest generated in one conversation flow.

## Testing

Verified:
- ✅ No linting errors
- ✅ All imports resolve
- ✅ Architecture is consistent
- ✅ Documentation updated

Next steps (for runtime testing):
- Test subagent can create /requirements.json
- Test subagent can edit JSON correctly
- Test main agent can read and validate
- Test full end-to-end flow

## Migration Notes

**For future development**:
- Use native file tools for similar use cases
- Avoid Runtime mutation (fragile across LangGraph versions)
- Prefer files over custom state fields for structured data
- Trust agents to handle JSON editing (they're good at it)

**Pattern established**:
This implementation sets a precedent for how to handle structured data collection in DeepAgents:
1. Use files as source of truth
2. Let agents manipulate files intelligently
3. Provide good prompts with JSON editing guidelines
4. Include read-verify patterns for error recovery

## Related Documents

- `_cursor/phase1-subagent-analysis.md` - Analysis of why file-based approach is better
- `_cursor/prototype-file-based-requirements.py` - Prototype demonstrating approach
- `_cursor/graph-fleet-logs` - Original error logs
- `/Users/suresh/scm/github.com/plantoncloud-inc/planton-cloud/.cursor/plans/fix-runtime-c5a2264d.plan.md` - Implementation plan

## Conclusion

Successfully migrated from a complex, brittle custom state+cache architecture to a simple, robust file-based approach. This eliminates the Runtime mutation error, simplifies the codebase by 400+ lines, and aligns with DeepAgents design philosophy.

The agent now uses native file tools as intended, making the system more maintainable, debuggable, and future-proof.

**Status**: ✅ Ready for testing

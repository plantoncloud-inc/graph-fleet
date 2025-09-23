# Task Plan: ECS Context Deep Agents - Initial Plan

**Project**: Simplify ECS Context Gathering with Deep Agents Patterns
**Date**: 2025-09-23
**Status**: PENDING REVIEW

## Objective

Refactor the context-gathering phase of the AWS ECS troubleshooter to adopt deep-agents patterns, making it more flexible, LLM-driven, and maintainable.

## Analysis of Current Implementation

The current `context_tools.py` has these characteristics:
1. **Deterministic flow**: Hard-coded sequence of MCP tool calls
2. **Single monolithic function**: `gather_planton_context` does everything
3. **No state persistence**: Context is gathered but not saved to files
4. **Limited flexibility**: Can't adapt to different scenarios
5. **No progress tracking**: No visibility into what's happening

## Deep Agents Patterns to Adopt

Based on the deep-agents-from-scratch repository:

### 1. **Todo Management**
- Create structured task lists for context gathering
- Track progress through each step
- Provide visibility into the process

### 2. **File System Usage**
- Save context to files for persistence
- Enable incremental gathering and resume capability
- Store raw responses for later reference

### 3. **Sub-agent Delegation**
- Create specialized sub-agents for different context types
- Enable parallel context gathering
- Isolate concerns and improve modularity

### 4. **Structured Prompts**
- Clear instructions for each component
- Well-defined tool descriptions
- Explicit success criteria

## Proposed Architecture

### High-Level Components

1. **Context Coordinator Agent** (Main)
   - Manages todo list for context gathering
   - Delegates to specialized sub-agents
   - Saves progress to files
   - Makes strategic decisions about what context is needed

2. **Planton Context Sub-agent**
   - Gathers service metadata from Planton Cloud
   - Extracts AWS credentials
   - Saves results to files

3. **AWS Context Sub-agent** (Future)
   - Gathers ECS service details
   - Collects related AWS resources
   - Saves results to files

### Tool Architecture

1. **MCP Tools Integration**
   - Wrap MCP tools to work with deep-agents patterns
   - Add file saving capabilities
   - Return minimal summaries (like tavily_search)

2. **Context Tools**
   - `gather_context`: Main coordination tool
   - `save_context`: File persistence tool
   - `summarize_context`: Create minimal summaries

3. **Progress Tools**
   - Todo management (from deep-agents)
   - File system tools (from deep-agents)
   - Think tool for reflection

## Task Breakdown

### Task 1: Create Base Infrastructure (2 hours)
- [ ] Set up project structure
- [ ] Create base context state schema
- [ ] Implement file-based context storage
- [ ] Create context summarization utilities

### Task 2: Implement MCP Tool Wrappers (2 hours)
- [ ] Create wrapper for Planton Cloud MCP tools
- [ ] Add file saving to tool responses
- [ ] Implement minimal summary returns
- [ ] Test MCP tool integration

### Task 3: Build Context Sub-agents (2 hours)
- [ ] Create Planton Context sub-agent
- [ ] Implement structured prompts
- [ ] Add tool descriptions
- [ ] Test sub-agent isolation

### Task 4: Create Main Coordinator (1 hour)
- [ ] Implement context coordinator logic
- [ ] Add todo management
- [ ] Create delegation logic
- [ ] Test end-to-end flow

### Task 5: Testing and Documentation (1 hour)
- [ ] Create test scenarios
- [ ] Document new architecture
- [ ] Migration guide from old approach
- [ ] Performance comparison

## Success Criteria

1. **LLM-driven tool selection**: The agent decides which tools to call based on the situation
2. **Progress visibility**: Clear todo tracking throughout the process
3. **State persistence**: Context saved to files for resume capability
4. **Modular design**: Clear separation of concerns with sub-agents
5. **Simplified code**: More readable and maintainable than current implementation

## Risks and Mitigation

1. **MCP Tool Compatibility**
   - Risk: MCP tools might not work well with Command pattern
   - Mitigation: Create adapter layer if needed

2. **Performance**
   - Risk: Multiple sub-agents might be slower
   - Mitigation: Use parallel execution where possible

3. **Complexity**
   - Risk: Deep-agents patterns might add complexity
   - Mitigation: Keep it simple, add patterns incrementally

## Next Steps

1. Review this plan and provide feedback
2. Start with Task 1 after approval
3. Iterate based on learnings

## Questions for Review

1. Should we include AWS context gathering in this phase or keep it for later?
2. Any specific MCP tools we should prioritize for the wrapper?
3. Should we maintain any backward compatibility interfaces?
4. Any specific test scenarios you'd like to see?

---

**Note**: This plan aims for a one-day implementation. If we find it's more complex, we can break it into phases.

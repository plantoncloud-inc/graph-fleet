# Task 01: Improve ECS Agent Instructions

**Created**: Monday, September 23, 2025  
**Type**: Refactoring & Enhancement  
**Status**: Planning

## Objective

Refactor the AWS ECS Troubleshooter instructions.py file to better align with deep-agents patterns, remove redundancies, and improve agent coordination.

## Background

The current instructions have several issues:
1. Context gathering instructions mention a think_tool reflection step but may not implement it properly
2. Main agent instructions have a redundant "Review Context" step that duplicates context gathering
3. Diagnostic specialist instructions need better alignment with the overall workflow
4. Instructions don't fully follow deep-agents prompt patterns (clear sections, hard limits, etc.)

## Task Breakdown

### 1. Analysis Phase (30 minutes)
- [ ] Review current instructions.py structure and content
- [ ] Identify all areas needing improvement
- [ ] Map current workflow vs desired workflow
- [ ] Document specific issues with each instruction function

### 2. Research Phase (30 minutes)
- [ ] Study deep-agents prompt patterns from reference repository
- [ ] Extract key patterns: structure, sections, language style
- [ ] Identify best practices for:
  - Tool usage instructions
  - Workflow descriptions
  - Hard limits and constraints
  - Reflection patterns

### 3. Context Gathering Refactor (45 minutes)
- [ ] Add explicit think_tool reflection step at the end
- [ ] Ensure the reflection includes:
  - Assessment of gathered context
  - Identification of missing information
  - Decision on whether to proceed
- [ ] Align with deep-agents patterns for tool instructions
- [ ] Test compatibility with existing implementation

### 4. Main Agent Instructions Refactor (1 hour)
- [ ] Remove redundant "Step 2: Review Context" section
- [ ] Streamline workflow to trust context-gatherer's completeness
- [ ] Improve coordination instructions for sub-agents
- [ ] Add clearer decision points for when to use each sub-agent
- [ ] Follow deep-agents structure:
  - Clear role definition
  - Available tools/sub-agents listing
  - Workflow with examples
  - Important guidelines
  - Hard limits if applicable

### 5. Diagnostic Specialist Enhancement (45 minutes)
- [ ] Review current diagnostic instructions
- [ ] Ensure proper file-based workflow integration
- [ ] Add structured output format requirements
- [ ] Align with main agent's expectations
- [ ] Include proper reflection patterns

### 6. Testing & Validation (30 minutes)
- [ ] Verify all instruction functions work together
- [ ] Check that removed redundancies don't break workflow
- [ ] Ensure think_tool integration is smooth
- [ ] Test that file-based patterns are preserved

## Implementation Strategy

### Phase 1: Analysis and Planning
1. Read through entire instructions.py file
2. Create a mapping of current vs desired state
3. Document specific changes needed for each function

### Phase 2: Deep-agents Pattern Study
1. Extract prompt patterns from deep-agents repository
2. Create a template for our instruction format
3. Note specific language and structure patterns to adopt

### Phase 3: Incremental Refactoring
1. Start with context gathering (smallest change)
2. Move to main agent (remove redundancy, improve flow)
3. Finish with diagnostic specialist (ensure alignment)
4. Test each change incrementally

### Phase 4: Final Integration
1. Review all instructions as a cohesive whole
2. Ensure consistent language and patterns
3. Verify workflow integrity
4. Document any breaking changes

## Success Metrics

1. **Context Gathering**: Includes explicit think_tool reflection step
2. **Main Agent**: No redundant review step, clearer sub-agent usage
3. **Diagnostic Specialist**: Better integrated with overall workflow
4. **Pattern Compliance**: Follows deep-agents prompt structure
5. **Backward Compatibility**: Works with existing agent implementation

## Risk Mitigation

1. **Breaking Changes**: Test each modification incrementally
2. **Pattern Mismatch**: Adapt patterns to fit existing architecture
3. **Workflow Disruption**: Maintain file-based state management
4. **Integration Issues**: Verify sub-agent communication paths

## Next Steps

1. Begin with detailed analysis of current instructions.py
2. Create a comparison chart of current vs desired patterns
3. Start implementation with context gathering instructions
4. Proceed through each instruction function systematically

## Notes

- The deep-agents patterns emphasize clarity, structure, and explicit limits
- File-based workflow must be preserved throughout changes
- Think_tool integration should feel natural, not forced
- Main agent should trust sub-agents' work rather than re-verify

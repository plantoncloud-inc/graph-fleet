# Task 01.1: Analysis of Current Instructions

**Created**: Monday, September 23, 2025  
**Status**: Complete

## Overview

Analysis of the current `instructions.py` file to identify improvement areas aligned with deep-agents patterns.

## Key Findings

### 1. Context Gathering Instructions (`get_context_gathering_instructions`)

**Issues Identified**:
- ✅ Already mentions think_tool in section 4 "Reflect and Verify"
- ❌ But it's not explicitly stated as a required final step
- ❌ Missing hard limits or constraints
- ❌ No clear "stop conditions" like deep-agents patterns
- ❌ Structure could be more aligned with deep-agents format

**Current Structure**:
- Your Goal
- Context Gathering Process (1-4)
- Important Patterns
- Context Completeness Checklist

**Deep-agents Structure Pattern**:
- Task description
- Available Tools
- Instructions/Workflow
- Hard Limits
- Show Your Thinking

### 2. Main Agent Instructions (`get_main_agent_instructions`)

**Issues Identified**:
- ❌ **Step 2: Review Context** is redundant - context-gatherer already verifies completeness
- ❌ Missing hard limits for delegation
- ❌ No clear decision criteria for when to use each sub-agent
- ❌ Workflow could be more streamlined
- ❌ Missing parallel execution guidance (deep-agents emphasizes this)

**Redundancy Analysis**:
- Context-gatherer already has "Reflect and Verify" step
- Context-gatherer has "Context Completeness Checklist"
- Main agent shouldn't need to re-verify what sub-agent already validated

### 3. Diagnostic Specialist Instructions (`get_diagnostic_specialist_instructions`)

**Issues Identified**:
- ✅ Well-structured with clear process
- ✅ Has TODO-driven workflow
- ✅ Includes think_tool usage
- ❌ Missing hard limits (e.g., max diagnostic iterations)
- ❌ Could use more explicit "stop conditions"
- ❌ Output format section could be more detailed

### 4. General Instruction V2 (`ECS_TROUBLESHOOTER_INSTRUCTIONS_V2`)

**Issues Identified**:
- ✅ Good overview structure
- ❌ Not actively used in the agent flow?
- ❌ Could serve as a unified instruction set

### 5. Remediation Specialist Instructions

**Issues Identified**:
- ❌ Too brief compared to other specialists
- ❌ Missing deep-agents structure entirely
- ❌ No TODO workflow
- ❌ No file-based patterns

## Pattern Comparison

### Deep-agents Patterns to Adopt:

1. **Clear Section Headers**:
   - `<Task>` - What the agent should do
   - `<Available Tools>` - Tools with descriptions
   - `<Instructions>` or `<Workflow>` - Step-by-step process
   - `<Hard Limits>` - Constraints and budgets
   - `<Show Your Thinking>` - Reflection requirements

2. **Explicit Limits**:
   - Tool call budgets
   - Iteration limits
   - Stop conditions

3. **Parallel Execution**:
   - Deep-agents emphasizes parallel tool calls
   - Multiple sub-agent delegation when beneficial

4. **Reflection Pattern**:
   - Always use think_tool after key steps
   - Structured reflection questions

## Specific Changes Needed

### For Context Gathering:
1. Add explicit final step: "Use think_tool to confirm context completeness"
2. Add Hard Limits section (e.g., max 5 tool calls)
3. Restructure to match deep-agents format
4. Make reflection mandatory, not optional

### For Main Agent:
1. Remove Step 2 (Review Context) entirely
2. Add Hard Limits for delegation
3. Add decision criteria for sub-agent selection
4. Include parallel delegation guidance
5. Streamline workflow to trust sub-agents

### For Diagnostic Specialist:
1. Add Hard Limits section
2. Enhance output format requirements
3. Add explicit stop conditions
4. Strengthen reflection pattern

### For Remediation Specialist:
1. Complete rewrite following deep-agents pattern
2. Add TODO workflow
3. Add file-based patterns
4. Add proper structure

## Next Steps

1. Study deep-agents patterns in detail
2. Create templates for each instruction type
3. Implement changes incrementally
4. Test compatibility with existing implementation

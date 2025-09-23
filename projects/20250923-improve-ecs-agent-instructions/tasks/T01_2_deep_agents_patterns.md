# Task 01.2: Deep-agents Pattern Analysis

**Created**: Monday, September 23, 2025  
**Status**: Complete

## Overview

Analysis of deep-agents prompt patterns to extract best practices for our ECS agent instructions.

## Key Patterns Identified

### 1. Structured Sections with XML-style Tags

Deep-agents uses clear section delimiters:
- `<Task>` - Defines what the agent should do
- `<Available Tools>` - Lists tools with descriptions
- `<Instructions>` or `<Workflow>` - Step-by-step process
- `<Hard Limits>` - Constraints and budgets
- `<Show Your Thinking>` - Reflection requirements
- `<Scaling Rules>` - When to use parallel execution

### 2. Tool Descriptions

Each tool has:
- **Bold name** with brief description
- Parameter explanations
- Usage context
- Clear value proposition

Example:
```
1. **tavily_search**: For conducting web searches to gather information
2. **think_tool**: For reflection and strategic planning during research

**CRITICAL: Use think_tool after each search to reflect on results and plan next steps**
```

### 3. Hard Limits Pattern

Always includes:
- **Tool Call Budgets** with specific numbers
- **Stop Conditions** - When to stop immediately
- Clear categorization (Simple/Normal/Complex)

Example:
```
<Hard Limits>
**Tool Call Budgets** (Prevent excessive searching):
- **Simple queries**: Use 1-2 search tool calls maximum
- **Normal queries**: Use 2-3 search tool calls maximum
- **Very Complex queries**: Use up to 5 search tool calls maximum

**Stop Immediately When**:
- You can answer the user's question comprehensively
- You have 3+ relevant examples/sources
- Your last 2 searches returned similar information
</Hard Limits>
```

### 4. Reflection Pattern

Think_tool usage is:
- **Mandatory** after key steps
- Has specific reflection questions
- Guides decision-making

Example:
```
<Show Your Thinking>
After each search tool call, use think_tool to analyze the results:
- What key information did I find?
- What's missing?
- Do I have enough to answer the question comprehensively?
- Should I search more or provide my answer?
</Show Your Thinking>
```

### 5. Parallel Execution Emphasis

Deep-agents strongly emphasizes parallel work:
- **PARALLEL RESEARCH** in bold/caps
- Specific limits (e.g., max 3 concurrent)
- Examples of when to parallelize

### 6. Human-like Language

Instructions use:
- "Think like a human researcher with limited time"
- Natural workflow descriptions
- Practical examples
- Clear, conversational tone

### 7. Example-Driven Explanations

Scaling rules include concrete examples:
- Simple: "List the top 10 coffee shops"
- Comparison: "Compare OpenAI vs. Anthropic"
- Multi-faceted: "Research renewable energy: costs, impact, adoption"

## Template for Our Instructions

Based on deep-agents patterns, our template should be:

```python
AGENT_INSTRUCTIONS = """You are [role description]. For context, today's date is {date}.

<Task>
[Clear, concise description of the agent's primary purpose]
</Task>

<Available Tools>
1. **tool_name**: Brief description of what it does
   - parameter: What it means
   - Returns: What to expect

**CRITICAL: [Any critical tool usage patterns]**
</Available Tools>

<Instructions>
[Step-by-step workflow in natural language]

1. **First Step** - Description
2. **Second Step** - Description
3. **Use think_tool** - Reflect on progress
4. **Final Step** - Complete the task
</Instructions>

<Hard Limits>
**Tool Call Budgets**:
- **Simple tasks**: X tool calls maximum
- **Complex tasks**: Y tool calls maximum
- **Always stop**: After Z tool calls

**Stop Immediately When**:
- [Condition 1]
- [Condition 2]
- [Condition 3]
</Hard Limits>

<Show Your Thinking>
Use think_tool to reflect on:
- [Reflection point 1]
- [Reflection point 2]
- [Reflection point 3]
</Show Your Thinking>

[Any additional sections like <Scaling Rules> if needed]
"""
```

## Key Takeaways for Our Refactoring

1. **Structure**: Use XML-style tags for clear sections
2. **Limits**: Always include hard limits with specific numbers
3. **Reflection**: Make think_tool usage mandatory and structured
4. **Examples**: Include concrete examples where helpful
5. **Parallel**: Emphasize parallel execution where applicable
6. **Natural**: Use conversational, human-like language
7. **Critical**: Use CRITICAL in caps for important patterns

## Application to ECS Agent

### Context Gathering:
- Add `<Hard Limits>` section (max 5 tool calls)
- Make think_tool reflection mandatory in `<Show Your Thinking>`
- Use structured sections

### Main Agent:
- Remove redundant review step
- Add `<Scaling Rules>` for parallel sub-agent delegation
- Include delegation budgets in `<Hard Limits>`

### Diagnostic Specialist:
- Add `<Hard Limits>` with iteration limits
- Enhance `<Show Your Thinking>` section
- Structure output requirements better

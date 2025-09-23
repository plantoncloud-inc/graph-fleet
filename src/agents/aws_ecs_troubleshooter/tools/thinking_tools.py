"""Strategic thinking and reflection tools for AWS ECS troubleshooter.

This module provides the think_tool for structured reflection and strategic planning
during troubleshooting workflows, following the deep-agents pattern with file persistence.
"""

import json
import logging
from datetime import datetime
from typing import Optional

from langchain_core.messages import ToolMessage
from langchain_core.tools import InjectedToolCallId, tool
from langgraph.prebuilt import InjectedState
from langgraph.types import Command
from typing_extensions import Annotated

from deepagents import DeepAgentState  # type: ignore[import-untyped]

logger = logging.getLogger(__name__)


def get_timestamp() -> str:
    """Get current timestamp for file naming."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def get_iso_timestamp() -> str:
    """Get ISO format timestamp for metadata."""
    return datetime.now().isoformat()


@tool(parse_docstring=True)
def think_tool(
    reflection: str,
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    context: Optional[str] = None,
) -> Command:
    """Tool for strategic reflection on troubleshooting progress and decision-making.
    
    Use this tool to pause and reflect on your progress, analyze findings, identify gaps,
    and plan next steps systematically. This creates a deliberate pause in the workflow
    for quality decision-making and strategic planning.
    
    When to use:
    - After gathering context: What information have I collected?
    - Before diagnosis: Do I have enough context to proceed?
    - After diagnosis: What issues did I identify and what's the root cause?
    - Before remediation: What's the safest approach to fix this?
    - After actions: Did my actions achieve the desired outcome?
    - When stuck: What am I missing and what should I try next?
    
    Reflection should address:
    1. Current state analysis - What do I know so far?
    2. Gap assessment - What crucial information is still missing?
    3. Quality evaluation - Do I have sufficient evidence for conclusions?
    4. Strategic decision - What should be my next step and why?
    5. Risk consideration - What could go wrong with my planned approach?
    
    Args:
        reflection: Your detailed reflection on progress, findings, gaps, and next steps
        state: Injected agent state for file storage
        tool_call_id: Injected tool call identifier
        context: Optional context identifier (e.g., "context_gathering", "diagnosis", "remediation")
        
    Returns:
        Command that saves reflection to file and provides confirmation
    """
    try:
        # Create filename with timestamp and context
        timestamp = get_timestamp()
        context_str = f"_{context}" if context else ""
        filename = f"reflections/{timestamp}{context_str}.json"
        
        # Prepare reflection data with metadata
        reflection_data = {
            "timestamp": get_iso_timestamp(),
            "context": context or "general",
            "reflection": reflection,
            "metadata": {
                "tool": "think_tool",
                "character_count": len(reflection),
                "word_count": len(reflection.split()),
            }
        }
        
        # Extract key insights from reflection for summary
        # Look for common patterns in reflections
        key_points = []
        
        if "gathered" in reflection.lower() or "collected" in reflection.lower():
            key_points.append("✓ Reviewed gathered information")
        if "missing" in reflection.lower() or "need" in reflection.lower():
            key_points.append("⚠ Identified gaps or needs")
        if "next" in reflection.lower() or "should" in reflection.lower():
            key_points.append("→ Planned next steps")
        if "issue" in reflection.lower() or "problem" in reflection.lower():
            key_points.append("🔍 Analyzed issues")
        if "fix" in reflection.lower() or "remediate" in reflection.lower():
            key_points.append("🔧 Considered remediation")
        
        # Save to file
        files = state.get("files", {})
        files[filename] = json.dumps(reflection_data, indent=2)
        
        # Create summary for agent
        summary = f"""🤔 Reflection recorded ({context or 'general'} context)

{' '.join(key_points) if key_points else '✓ Strategic thinking captured'}

Key themes: {', '.join([context] if context else ['progress review', 'planning'])}
Word count: {reflection_data['metadata']['word_count']}

File: {filename}
💡 Use read_file('{filename}') to review this reflection later."""
        
        logger.info(f"Recorded reflection to {filename} ({len(reflection)} chars)")
        
        return Command(
            update={
                "files": files,
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error recording reflection: {e}")
        error_summary = f"""❌ Failed to record reflection

Error: {str(e)}

The reflection was not saved, but you can continue with your analysis."""
        
        return Command(
            update={
                "messages": [ToolMessage(error_summary, tool_call_id=tool_call_id)]
            }
        )


@tool(parse_docstring=True)
def review_reflections(
    state: Annotated[DeepAgentState, InjectedState],
    tool_call_id: Annotated[str, InjectedToolCallId],
    context_filter: Optional[str] = None,
    limit: int = 5,
) -> Command:
    """Review previous reflections to understand thinking progression.
    
    This tool helps you look back at your strategic thinking and decision-making
    process throughout the troubleshooting workflow. Use it to maintain context
    and ensure consistency in your approach.
    
    Args:
        state: Injected agent state for file access
        tool_call_id: Injected tool call identifier
        context_filter: Optional filter by context (e.g., "diagnosis", "remediation")
        limit: Maximum number of reflections to review (default: 5, max: 10)
        
    Returns:
        Command with summary of recent reflections
    """
    try:
        files = state.get("files", {})
        
        # Find reflection files
        reflection_files = [
            f for f in files.keys() 
            if f.startswith("reflections/") and f.endswith(".json")
        ]
        
        # Sort by filename (which includes timestamp) for chronological order
        reflection_files.sort(reverse=True)  # Most recent first
        
        # Apply context filter if specified
        if context_filter:
            filtered_files = []
            for file in reflection_files:
                try:
                    content = json.loads(files[file])
                    if content.get("context") == context_filter:
                        filtered_files.append(file)
                except:
                    continue
            reflection_files = filtered_files
        
        # Limit the number of reflections
        reflection_files = reflection_files[:min(limit, 10)]
        
        if not reflection_files:
            summary = f"""No reflections found{f' for context: {context_filter}' if context_filter else ''}.

Use think_tool() to record your strategic thinking and planning."""
        else:
            summaries = []
            for file in reflection_files:
                try:
                    content = json.loads(files[file])
                    timestamp = content.get("timestamp", "Unknown time")
                    context = content.get("context", "general")
                    reflection_preview = content.get("reflection", "")[:200]
                    if len(content.get("reflection", "")) > 200:
                        reflection_preview += "..."
                    
                    summaries.append(f"""📝 {context} ({timestamp})
   {reflection_preview}
   File: {file}""")
                except:
                    continue
            
            summary = f"""📚 Found {len(reflection_files)} reflection(s){f' for context: {context_filter}' if context_filter else ''}:

{chr(10).join(summaries)}

💡 Use read_file() on any file to see the full reflection."""
        
        return Command(
            update={
                "messages": [ToolMessage(summary, tool_call_id=tool_call_id)]
            }
        )
        
    except Exception as e:
        logger.error(f"Error reviewing reflections: {e}")
        error_summary = f"""❌ Failed to review reflections

Error: {str(e)}"""
        
        return Command(
            update={
                "messages": [ToolMessage(error_summary, tool_call_id=tool_call_id)]
            }
        )

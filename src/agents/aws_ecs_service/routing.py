"""Simplified routing logic for ECS Deep Agent.

This module implements a simple state machine for agent routing,
preventing infinite loops through proper state tracking.
"""

import logging
from typing import Literal

from .state import ECSDeepAgentState

logger = logging.getLogger(__name__)


def supervisor_router(
    state: ECSDeepAgentState,
) -> Literal["contextualizer", "operations", "__end__"]:
    """Simple router that prevents infinite loops.
    
    Core routing logic:
    1. If agent is awaiting user input, end to wait for response
    2. Track processed messages to avoid reprocessing
    3. Route based on context completeness and operation status
    
    Args:
        state: Current ECS Deep Agent state
        
    Returns:
        Name of the next agent to route to
    """
    logger.info("=== ROUTING DECISION ===")
    logger.info(f"Current agent: {state.get('current_agent')}")
    logger.info(f"Awaiting user input: {state.get('awaiting_user_input')}")
    logger.info(f"Context status: {state.get('context_extraction_status')}")
    logger.info(f"Operation phase: {state.get('operation_phase')}")
    
    # Critical: If any agent is awaiting user input, end immediately
    if state.get("awaiting_user_input"):
        logger.info("Agent is awaiting user input, ending conversation")
        return "__end__"
    
    # Check message count to prevent reprocessing
    messages = state.get("messages", [])
    current_message_count = len(messages)
    processed_count = state.get("processed_message_count", 0)
    
    # If we've already processed all messages, end
    if current_message_count <= processed_count:
        logger.info("All messages already processed, ending")
        return "__end__"
    
    # Check for errors
    if state.get("error_count", 0) >= 3:
        logger.warning("Too many errors, ending conversation")
        return "__end__"
    
    # Determine routing based on context status
    context_status = state.get("context_extraction_status")
    
    # If context extraction needs user input, we should have ended above
    if context_status == "needs_input":
        logger.info("Context needs input but awaiting_user_input not set, ending anyway")
        return "__end__"
    
    # If we have complete context, go to operations
    if context_status == "complete" and state.get("ecs_context") and state.get("user_intent"):
        # Check if operations already completed
        if state.get("operation_status") == "completed":
            logger.info("Operations completed, ending")
            return "__end__"
        logger.info("Context complete, routing to operations")
        return "operations"
    
    # If context is partial or in progress, continue with contextualizer
    if context_status in ["partial", "in_progress", None]:
        # But only if we haven't just come from contextualizer
        if state.get("current_agent") == "contextualizer":
            logger.info("Just came from contextualizer, checking if it needs user input")
            # If contextualizer didn't set awaiting_user_input, something's wrong
            # End to prevent loop
            return "__end__"
        logger.info("Context incomplete, routing to contextualizer")
        return "contextualizer"
    
    # Default: end to prevent loops
    logger.info("No clear routing path, ending to prevent loops")
    return "__end__"
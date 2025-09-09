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
    """Simple router with one goal: get service name then hand off to operations.
    
    Simplified routing:
    1. No service identified → contextualizer
    2. Service identified → operations
    3. Work complete or awaiting input → end
    
    Args:
        state: Current ECS Deep Agent state
        
    Returns:
        Name of the next agent to route to
    """
    logger.info("=== ROUTING DECISION ===")
    logger.info(f"Current agent: {state.get('current_agent')}")
    logger.info(f"Awaiting user input: {state.get('awaiting_user_input')}")
    
    # Check message count to see if we have new messages
    messages = state.get("messages", [])
    current_message_count = len(messages)
    processed_count = state.get("processed_message_count", 0)
    has_new_messages = current_message_count > processed_count
    
    if has_new_messages:
        logger.info(f"New messages detected: {current_message_count} total, {processed_count} processed")
    else:
        # No new messages - check if we're waiting for input
        if state.get("awaiting_user_input"):
            logger.info("Awaiting user input and no new messages, ending")
            return "__end__"
        logger.info("No new messages to process, ending")
        return "__end__"
    
    # Check for errors
    if state.get("error_count", 0) >= 3:
        logger.warning("Too many errors, ending conversation")
        return "__end__"
    
    # SIMPLIFIED ROUTING LOGIC
    # Key decision: Do we know which ECS service to work with?
    ecs_context = state.get("ecs_context", {})
    has_service = bool(ecs_context and ecs_context.get("service"))
    
    if has_service:
        # We have the service - go to operations (unless already completed)
        if state.get("operation_status") == "completed":
            logger.info("Operations completed, ending")
            return "__end__"
        logger.info(f"Service identified: {ecs_context.get('service')}. Routing to operations")
        return "operations"
    else:
        # No service yet - need contextualizer (but prevent loops)
        if state.get("current_agent") == "contextualizer":
            # Just came from contextualizer - it should have set awaiting_user_input
            # If not, end to prevent loop
            if not state.get("awaiting_user_input"):
                logger.warning("Contextualizer didn't identify service or request input, ending to prevent loop")
                return "__end__"
            return "__end__"
        logger.info("Service not identified, routing to contextualizer")
        return "contextualizer"
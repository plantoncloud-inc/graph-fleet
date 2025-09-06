"""ECS Deep Agent Graph Implementation for LangGraph Studio

This module creates an ECS DeepAgent with MCP tools for LangGraph Studio deployment.
Implements a single-node flow with ECS diagnostic and repair capabilities.

The graph is organized as:
- Single node: ECS DeepAgent execution with AWS ECS MCP tools
- Configuration: Handles write permissions and AWS credentials
- Session management: Handles MCP clients and agent lifecycle
"""

import logging
import os
from typing import Optional, Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from deepagents import async_create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver

from .configuration import ECSDeepAgentConfig
from .state import ECSDeepAgentState
from .mcp_tools import get_mcp_tools, get_interrupt_config
from .prompts import ORCHESTRATOR_PROMPT
from .subagents import SUBAGENTS

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def ecs_deep_agent_node(state: ECSDeepAgentState, config: ECSDeepAgentConfig) -> ECSDeepAgentState:
    """Main ECS Deep Agent node that processes conversational user requests.
    
    This node creates a conversational deep agent with ECS MCP tools and processes
    natural language requests for ECS service diagnosis and repair. It initializes
    conversation context and coordinates between specialized subagents.
    
    Args:
        state: Current state with messages, conversation context, and configuration
        config: Agent configuration including write permissions
        
    Returns:
        Updated state with agent response and enhanced conversation context
    """
    logger.info("Starting conversational ECS Deep Agent node")
    
    # Initialize conversation context if not present
    if not state.get("conversation_context"):
        state["conversation_context"] = {}
    if not state.get("conversation_history"):
        state["conversation_history"] = []
    if not state.get("conversation_session_id"):
        import uuid
        state["conversation_session_id"] = str(uuid.uuid4())
    
    # Initialize conversation flow state
    if not state.get("conversation_flow_state"):
        state["conversation_flow_state"] = "context_extraction"
    
    # Extract user preferences from config and state
    user_preferences = state.get("user_preferences", {})
    if config.cluster:
        user_preferences["default_cluster"] = config.cluster
    if config.service:
        user_preferences["default_service"] = config.service
    if config.aws_region:
        user_preferences["default_region"] = config.aws_region
    
    # Update state with user preferences
    state["user_preferences"] = user_preferences
    
    # Determine write permissions
    env_allow_write = os.environ.get("ALLOW_WRITE", "false").lower() == "true"
    config_allow_write = config.allow_write
    read_only = not (env_allow_write and config_allow_write)
    
    logger.info(f"Write permissions: env={env_allow_write}, config={config_allow_write}, read_only={read_only}")
    logger.info(f"Conversation session: {state.get('conversation_session_id')}")
    logger.info(f"Flow state: {state.get('conversation_flow_state')}")
    
    try:
        # Get MCP tools with appropriate permissions
        mcp_tools = await get_mcp_tools(read_only=read_only)
        
        # Get interrupt configuration for write tools
        interrupt_config = get_interrupt_config(mcp_tools) if not read_only else {}
        
        # Prepare enhanced context for the deep agent
        enhanced_messages = state["messages"].copy()
        
        # Add conversation context to the latest message if it's from the user
        if enhanced_messages and enhanced_messages[-1].get("role") == "user":
            latest_message = enhanced_messages[-1]
            
            # Enhance the message with conversation context
            context_info = []
            if state.get("conversation_history"):
                context_info.append(f"Previous conversation context available ({len(state['conversation_history'])} interactions)")
            if state.get("cluster") or state.get("service"):
                context_info.append(f"Known ECS context: cluster={state.get('cluster', 'unknown')}, service={state.get('service', 'unknown')}")
            if state.get("problem_description"):
                context_info.append(f"Previous problem: {state['problem_description']}")
            if state.get("conversation_flow_state"):
                context_info.append(f"Current phase: {state['conversation_flow_state']}")
            
            if context_info:
                enhanced_content = f"{latest_message['content']}\n\n[Conversation Context: {'; '.join(context_info)}]"
                enhanced_messages[-1] = {**latest_message, "content": enhanced_content}
        
        # Create the conversational deep agent with updated subagents
        agent = await async_create_deep_agent(
            tools=mcp_tools,
            instructions=ORCHESTRATOR_PROMPT,
            subagents=SUBAGENTS,  # Now includes context-extractor, conversation-coordinator, and enhanced subagents
            interrupt_config=interrupt_config,
            model=config.model_name
        )
        
        # Attach in-memory checkpointer for HITL
        agent.checkpointer = InMemorySaver()
        
        # Process the conversational user message
        result = await agent.ainvoke(
            {"messages": enhanced_messages},
            config={"configurable": {"thread_id": state.get("conversation_session_id", "default")}}
        )
        
        # Extract conversation insights from the response
        response_messages = result.get("messages", [])
        if response_messages:
            latest_response = response_messages[-1]
            response_content = latest_response.get("content", "")
            
            # Update conversation context based on response patterns
            if "cluster" in response_content.lower() and not state.get("cluster"):
                # Try to extract cluster name from response
                import re
                cluster_match = re.search(r'cluster[:\s]+([a-zA-Z0-9\-_]+)', response_content, re.IGNORECASE)
                if cluster_match:
                    state["cluster"] = cluster_match.group(1)
            
            if "service" in response_content.lower() and not state.get("service"):
                # Try to extract service name from response
                service_match = re.search(r'service[:\s]+([a-zA-Z0-9\-_]+)', response_content, re.IGNORECASE)
                if service_match:
                    state["service"] = service_match.group(1)
        
        # Update conversation history
        conversation_entry = {
            "timestamp": logger.info.__globals__.get("time", __import__("time")).time(),
            "user_message": state["messages"][-1] if state["messages"] else None,
            "agent_response": response_messages[-1] if response_messages else None,
            "flow_state": state.get("conversation_flow_state"),
            "extracted_context": {
                "cluster": state.get("cluster"),
                "service": state.get("service"),
                "region": state.get("region")
            }
        }
        
        conversation_history = state.get("conversation_history", [])
        conversation_history.append(conversation_entry)
        state["conversation_history"] = conversation_history
        
        # Update conversation flow state based on response content
        if response_messages:
            response_content = response_messages[-1].get("content", "").lower()
            if "triage" in response_content or "diagnosing" in response_content:
                state["conversation_flow_state"] = "triage"
            elif "plan" in response_content or "planning" in response_content:
                state["conversation_flow_state"] = "planning"
            elif "executing" in response_content or "implementing" in response_content:
                state["conversation_flow_state"] = "execution"
            elif "verifying" in response_content or "checking" in response_content:
                state["conversation_flow_state"] = "verification"
            elif "report" in response_content or "summary" in response_content:
                state["conversation_flow_state"] = "reporting"
        
        # Update state with enhanced conversational response
        updated_state = {
            **state,
            "messages": result["messages"],
            "status": "completed",
            "last_user_interaction": {
                "timestamp": conversation_entry["timestamp"],
                "content": state["messages"][-1] if state["messages"] else None
            }
        }
        
        logger.info(f"Conversational ECS Deep Agent completed. Flow state: {updated_state.get('conversation_flow_state')}")
        return updated_state
        
    except Exception as e:
        logger.error(f"Error in conversational ECS Deep Agent node: {e}")
        
        # Update conversation history with error
        error_entry = {
            "timestamp": logger.info.__globals__.get("time", __import__("time")).time(),
            "user_message": state["messages"][-1] if state["messages"] else None,
            "error": str(e),
            "flow_state": state.get("conversation_flow_state")
        }
        
        conversation_history = state.get("conversation_history", [])
        conversation_history.append(error_entry)
        
        return {
            **state,
            "messages": state["messages"] + [{"role": "assistant", "content": f"I encountered an error while processing your request: {str(e)}. Please try rephrasing your request or provide more specific details about the ECS service you'd like me to help with."}],
            "status": "error",
            "error_message": str(e),
            "conversation_history": conversation_history
        }


async def graph(config: Optional[dict] = None) -> CompiledStateGraph:
    """Main graph function for LangGraph Studio
    
    This is the entry point that LangGraph Studio calls. It creates a single-node
    graph that handles ECS service diagnosis and repair.
    
    Configuration can be passed through LangGraph Studio UI:
    - model_name: LLM model to use (e.g., 'claude-3-5-sonnet-20241022')
    - allow_write: Allow write operations (default: False)
    - allow_sensitive_data: Allow sensitive data handling (default: False)
    - aws_region: AWS region to use
    - aws_profile: AWS profile to use
    
    Args:
        config: Optional configuration dictionary from LangGraph Studio
        
    Returns:
        Configured StateGraph for ECS operations
    """
    logger.info("Creating ECS Deep Agent graph")
    
    # Create configuration
    agent_config = ECSDeepAgentConfig(**(config or {}))
    
    # Create the state graph
    workflow = StateGraph(ECSDeepAgentState)
    
    # Add the main ECS agent node
    workflow.add_node(
        "ecs_agent", 
        lambda state: ecs_deep_agent_node(state, agent_config)
    )
    
    # Set entry point and exit
    workflow.set_entry_point("ecs_agent")
    workflow.add_edge("ecs_agent", END)
    
    # Compile the graph
    compiled_graph = workflow.compile()
    
    logger.info("ECS Deep Agent graph created successfully")
    return compiled_graph


async def create_ecs_deep_agent(
    config: Optional[ECSDeepAgentConfig] = None,
    cluster: Optional[str] = None,
    service: Optional[str] = None,
    allow_write: bool = False
) -> CompiledStateGraph:
    """Create an ECS Deep Agent for examples and CLI demos
    
    This function is specifically for running examples and quick demos outside
    of LangGraph Studio. It wraps the main graph() function for standalone use.
    
    Args:
        config: Full agent configuration (optional)
        cluster: ECS cluster name for operations
        service: ECS service name for operations  
        allow_write: Whether to allow write operations
        
    Returns:
        Compiled StateGraph for ECS operations
        
    Example:
        >>> agent = await create_ecs_deep_agent(
        ...     cluster="my-cluster", 
        ...     service="my-service",
        ...     allow_write=True
        ... )
        >>> result = await agent.ainvoke({
        ...     "messages": [{"role": "user", "content": "Diagnose this ECS service"}]
        ... })
    """
    # Create config if not provided
    if config is None:
        config = ECSDeepAgentConfig()
    
    # Apply runtime overrides
    config.allow_write = allow_write
    
    # Convert config to dict for graph function
    config_dict = config.model_dump()
    
    # Add cluster/service context if provided
    if cluster:
        config_dict["cluster"] = cluster
    if service:
        config_dict["service"] = service
    
    # Create and return the graph
    return await graph(config_dict)


# Export for LangGraph and examples
__all__ = ["graph", "create_ecs_deep_agent", "ECSDeepAgentState", "ECSDeepAgentConfig"]


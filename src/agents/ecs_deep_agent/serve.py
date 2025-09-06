"""LangGraph server module for ECS Deep Agent."""

import os
from typing import Dict, Any

from langgraph.graph import StateGraph, MessagesState
from langgraph.prebuilt import ToolNode
from langchain_core.messages import HumanMessage

from .main import create_agent


async def get_graph():
    """
    Create and return the LangGraph graph for serving.
    
    Returns:
        Compiled StateGraph instance
    """
    # Create the agent
    agent = await create_agent()
    
    # Create a state graph
    workflow = StateGraph(MessagesState)
    
    # Define the agent node
    async def agent_node(state: MessagesState) -> Dict[str, Any]:
        """Process messages through the deep agent."""
        result = await agent.ainvoke(
            state,
            config={"configurable": {"thread_id": state.get("thread_id", "default")}}
        )
        return result
    
    # Add nodes to the graph
    workflow.add_node("agent", agent_node)
    
    # Set the entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges based on agent output
    def should_continue(state: MessagesState) -> str:
        """Determine if we should continue or end."""
        # Check if there are tool calls pending
        messages = state.get("messages", [])
        if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
            return "tools"
        return "end"
    
    # Add conditional edge
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "agent",  # Loop back if tools need to be called
            "end": None  # End the graph
        }
    )
    
    # Compile the graph
    return workflow.compile()


# Export the graph for LangGraph server
graph = None


def initialize_graph():
    """Initialize the graph synchronously for module-level export."""
    import asyncio
    
    async def _init():
        global graph
        graph = await get_graph()
        return graph
    
    # Run the async initialization
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(_init())


# Initialize on module load
if __name__ != "__main__":
    # Only initialize when imported, not when run directly
    graph = initialize_graph()


if __name__ == "__main__":
    # For testing the server locally
    import uvicorn
    from langgraph.server import create_server
    
    async def main():
        """Run the LangGraph server."""
        graph_instance = await get_graph()
        
        # Create server app
        app = create_server(graph_instance)
        
        # Run the server
        config = uvicorn.Config(
            app,
            host="127.0.0.1",
            port=2024,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()
    
    import asyncio
    asyncio.run(main())

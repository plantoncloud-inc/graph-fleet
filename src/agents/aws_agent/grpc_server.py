"""gRPC Server for AWS Agent

This module implements the gRPC service for invoking the AWS agent graph.
It follows the protobuf contract defined in the Planton Cloud APIs.
"""

import asyncio
from typing import AsyncGenerator, Any
from concurrent import futures
import grpc
from langchain_core.messages import HumanMessage, AIMessage
from cloud.planton.apis.agentfleet.agents.aws.v1 import (
        graph_pb2_grpc,
        io_pb2,
        spec_pb2
)
from .graph import async_create_aws_agent_graph
from .configuration import AWSAgentConfig


class AwsAgentGraphControllerServicer(graph_pb2_grpc.AwsAgentGraphControllerServicer):
    """gRPC service implementation for AWS Agent Graph Controller"""
    
    def __init__(self):
        """Initialize the servicer"""
        self.agents = {}  # Cache for agent instances per configuration
    
    async def Invoke(
        self, 
        request, 
        context
    ) -> AsyncGenerator:
        """Invoke the AWS agent graph and stream events
        
        Args:
            request: AwsAgentGraphInvokeInput with assistant_id, session_id, input, config
            context: gRPC context
            
        Yields:
            AwsAgentGraphInvokeEvent stream
        """
        try:
            # Emit start event
            yield self._create_event(progress="started")
            
            # Parse configuration if provided
            config = AWSAgentConfig()
            if request.config_overwrite:
                config.model_name = request.config_overwrite.model_name or config.model_name
                config.instructions = request.config_overwrite.instructions or config.instructions
                # Note: MCP servers are now default only, customization will be added later
            
            # Create or get cached agent
            agent_key = f"{request.assistant_id}_{config.model_name}"
            if agent_key not in self.agents:
                # Use async version for MCP integration
                self.agents[agent_key] = await async_create_aws_agent_graph(config)
            agent = self.agents[agent_key]
            
            # Prepare initial state
            initial_state = {
                "messages": [],
                "aws_credential_id": request.input.aws_credential_id,
                "aws_region": request.input.aws_region,
                "session_id": request.session_id,
                "assistant_id": request.assistant_id,
                "step_count": 0,
                "max_steps": 10
            }
            
            # Add input messages
            if request.input.messages:
                for msg in request.input.messages:
                    initial_state["messages"].append(HumanMessage(content=msg))
            
            # Emit progress
            yield self._create_event(progress="processing")
            
            # Invoke the DeepAgent
            # DeepAgents handle streaming differently - they emit events for planning, sub-agents, etc.
            async for chunk in agent.astream(initial_state, stream_mode="values"):
                if "messages" in chunk:
                    # Process messages from the agent
                    messages = chunk.get("messages", [])
                    if messages:
                        last_msg = messages[-1]
                        
                        # Emit different progress based on message type
                        if hasattr(last_msg, 'tool_calls') and last_msg.tool_calls:
                            # Agent is calling a tool (could be todo list, sub-agent, etc.)
                            tool_name = last_msg.tool_calls[0].get("name", "unknown")
                            yield self._create_event(progress=f"tool:{tool_name}")
                        
                        elif isinstance(last_msg, AIMessage):
                            # Agent response
                            output = spec_pb2.AwsAgentStateOutput()
                            output.messages.append(last_msg.content)
                            yield self._create_event(output=output)
                        
                        # Track planning progress
                        if "todo" in str(last_msg).lower():
                            yield self._create_event(progress="planning")
                        elif "subagent" in str(last_msg).lower():
                            yield self._create_event(progress="spawning_subagent")
            
            # Emit completion
            yield self._create_event(progress="completed", done=True)
            
        except Exception as e:
            # Emit error
            yield self._create_event(
                error=f"Agent invocation failed: {str(e)}",
                done=True
            )
    
    def _create_event(
        self,
        progress: str = None,
        output: Any = None,
        error: str = None,
        done: bool = False
    ):
        """Create an AwsAgentGraphInvokeEvent
        
        Args:
            progress: Progress message
            output: Output payload
            error: Error message
            done: Whether this is the final event
            
        Returns:
            AwsAgentGraphInvokeEvent
        """
        event = io_pb2.AwsAgentGraphInvokeEvent()
        
        if progress:
            event.progress_event = progress
        elif output:
            event.output.CopyFrom(output)
        elif error:
            event.error_message = error
        
        event.done = done
        return event


async def serve(port: int = 50051):
    """Start the gRPC server
    
    Args:
        port: Port to listen on (default: 50051)
    """
    server = grpc.aio.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    
    # Add the servicer
    servicer = AwsAgentGraphControllerServicer()
    graph_pb2_grpc.add_AwsAgentGraphControllerServicer_to_server(
        servicer, server
    )
    
    # Listen on the specified port
    server.add_insecure_port(f'[::]:{port}')
    
    print(f"Starting AWS Agent gRPC server on port {port}")
    await server.start()
    
    try:
        await server.wait_for_termination()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        await server.stop(5)


def main():
    """Main entry point for the gRPC server"""
    asyncio.run(serve())


if __name__ == "__main__":
    main()

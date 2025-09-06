"""Main entry point and agent creation for ECS Deep Agent."""

import os
import asyncio
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

import click
from deepagents import async_create_deep_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from .prompts import ORCHESTRATOR_PROMPT
from .subagents import SUBAGENTS
from .mcp_tools import get_mcp_tools, get_interrupt_config


async def create_checkpointer():
    """Create a checkpointer based on environment configuration.
    
    Checks for DATABASE_URL environment variable and creates an AsyncPostgresSaver
    if available. Falls back to InMemorySaver if DATABASE_URL is not configured
    or if there's an error connecting to PostgreSQL.
    
    Returns:
        Checkpointer instance (AsyncPostgresSaver or InMemorySaver)
    """
    database_url = os.environ.get("DATABASE_URL")
    
    if not database_url:
        print("DATABASE_URL not configured, using InMemorySaver for checkpointing")
        return InMemorySaver()
    
    try:
        print("DATABASE_URL found, attempting to create PostgreSQL checkpointer")
        checkpointer = AsyncPostgresSaver.from_conn_string(database_url)
        
        # Setup the checkpointer (creates tables if they don't exist)
        await checkpointer.setup()
        
        print("PostgreSQL checkpointer created successfully")
        return checkpointer
        
    except Exception as e:
        print(f"Failed to create PostgreSQL checkpointer: {e}")
        print("Falling back to InMemorySaver for checkpointing")
        return InMemorySaver()


def load_config() -> Dict[str, Any]:
    """Load agent configuration from agent.yaml."""
    config_path = Path(__file__).parent / "agent.yaml"
    
    if not config_path.exists():
        # Return defaults if config doesn't exist
        return {
            "model": "claude-3-5-sonnet-20241022",
            "allowWrite": False,
            "allowSensitiveData": False,
            "region": "",
            "profile": ""
        }
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)


async def create_agent(allow_write_override: Optional[bool] = None):
    """
    Create the ECS Deep Agent with MCP tools and sub-agents.
    
    Args:
        allow_write_override: Optional override for write permissions from CLI
    
    Returns:
        Configured deep agent instance
    """
    # Load configuration
    config = load_config()
    
    # Determine write permissions
    env_allow_write = os.environ.get("ALLOW_WRITE", "false").lower() == "true"
    config_allow_write = config.get("allowWrite", False)
    
    # Use CLI override if provided, otherwise AND the env and config values
    if allow_write_override is not None:
        read_only = not allow_write_override
    else:
        read_only = not (env_allow_write and config_allow_write)
    
    # Get MCP tools with appropriate permissions
    mcp_tools = await get_mcp_tools(read_only=read_only)
    
    # Get interrupt configuration for write tools
    interrupt_config = get_interrupt_config(mcp_tools) if not read_only else {}
    
    # Create the deep agent
    agent = await async_create_deep_agent(
        tools=mcp_tools,
        instructions=ORCHESTRATOR_PROMPT,
        subagents=SUBAGENTS,
        interrupt_config=interrupt_config,
        model=config.get("model", "claude-3-5-sonnet-20241022")
    )
    
    # Attach postgres checkpointer for HITL (falls back to InMemorySaver if not configured)
    agent.checkpointer = await create_checkpointer()
    
    return agent


async def run_agent(message: str, allow_write: bool = False):
    """
    Run the agent with a user message.
    
    Args:
        message: User message to process
        allow_write: Whether to allow write operations
    
    Returns:
        Agent response
    """
    agent = await create_agent(allow_write_override=allow_write)
    
    # Invoke the agent with the message
    result = await agent.ainvoke(
        {"messages": [{"role": "user", "content": message}]},
        config={"configurable": {"thread_id": "default"}}
    )
    
    return result


@click.group()
def cli():
    """ECS Deep Agent CLI for diagnosing and repairing ECS services."""
    pass


@cli.command()
@click.option('--cluster', required=True, help='ECS cluster ID')
@click.option('--service', required=True, help='ECS service name')
def triage(cluster: str, service: str):
    """Run read-only triage on an ECS service."""
    message = f"Diagnose service {service} in cluster {cluster}. Start read-only triage and write triage_report.md."
    
    async def run():
        result = await run_agent(message, allow_write=False)
        print("Triage complete. Check triage_report.md for results.")
        return result
    
    asyncio.run(run())


@cli.command()
@click.option('--cluster', required=True, help='ECS cluster ID')
@click.option('--service', required=True, help='ECS service name')
@click.option('--allow-write', is_flag=True, help='Allow write operations (requires approval)')
def loop(cluster: str, service: str, allow_write: bool):
    """Run the full diagnostic and repair loop."""
    message = f"Fix service {service} in cluster {cluster}. Follow plan, ask for approval on writes, and produce Markdown artifacts."
    
    async def run():
        result = await run_agent(message, allow_write=allow_write)
        print("Loop complete. Check report_summary.md for results.")
        return result
    
    asyncio.run(run())


if __name__ == "__main__":
    cli()




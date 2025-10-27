"""Main graph for AWS RDS manifest generator agent."""

from .agent import create_rds_agent

# Export the compiled graph for LangGraph
graph = create_rds_agent()



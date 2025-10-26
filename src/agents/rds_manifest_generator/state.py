"""State schema for the RDS manifest generator agent."""

from typing import Annotated, TypedDict

from langgraph.graph import add_messages


class RdsManifestState(TypedDict):
    """State for RDS manifest generation agent.

    Attributes:
        messages: Conversation messages between user and agent
        collected_requirements: User responses to questions (field_name -> value mapping)
        manifest_draft: Generated YAML manifest (populated in Phase 3)
    """

    messages: Annotated[list, add_messages]
    collected_requirements: dict
    manifest_draft: str | None


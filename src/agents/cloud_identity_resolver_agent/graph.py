"""Graph builder for the Identity Resolver agent."""

from __future__ import annotations

from langgraph.graph import StateGraph

from .nodes import collect_mentions, resolve_identities
from .state import InputState, State
from .configuration import Configuration

builder = StateGraph(State, input_schema=InputState,context_schema=Configuration)
builder.add_node("collect_mentions", collect_mentions)
builder.add_node("resolve_identities", resolve_identities)
builder.add_edge("__start__", "collect_mentions")
builder.add_edge("collect_mentions", "resolve_identities")
builder.add_edge("resolve_identities", "__end__")

graph = builder.compile(name="Cloud Identity Resolver Agent")



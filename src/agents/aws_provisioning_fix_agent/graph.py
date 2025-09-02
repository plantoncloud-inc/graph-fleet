"""Graph builder for the AWS Provisioning Fix agent."""

from __future__ import annotations

from langgraph.graph import StateGraph

from .nodes import plan, diagnose, propose_fixes, apply_fixes
from .state import InputState, State
from .configuration import Configuration


builder = StateGraph(State, input_schema=InputState, context_schema=Configuration)
builder.add_node("plan", plan)
builder.add_node("diagnose", diagnose)
builder.add_node("propose_fixes", propose_fixes)
builder.add_node("apply_fixes", apply_fixes)

builder.add_edge("__start__", "plan")
builder.add_edge("plan", "diagnose")
builder.add_edge("diagnose", "propose_fixes")
builder.add_edge("propose_fixes", "apply_fixes")
builder.add_edge("apply_fixes", "__end__")

graph = builder.compile(name="AWS Provisioning Fix Agent")



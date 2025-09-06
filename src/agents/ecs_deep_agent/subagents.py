"""Sub-agent definitions for ECS Deep Agent."""

from .prompts import (
    CONTEXT_EXTRACTOR_PROMPT,
    TRIAGE_AGENT_PROMPT,
    CHANGE_PLANNER_PROMPT,
    REMEDIATOR_PROMPT,
    VERIFIER_PROMPT,
    CONVERSATION_COORDINATOR_PROMPT,
    REPORTER_PROMPT
)

SUBAGENTS = [
    {
        "name": "context-extractor",
        "description": "Parses natural language messages to extract ECS context, problem descriptions, and user intent",
        "prompt": CONTEXT_EXTRACTOR_PROMPT
    },
    {
        "name": "conversation-coordinator",
        "description": "Manages flow between subagents based on conversational context, handles follow-up questions, and maintains conversation state across multiple interactions",
        "prompt": CONVERSATION_COORDINATOR_PROMPT
    },
    {
        "name": "triage-agent",
        "description": "Diagnoses ECS service issues using read-only tools",
        "prompt": TRIAGE_AGENT_PROMPT
    },
    {
        "name": "change-planner",
        "description": "Creates minimal, reversible repair plans",
        "prompt": CHANGE_PLANNER_PROMPT
    },
    {
        "name": "remediator",
        "description": "Executes approved repair steps with minimal blast radius",
        "prompt": REMEDIATOR_PROMPT
    },
    {
        "name": "verifier",
        "description": "Verifies service health after changes",
        "prompt": VERIFIER_PROMPT
    },
    {
        "name": "reporter",
        "description": "Summarizes actions and results for audit",
        "prompt": REPORTER_PROMPT
    }
]





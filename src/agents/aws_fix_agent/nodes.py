"""Graph node implementations for the AWS Fix agent."""

from __future__ import annotations

import json
from typing import Any

from langgraph.types import Command

from .configuration import Configuration
from .state import State
from .llm_utils import load_chat_model


def plan(state: State) -> Command[Any]:
    cfg = Configuration.from_context()
    model = load_chat_model(cfg.llm_model, temperature=0)

    conversation = "\n".join(str(m.get("content", "")) for m in state.messages)
    sys = (
        "You are an AWS provisioning incident agent. Create a short ordered plan to "
        "diagnose and fix the user's issue. Prefer read-only steps first, then propose "
        "safe, minimal changes requiring approval. Output JSON with keys: plan[]."
    )
    user = f"Conversation:\n{conversation}\nReturn JSON only."

    try:
        from langchain_core.messages import HumanMessage, SystemMessage

        out = model.invoke([SystemMessage(content=sys), HumanMessage(content=user)])
        content = getattr(out, "content", "{}")
        data = json.loads(content)
        steps = data.get("plan", [])
    except Exception:
        steps = [
            {"action": "gather_context", "desc": "List recent failed stack jobs and errors"},
            {"action": "diagnose", "desc": "Check AWS resource states and dependencies"},
            {"action": "propose_fix", "desc": "Suggest minimal fix and request approval"},
        ]

    return Command(goto="diagnose", update={"plan": steps})


def diagnose(state: State) -> Command[Any]:
    findings = [
        {"type": "stub", "detail": "Diagnosis via MCP not yet implemented."}
    ]
    return Command(goto="propose_fixes", update={"findings": findings})


def propose_fixes(state: State) -> Command[Any]:
    cfg = Configuration.from_context()
    model = load_chat_model(cfg.llm_model, temperature=0)

    findings_text = json.dumps(state.findings)
    sys = (
        "Given AWS provisioning findings, propose minimal and safe fixes. Each fix must "
        "describe the change and the exact AWS action required (service, operation, args). "
        "Output JSON with key 'fixes' as a list."
    )
    user = f"Findings: {findings_text}\nReturn JSON only."

    try:
        from langchain_core.messages import HumanMessage, SystemMessage

        out = model.invoke([SystemMessage(content=sys), HumanMessage(content=user)])
        content = getattr(out, "content", "{}")
        data = json.loads(content)
        fixes = data.get("fixes", [])
    except Exception:
        fixes = [
            {
                "title": "Retry failed CloudFormation stack",
                "tool": "apply_fix",
                "args": {"service": "cloudformation", "operation": "update_stack", "params": {}},
            }
        ]

    return Command(goto="apply_fixes", update={"proposed_fixes": fixes})


def apply_fixes(state: State) -> Command[Any]:
    applied = []
    for fix in state.proposed_fixes:
        applied.append({"fix": fix, "status": "pending (requires MCP integration)"})

    messages = list(state.messages) + [
        {
            "role": "assistant",
            "content": (
                "Proposed fixes are ready for approval. No changes made yet."
            ),
        }
    ]
    return Command(goto="__end__", update={"applied_changes": applied, "messages": messages})



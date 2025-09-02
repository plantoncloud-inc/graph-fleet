"""Graph node implementations for the Identity Resolver agent."""

from __future__ import annotations

import json
import re
from typing import Any

from langgraph.types import Command

from .configuration import Configuration
from .state import State
from .llm_utils import load_chat_model
from .utils import extract_candidate_ids, load_valid_prefixes
from .message_utils import messages_to_conversation_text

ID_PATTERN = re.compile(r"\b([a-z0-9]+_[a-z0-9_\-]+)\b", re.IGNORECASE)


def collect_mentions(state: State) -> Command[Any]:
    """Collect identity mentions (IDs/names) from the input messages."""
    text = messages_to_conversation_text(state.messages)
    # 1) Try regex-based candidates with optional prefix allowlist
    allowed = load_valid_prefixes()
    ids = extract_candidate_ids(text, allowed_prefixes=allowed or None)
    names: list[str] = []  # future: LLM aided extraction for plain names

    mentions: list[str] = []
    seen = set()
    for m in [*ids, *names]:
        m_norm = m.strip()
        if not m_norm or m_norm in seen:
            continue
        seen.add(m_norm)
        mentions.append(m_norm)

    if not mentions:
        return Command(
            goto="__end__",
            update={
                "messages": state.messages
                + [
                    {
                        "role": "assistant",
                        "content": "No identifiable resource references found. Please provide IDs or names.",
                    }
                ],
            },
        )

    # Pass mentions onward. Selection happens in resolve_identities via LLM.
    return Command(goto="resolve_identities", update={"mentions": mentions})


def resolve_identities(
    state: State, config: dict[str, object] | None = None
) -> Command[Any]:
    """Use LLM to select relevant IDs from mentions based on conversation context."""
    # Start with env-backed defaults then overlay Studio-configurable values
    _cfg = Configuration.from_context()
    if config and "llm_model" in config:
        _cfg.llm_model = str(config["llm_model"])  # mypy: ignore[assignment]

    mentions: list[str] = list(state.mentions)
    conversation = messages_to_conversation_text(state.messages)

    def _heuristic_select_by_cues(text: str, options: list[str]) -> list[str]:
        text_l = text.lower()
        # Order cues: first/second/third
        order_map = {"first": 0, "1st": 0, "second": 1, "2nd": 1, "third": 2, "3rd": 2}
        for cue, idx in order_map.items():
            if cue in text_l and idx < len(options):
                return [options[idx]]
        # Starts-with cue: "starts with 'a'" or similar
        m = re.search(r"start(?:s|ing)?\s+with\s+'?([a-z0-9_])", text_l)
        if m:
            ch = m.group(1)
            by_char = [o for o in options if o.startswith(ch)]
            if by_char:
                return by_char
        return []

    def _llm_select_ids(
        messages: list[object], candidates: list[str]
    ) -> list[str]:
        try:
            from langchain_core.messages import HumanMessage, SystemMessage
        except Exception:
            return []

        if not candidates:
            return []

        sys = (
            "You select relevant Planton Cloud resource IDs from a conversation. "
            "Use only IDs provided in the candidate list. Consider conversational cues "
            "like order (first/second/third), explicit references (starts with 'a'), or direct mentions. "
            'Return strictly JSON as {"selected_ids": ["id", ...]} with zero commentary.'
        )
        conv_text = messages_to_conversation_text(messages)
        user = (
            "Conversation:\n"
            + conv_text
            + "\n\nCandidates (JSON array):\n"
            + json.dumps(candidates)
            + "\n\nRules:\n- Choose only from candidates.\n- If ambiguous, choose the most likely single ID.\n- If the user references order, respect the order in the conversation text.\n\n"
            "Respond with valid JSON only."
        )

        try:
            # Only support OpenAI models per request
            model = _cfg.llm_model or "gpt-4o-mini"
            llm_obj = load_chat_model(model, temperature=0)
            out = llm_obj.invoke(
                [SystemMessage(content=sys), HumanMessage(content=user)]
            )
            text = getattr(out, "content", "") or "{}"
            data = json.loads(text)
            ids = data.get("selected_ids", [])
            return [i for i in ids if i in candidates]
        except Exception:
            return []

    candidate_ids = [m for m in mentions if "_" in m]
    selected = _llm_select_ids(state.messages, candidate_ids)
    if not selected:
        selected = _heuristic_select_by_cues(conversation, candidate_ids)
    if not selected:
        selected = candidate_ids

    content = (
        "Selected resource ID(s):\n" + "\n".join(f"- {rid}" for rid in selected)
        if selected
        else "I could not determine a specific ID from the conversation."
    )

    return Command(
        goto="__end__",
        update={
            "resolved": [{"type": "id", "value": rid} for rid in selected],
            "resource_ids": selected,
            "messages": state.messages
            + [
                {
                    "role": "assistant",
                    "content": content,
                }
            ],
        },
    )



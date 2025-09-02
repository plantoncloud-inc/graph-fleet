"""Message/Conversation utilities for the Identity Resolver agent.

These helpers normalize the various shapes of messages we may receive
({"role": ..., "content": ...} dicts, plain strings, etc.) into consistent
forms that are convenient for prompting and logging.
"""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any


def extract_text_from_message(message: Any) -> str:
    """Return the textual content of a message-like object.

    Supports:
    - Mapping with a "content" field
    - Plain strings
    - Any other object (falls back to ``str(obj)``)
    """

    if isinstance(message, dict):
        return str(message.get("content", ""))
    return str(message)


def messages_to_conversation_text(messages: Sequence[Any]) -> str:
    """Concatenate messages into a newline-separated conversation string."""

    return "\n".join(extract_text_from_message(m) for m in messages)


def messages_to_openai_chat(messages: Sequence[Any]) -> list[dict[str, str]]:
    """Convert arbitrary messages to OpenAI chat dicts.

    If a message is a mapping and provides a "role", it's preserved; otherwise,
    defaults to role="user". The content is derived via
    :func:`extract_text_from_message`.
    """

    result: list[dict[str, str]] = []
    for m in messages:
        role = "user"
        if isinstance(m, dict) and isinstance(m.get("role"), str):
            role = m["role"]
        content = extract_text_from_message(m)
        result.append({"role": role, "content": content})
    return result




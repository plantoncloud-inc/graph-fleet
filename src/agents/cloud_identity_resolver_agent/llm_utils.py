"""LLM utilities for the Identity Resolver agent.

This module centralizes creation of chat model clients so the rest of the code
can just ask for a model by name. Today we support a curated set of popular
OpenAI chat models; we can expand this list or add providers later without
touching call sites.
"""

from __future__ import annotations


_SUPPORTED_OPENAI_MODELS: set[str] = {
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
}


def load_chat_model(model_name: str, *, temperature: float = 0.0):
    """Return a chat LLM object for the given model name.

    - Supports a curated set of OpenAI chat models (see `_SUPPORTED_OPENAI_MODELS`).
    - Falls back to "gpt-4o-mini" if an unsupported name is provided.
    """

    name = (model_name or "").strip()
    if name not in _SUPPORTED_OPENAI_MODELS:
        name = "gpt-4o-mini"

    from langchain_openai import ChatOpenAI  # lazy import

    return ChatOpenAI(model=name, temperature=temperature)




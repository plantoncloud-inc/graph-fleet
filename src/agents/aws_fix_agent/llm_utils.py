"""LLM utilities shared in the AWS Fix agent."""

from __future__ import annotations

_SUPPORTED_OPENAI_MODELS: set[str] = {
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
}


def load_chat_model(model_name: str, *, temperature: float = 0.0):
    name = (model_name or "").strip()
    if name not in _SUPPORTED_OPENAI_MODELS:
        name = "gpt-4o-mini"
    from langchain_openai import ChatOpenAI

    return ChatOpenAI(model=name, temperature=temperature)



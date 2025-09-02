"""Configuration utilities for the Identity Resolver agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Literal

from langchain_core.runnables import ensure_config
from langgraph.config import get_config


@dataclass(kw_only=True)
class Configuration:
    """Runtime configuration for the resolver (Studio-configurable)."""

    api_bearer_token: str | None = field(
        default=os.getenv("PLANTON_API_BEARER_TOKEN"),
        metadata={
            "description": "Optional bearer token for future real backends.",
        },
    )

    # Primary Studio-configurable field (OpenAI models dropdown)
    llm_model: Annotated[
        Literal["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
        {"description": "OpenAI chat model to use (popular options shown)."},
    ] = field(default="gpt-4o-mini")

    @classmethod
    def from_context(cls) -> Configuration:
        """Create a Configuration instance from LangGraph's RunnableConfig."""
        try:
            cfg = get_config()
        except RuntimeError:
            cfg = None
        cfg = ensure_config(cfg)
        configurable = cfg.get("configurable") or {}
        allowed = {f.name for f in fields(cls) if f.init}
        # Overlay Studio-configurable values on top of defaults (which include env)
        return cls(**{k: v for k, v in configurable.items() if k in allowed})



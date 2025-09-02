"""Configuration utilities for the AWS Provisioning Fix agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Literal

from langchain_core.runnables import ensure_config
from langgraph.config import get_config


@dataclass(kw_only=True)
class Configuration:
    """Runtime configuration for the AWS agent (Studio-configurable)."""

    # LLM selection for planning/diagnosis
    llm_model: Annotated[
        Literal["gpt-4o-mini", "gpt-4o", "gpt-4.1-mini", "gpt-4.1"],
        {"description": "OpenAI chat model to use for reasoning."},
    ] = field(default="gpt-4o-mini")

    # Human-in-loop gating
    require_approval_for_changes: bool = field(
        default=True, metadata={"description": "Require approval before modifying AWS state."}
    )

    # MCP server connection details (optional override via Studio config)
    aws_mcp_server: str | None = field(
        default=os.getenv("AWS_MCP_SERVER"),
        metadata={"description": "MCP server identifier or URL for AWS."},
    )

    # Optional: named profile or static creds provided to the AWS MCP server
    aws_profile: str | None = field(
        default=os.getenv("AWS_PROFILE"),
        metadata={"description": "AWS profile to use (if MCP server supports)."},
    )

    def as_interrupt_config(self) -> dict[str, object]:
        """Return interrupt configuration for tools that change cloud state."""
        if self.require_approval_for_changes:
            return {"apply_fix": True}
        return {}

    @classmethod
    def from_context(cls) -> Configuration:
        try:
            cfg = get_config()
        except RuntimeError:
            cfg = None
        cfg = ensure_config(cfg)
        configurable = cfg.get("configurable") or {}
        allowed = {f.name for f in fields(cls) if f.init}
        return cls(**{k: v for k, v in configurable.items() if k in allowed})



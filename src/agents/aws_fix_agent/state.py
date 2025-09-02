"""Types representing the graph's input and runtime state for AWS Fix agent."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


class InputState(TypedDict):
    messages: list[dict[str, object]]
    files: dict[str, str] | None


@dataclass
class State:
    messages: list[dict[str, object]] = field(default_factory=list)
    files: dict[str, str] = field(default_factory=dict)
    plan: list[dict[str, object]] = field(default_factory=list)
    findings: list[dict[str, object]] = field(default_factory=list)
    proposed_fixes: list[dict[str, object]] = field(default_factory=list)
    applied_changes: list[dict[str, object]] = field(default_factory=list)



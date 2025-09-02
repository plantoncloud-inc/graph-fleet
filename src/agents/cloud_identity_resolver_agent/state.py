"""Types representing the graph's input and runtime state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TypedDict


class InputState(TypedDict):
    """Input schema expected by the graph."""

    messages: list[dict[str, object]]


@dataclass
class State:
    """Graph state passed between nodes during execution."""

    messages: list[dict[str, object]] = field(default_factory=list)
    mentions: list[str] = field(default_factory=list)
    resolved: list[dict[str, object]] = field(default_factory=list)



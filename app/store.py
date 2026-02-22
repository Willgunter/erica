from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class InMemoryStore:
    checkpoint_sessions: dict[str, dict[str, Any]] = field(default_factory=dict)
    test_sessions: dict[str, dict[str, Any]] = field(default_factory=dict)
    test_results: dict[str, dict[str, Any]] = field(default_factory=dict)
    summaries: dict[str, dict[str, Any]] = field(default_factory=dict)
    user_summaries: dict[str, list[str]] = field(default_factory=dict)
    lock: Lock = field(default_factory=Lock)


store = InMemoryStore()

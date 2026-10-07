"""Explicit action registration and lookup."""

from __future__ import annotations

from typing import Any, Protocol

from automation.engine.errors import ActionRegistrationError, UnknownActionError
from automation.engine.models import ActionResult, ExecutionContext, Step


class Action(Protocol):
    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        """Execute one narrowly scoped operation."""


class ActionRegistry:
    def __init__(self) -> None:
        self._actions: dict[str, Action] = {}

    def register(self, name: str, action: Action) -> None:
        if not isinstance(name, str) or not name:
            raise ActionRegistrationError("Action name must be a non-empty string")
        if name in self._actions:
            raise ActionRegistrationError(f"Action '{name}' is already registered")
        self._actions[name] = action

    def get(self, name: str) -> Action:
        try:
            return self._actions[name]
        except KeyError as exc:
            raise UnknownActionError(f"Action '{name}' is not registered") from exc

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(self._actions)

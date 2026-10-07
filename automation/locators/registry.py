"""Explicit locator strategy registration."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from automation.engine.errors import LocatorRegistrationError, TargetNotFound
from automation.engine.models import ExecutionContext
from automation.locators.models import LocatorResult


class Locator(Protocol):
    def begin(self, context: ExecutionContext) -> None:
        """Capture optional per-run state before workflow execution."""

    def locate(
        self, selector: Mapping[str, Any], context: ExecutionContext
    ) -> LocatorResult:
        """Attempt one target lookup without performing an action."""


class LocatorRegistry:
    def __init__(self) -> None:
        self._locators: dict[str, Locator] = {}

    def register(self, name: str, locator: Locator) -> None:
        if not isinstance(name, str) or not name:
            raise LocatorRegistrationError("Locator name must be a non-empty string")
        if name in self._locators:
            raise LocatorRegistrationError(f"Locator '{name}' is already registered")
        self._locators[name] = locator

    def get(self, name: str) -> Locator:
        try:
            return self._locators[name]
        except KeyError as exc:
            raise TargetNotFound(f"Locator strategy '{name}' is not registered") from exc

    @property
    def locators(self) -> tuple[Locator, ...]:
        return tuple(self._locators.values())

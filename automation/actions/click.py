"""Click exactly one resolved semantic or screen target."""

from __future__ import annotations

from typing import Any, Callable

from automation.engine.errors import ActionFailed
from automation.engine.models import ActionResult, ExecutionContext, Step
from automation.locators.models import LocatorResult


def _default_screen_click(x: int, y: int) -> None:
    import pyautogui

    pyautogui.click(x=x, y=y)


class ClickAction:
    def __init__(self, screen_click: Callable[[int, int], None] | None = None) -> None:
        self._screen_click = screen_click or _default_screen_click

    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        if not isinstance(target, LocatorResult) or not target.found or target.ambiguous:
            raise ActionFailed("Click requires one resolved, unambiguous target")
        if target.element is not None:
            try:
                target.element.iface_invoke.Invoke()
            except AttributeError as exc:
                raise ActionFailed("Resolved UIA target does not support Invoke") from exc
            message = "Invoked UIA target"
        elif target.x is not None and target.y is not None:
            try:
                self._screen_click(target.x, target.y)
            except Exception as exc:
                raise ActionFailed(f"Screen click failed: {exc}") from exc
            message = "Clicked resolved screen target"
        else:
            raise ActionFailed("Resolved click target has no semantic element or coordinates")
        return ActionResult.executed_unverified(
            message, metadata=dict(target.metadata)
        )

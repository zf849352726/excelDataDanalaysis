"""Target-bound semantic UIA actions."""

from __future__ import annotations

from typing import Any

from automation.engine.errors import ActionFailed
from automation.engine.models import ActionResult, ExecutionContext, Step
from automation.locators.models import LocatorResult


def _uia_element(target: Any | None) -> Any:
    if not isinstance(target, LocatorResult) or not target.found or target.element is None:
        raise ActionFailed("UIA action requires one resolved target")
    if target.ambiguous:
        raise ActionFailed("UIA action will not operate on an ambiguous target")
    return target.element


class TypeTextAction:
    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        element = _uia_element(target)
        text = step.parameters["text"]
        try:
            element.iface_value.SetValue(text)
        except AttributeError as exc:
            raise ActionFailed("Resolved UIA target does not support SetValue") from exc
        return ActionResult.executed_unverified(
            "Set UIA value",
            metadata={**dict(target.metadata), "text_length": len(text)},
        )


class CloseWindowAction:
    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        element = _uia_element(target)
        if element.element_info.control_type != "Window":
            raise ActionFailed("close_window requires a UIA Window target")
        element.close()
        return ActionResult.executed_unverified(
            "Requested UIA window close", metadata=dict(target.metadata)
        )

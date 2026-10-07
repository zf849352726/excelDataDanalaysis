"""Target-bound semantic UIA actions."""

from __future__ import annotations

import time
from typing import Any

from comtypes import COMError
from pywinauto.findwindows import ElementNotFoundError

from automation.engine.errors import ActionFailed, WorkflowCancelled
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
    _PROMPT_TIMEOUT_SECONDS = 1.0
    _POLL_INTERVAL_SECONDS = 0.05

    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        element = _uia_element(target)
        control_type = element.element_info.control_type
        automation_id = getattr(element.element_info, "automation_id", "")
        root = element if control_type == "Window" else element.top_level_parent()
        if control_type == "Button" and automation_id == "CloseButton":
            try:
                element.iface_invoke.Invoke()
            except AttributeError as exc:
                raise ActionFailed("Resolved close button does not support Invoke") from exc
            message = "Invoked the resolved document close button"
        elif control_type == "Window" and target.metadata.get("window_is_new"):
            try:
                element.iface_window.Close()
            except AttributeError as exc:
                raise ActionFailed("Resolved UIA window does not support Window.Close") from exc
            message = "Requested close for the run-owned UIA window"
        else:
            raise ActionFailed(
                "close_window requires a resolved document CloseButton or a new run-owned Window"
            )
        if step.parameters.get("discard_changes", False):
            if self._discard_save_prompt(root, context):
                message += " and discarded its save prompt"
        return ActionResult.executed_unverified(
            message, metadata=dict(target.metadata)
        )

    def _discard_save_prompt(
        self, root: Any, context: ExecutionContext
    ) -> bool:
        action_deadline = time.monotonic() + self._PROMPT_TIMEOUT_SECONDS
        if context.deadline is not None:
            action_deadline = min(action_deadline, context.deadline)
        while time.monotonic() < action_deadline:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled("Cancelled while waiting for the save prompt")
            try:
                candidates = [
                    element
                    for element in root.descendants()
                    if element.element_info.control_type == "Button"
                    and element.element_info.automation_id == "CommandButton_7"
                ]
            except (COMError, ElementNotFoundError):
                return False
            if len(candidates) > 1:
                raise ActionFailed("Save prompt has multiple discard buttons")
            if candidates:
                try:
                    candidates[0].iface_invoke.Invoke()
                except AttributeError as exc:
                    raise ActionFailed(
                        "Save prompt discard button does not support Invoke"
                    ) from exc
                return True
            context.cancellation.wait(
                min(
                    self._POLL_INTERVAL_SECONDS,
                    max(0.0, action_deadline - time.monotonic()),
                )
            )
        return False

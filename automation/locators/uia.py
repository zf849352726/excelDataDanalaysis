"""Semantic Windows UI Automation locator backed by pywinauto."""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping

from pywinauto import Desktop

from automation.engine.models import ExecutionContext
from automation.locators.models import LocatorResult


class UIALocator:
    _BASELINE_WINDOWS_KEY = "uia_baseline_top_level_windows"

    def begin(self, context: ExecutionContext) -> None:
        context.runtime_state[self._BASELINE_WINDOWS_KEY] = {
            window.handle: window.window_text()
            for window in Desktop(backend="uia").windows()
        }

    def locate(
        self, selector: Mapping[str, Any], context: ExecutionContext
    ) -> LocatorResult:
        process_alias = selector["process"]
        process = context.processes.get(process_alias)
        if process is None:
            return LocatorResult(
                found=False,
                strategy="uia",
                metadata={"process_alias": process_alias, "reason": "unknown_process_alias"},
            )

        roots = self._candidate_windows(selector, context, process.pid)
        matching_roots = [
            root for root in roots if self._matches(root, selector["window"], window=True)
        ]

        control_selector = selector.get("control")
        if control_selector is None:
            candidates = matching_roots
        else:
            candidates = [
                control
                for root in matching_roots
                for control in self._descendants(root)
                if self._matches(control, control_selector, window=False)
            ]

        metadata = {
            "process_alias": process_alias,
            "candidate_count": len(candidates),
            "window_candidate_count": len(matching_roots),
        }
        if not candidates:
            return LocatorResult(False, "uia", metadata=metadata)
        if len(candidates) > 1:
            metadata["candidate_handles"] = [
                getattr(candidate, "handle", None) for candidate in candidates
            ]
            return LocatorResult(
                False,
                "uia",
                ambiguous=True,
                metadata=metadata,
            )

        element = candidates[0]
        process.bound_pid = element.process_id()
        rectangle = element.rectangle()
        bounds = (
            rectangle.left,
            rectangle.top,
            rectangle.right,
            rectangle.bottom,
        )
        metadata.update(
            {
                "process_id": element.process_id(),
                "handle": getattr(element, "handle", None),
                "name": element.window_text(),
                "control_type": element.element_info.control_type,
                "automation_id": element.element_info.automation_id,
                "class_name": element.element_info.class_name,
            }
        )
        return LocatorResult(
            found=True,
            strategy="uia",
            x=(rectangle.left + rectangle.right) // 2,
            y=(rectangle.top + rectangle.bottom) // 2,
            bounds=bounds,
            element=element,
            metadata=metadata,
        )

    def _candidate_windows(
        self,
        selector: Mapping[str, Any],
        context: ExecutionContext,
        process_id: int,
    ) -> list[Any]:
        desktop = Desktop(backend="uia")
        direct = list(desktop.windows(process=process_id))
        if direct or not selector["allow_process_handoff"]:
            return direct

        baseline = context.runtime_state.get(self._BASELINE_WINDOWS_KEY, {})
        return [
            window
            for window in desktop.windows()
            if window.handle not in baseline
            or baseline[window.handle] != window.window_text()
        ]

    @staticmethod
    def _descendants(root: Any) -> Iterable[Any]:
        return root.descendants()

    @staticmethod
    def _matches(
        element: Any, selector: Mapping[str, str], *, window: bool
    ) -> bool:
        info = element.element_info
        name = element.window_text()
        if window:
            checks = {
                "title": name,
                "class_name": info.class_name,
            }
            if "title_contains" in selector and selector["title_contains"] not in name:
                return False
            if "title_regex" in selector and not re.search(selector["title_regex"], name):
                return False
        else:
            checks = {
                "control_type": info.control_type,
                "name": name,
                "automation_id": info.automation_id,
                "class_name": info.class_name,
            }
        return all(checks.get(key) == value for key, value in selector.items() if key in checks)

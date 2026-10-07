"""Strict YAML loader for the Milestone 1 workflow schema."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Mapping

import yaml

from automation.engine.errors import WorkflowValidationError
from automation.engine.models import Step, Workflow


_WORKFLOW_FIELDS = {"name", "version", "steps"}
_COMMON_STEP_FIELDS = {"id", "name", "action", "target", "expect"}
_ACTION_FIELDS = {
    "wait": {"seconds"},
    "launch": {"program", "args", "wait_for_exit", "process_alias"},
    "click": set(),
    "type_text": {"text"},
    "close_window": set(),
}
_TARGET_ACTIONS = {"click", "type_text", "close_window"}
_UIA_STRATEGY_FIELDS = {
    "type",
    "process",
    "allow_process_handoff",
    "window",
    "control",
}
_UIA_WINDOW_FIELDS = {"title", "title_contains", "title_regex", "class_name"}
_UIA_CONTROL_FIELDS = {"control_type", "name", "automation_id", "class_name"}


class WorkflowLoader:
    """Load only the schema implemented by the current milestone."""

    def load(self, path: str | Path) -> Workflow:
        source_path = Path(path).resolve()
        try:
            raw = yaml.safe_load(source_path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            raise WorkflowValidationError(
                f"Invalid YAML in '{source_path}': {exc}"
            ) from exc

        data = self._require_mapping(raw, "workflow")
        self._reject_unknown_fields(data, _WORKFLOW_FIELDS, "workflow")

        name = self._require_non_empty_string(data.get("name"), "workflow.name")
        version = data.get("version")
        if isinstance(version, bool) or not isinstance(version, int) or version != 1:
            raise WorkflowValidationError("workflow.version must be the integer 1")

        raw_steps = data.get("steps")
        if not isinstance(raw_steps, list) or not raw_steps:
            raise WorkflowValidationError("workflow.steps must be a non-empty list")

        steps: list[Step] = []
        step_ids: set[str] = set()
        for index, raw_step in enumerate(raw_steps):
            step = self._load_step(raw_step, index)
            if step.id in step_ids:
                raise WorkflowValidationError(f"Duplicate step id '{step.id}'")
            step_ids.add(step.id)
            steps.append(step)

        return Workflow(
            name=name,
            version=version,
            steps=tuple(steps),
            source_path=source_path,
        )

    def _load_step(self, raw: Any, index: int) -> Step:
        location = f"workflow.steps[{index}]"
        data = self._require_mapping(raw, location)

        action_name = self._require_non_empty_string(
            data.get("action"), f"{location}.action"
        )
        action_fields = _ACTION_FIELDS.get(action_name)
        if action_fields is None:
            supported = ", ".join(sorted(_ACTION_FIELDS))
            raise WorkflowValidationError(
                f"{location}.action '{action_name}' is unsupported; supported actions: {supported}"
            )

        self._reject_unknown_fields(
            data, _COMMON_STEP_FIELDS | action_fields, location
        )
        step_id = self._require_non_empty_string(data.get("id"), f"{location}.id")

        name = data.get("name")
        if name is not None:
            name = self._require_non_empty_string(name, f"{location}.name")

        parameters = self._load_action_parameters(action_name, data, location)
        target = self._load_optional_target(data.get("target"), f"{location}.target")
        if action_name in _TARGET_ACTIONS and target is None:
            raise WorkflowValidationError(
                f"{location}.target is required for action '{action_name}'"
            )
        if action_name not in _TARGET_ACTIONS and target is not None:
            raise WorkflowValidationError(
                f"{location}.target is not supported for action '{action_name}'"
            )

        expectation = self._load_optional_expectation(
            data.get("expect"), f"{location}.expect", target is not None
        )
        return Step(
            id=step_id,
            name=name,
            action=action_name,
            parameters=parameters,
            target=target,
            expectation=expectation,
        )

    def _load_action_parameters(
        self, action_name: str, data: Mapping[str, Any], location: str
    ) -> dict[str, Any]:
        if action_name == "wait":
            return self._load_wait_parameters(data, location)
        if action_name == "launch":
            return self._load_launch_parameters(data, location)
        if action_name == "type_text":
            return {
                "text": self._require_string(data.get("text"), f"{location}.text")
            }
        return {}

    def _load_wait_parameters(
        self, data: Mapping[str, Any], location: str
    ) -> dict[str, Any]:
        seconds = data.get("seconds")
        if (
            isinstance(seconds, bool)
            or not isinstance(seconds, (int, float))
            or not math.isfinite(seconds)
            or seconds < 0
        ):
            raise WorkflowValidationError(
                f"{location}.seconds must be a finite non-negative number"
            )
        return {"seconds": float(seconds)}

    def _load_launch_parameters(
        self, data: Mapping[str, Any], location: str
    ) -> dict[str, Any]:
        program = self._require_non_empty_string(
            data.get("program"), f"{location}.program"
        )
        args = data.get("args", [])
        if not isinstance(args, list) or any(not isinstance(arg, str) for arg in args):
            raise WorkflowValidationError(f"{location}.args must be a list of strings")

        wait_for_exit = data.get("wait_for_exit", False)
        if not isinstance(wait_for_exit, bool):
            raise WorkflowValidationError(
                f"{location}.wait_for_exit must be a boolean"
            )

        process_alias = data.get("process_alias")
        if process_alias is not None:
            process_alias = self._require_non_empty_string(
                process_alias, f"{location}.process_alias"
            )

        return {
            "program": program,
            "args": tuple(args),
            "wait_for_exit": wait_for_exit,
            "process_alias": process_alias,
        }

    def _load_optional_target(
        self, value: Any, location: str
    ) -> Mapping[str, Any] | None:
        if value is None:
            return None
        data = self._require_mapping(value, location)
        self._reject_unknown_fields(data, {"strategies"}, location)
        strategies = data.get("strategies")
        if not isinstance(strategies, list) or not strategies:
            raise WorkflowValidationError(f"{location}.strategies must be a non-empty list")
        return {
            "strategies": tuple(
                self._load_uia_strategy(strategy, f"{location}.strategies[{index}]")
                for index, strategy in enumerate(strategies)
            )
        }

    def _load_uia_strategy(self, value: Any, location: str) -> Mapping[str, Any]:
        data = self._require_mapping(value, location)
        self._reject_unknown_fields(data, _UIA_STRATEGY_FIELDS, location)
        strategy_type = self._require_non_empty_string(
            data.get("type"), f"{location}.type"
        )
        if strategy_type != "uia":
            raise WorkflowValidationError(
                f"{location}.type '{strategy_type}' is unsupported in Milestone 2"
            )
        process = self._require_non_empty_string(
            data.get("process"), f"{location}.process"
        )
        allow_handoff = data.get("allow_process_handoff", False)
        if not isinstance(allow_handoff, bool):
            raise WorkflowValidationError(
                f"{location}.allow_process_handoff must be a boolean"
            )

        window = self._load_selector_part(
            data.get("window"), _UIA_WINDOW_FIELDS, f"{location}.window"
        )
        if window is None:
            raise WorkflowValidationError(f"{location}.window is required")
        if "title_regex" in window:
            try:
                re.compile(window["title_regex"])
            except re.error as exc:
                raise WorkflowValidationError(
                    f"{location}.window.title_regex is invalid: {exc}"
                ) from exc

        control = self._load_selector_part(
            data.get("control"), _UIA_CONTROL_FIELDS, f"{location}.control"
        )
        if allow_handoff and not any(
            key in window for key in ("title", "title_contains", "title_regex")
        ):
            raise WorkflowValidationError(
                f"{location}.window requires a title constraint when process handoff is allowed"
            )

        return {
            "type": "uia",
            "process": process,
            "allow_process_handoff": allow_handoff,
            "window": window,
            "control": control,
        }

    def _load_selector_part(
        self, value: Any, allowed: set[str], location: str
    ) -> Mapping[str, str] | None:
        if value is None:
            return None
        data = self._require_mapping(value, location)
        self._reject_unknown_fields(data, allowed, location)
        if not data:
            raise WorkflowValidationError(f"{location} must not be empty")
        return {
            key: self._require_non_empty_string(item, f"{location}.{key}")
            for key, item in data.items()
        }

    def _load_optional_expectation(
        self, value: Any, location: str, has_action_target: bool
    ) -> Mapping[str, Any] | None:
        if value is None:
            return None
        data = self._require_mapping(value, location)
        expectation_type = self._require_non_empty_string(
            data.get("type"), f"{location}.type"
        )
        allowed_by_type = {
            "uia_exists": {"type", "target"},
            "uia_text_equals": {"type", "target", "value"},
            "uia_disappeared": {"type", "target"},
        }
        allowed = allowed_by_type.get(expectation_type)
        if allowed is None:
            supported = ", ".join(sorted(allowed_by_type))
            raise WorkflowValidationError(
                f"{location}.type '{expectation_type}' is unsupported; "
                f"supported expectations: {supported}"
            )
        self._reject_unknown_fields(data, allowed, location)

        target = self._load_optional_target(data.get("target"), f"{location}.target")
        if expectation_type in {"uia_exists", "uia_disappeared"} and target is None:
            raise WorkflowValidationError(
                f"{location}.target is required for '{expectation_type}'"
            )
        if expectation_type == "uia_text_equals" and target is None and not has_action_target:
            raise WorkflowValidationError(
                f"{location} requires a target because the action has no target"
            )

        expectation: dict[str, Any] = {
            "type": expectation_type,
            "target": target,
        }
        if expectation_type == "uia_text_equals":
            expectation["value"] = self._require_string(
                data.get("value"), f"{location}.value"
            )
        return expectation

    @staticmethod
    def _require_mapping(value: Any, location: str) -> Mapping[str, Any]:
        if not isinstance(value, dict):
            raise WorkflowValidationError(f"{location} must be a mapping")
        if any(not isinstance(key, str) for key in value):
            raise WorkflowValidationError(f"{location} field names must be strings")
        return value

    @staticmethod
    def _require_non_empty_string(value: Any, location: str) -> str:
        if not isinstance(value, str) or not value.strip():
            raise WorkflowValidationError(f"{location} must be a non-empty string")
        return value

    @staticmethod
    def _require_string(value: Any, location: str) -> str:
        if not isinstance(value, str):
            raise WorkflowValidationError(f"{location} must be a string")
        return value

    @staticmethod
    def _reject_unknown_fields(
        data: Mapping[str, Any], allowed: set[str], location: str
    ) -> None:
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise WorkflowValidationError(
                f"{location} contains unsupported fields: {', '.join(unknown)}"
            )

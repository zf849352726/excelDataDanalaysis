"""Strict YAML loader for the Milestone 1 workflow schema."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

import yaml

from automation.engine.errors import WorkflowValidationError
from automation.engine.models import Step, Workflow


_WORKFLOW_FIELDS = {"name", "version", "steps"}
_COMMON_STEP_FIELDS = {"id", "name", "action"}
_ACTION_FIELDS = {
    "wait": {"seconds"},
    "launch": {"program", "args", "wait_for_exit"},
}


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

        if action_name == "wait":
            parameters = self._load_wait_parameters(data, location)
        else:
            parameters = self._load_launch_parameters(data, location)

        return Step(id=step_id, name=name, action=action_name, parameters=parameters)

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

        return {
            "program": program,
            "args": tuple(args),
            "wait_for_exit": wait_for_exit,
        }

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
    def _reject_unknown_fields(
        data: Mapping[str, Any], allowed: set[str], location: str
    ) -> None:
        unknown = sorted(set(data) - allowed)
        if unknown:
            raise WorkflowValidationError(
                f"{location} contains unsupported fields: {', '.join(unknown)}"
            )

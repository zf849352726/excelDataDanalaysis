from pathlib import Path

import pytest

from automation.engine import WorkflowLoader, WorkflowValidationError


def write_workflow(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "workflow.yaml"
    path.write_text(content, encoding="utf-8")
    return path


def test_loads_notepad_uia_workflow() -> None:
    project_root = Path(__file__).resolve().parents[2]
    workflow = WorkflowLoader().load(
        project_root / "workflows" / "notepad_uia" / "workflow.yaml"
    )

    assert [step.action for step in workflow.steps] == ["launch", "type_text", "click"]
    assert workflow.steps[0].parameters["process_alias"] == "notepad_m2"
    assert workflow.steps[1].target is not None
    assert workflow.steps[1].expectation["type"] == "uia_text_equals"


def test_target_bound_action_requires_target(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: missing_target
version: 1
steps:
  - id: type
    action: type_text
    text: hello
""",
    )

    with pytest.raises(WorkflowValidationError, match="target is required"):
        WorkflowLoader().load(path)


def test_process_handoff_requires_window_title_constraint(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: unsafe_handoff
version: 1
steps:
  - id: click
    action: click
    target:
      strategies:
        - type: uia
          process: app
          allow_process_handoff: true
          window:
            class_name: Notepad
          control:
            control_type: Button
            automation_id: CloseButton
""",
    )

    with pytest.raises(WorkflowValidationError, match="title constraint"):
        WorkflowLoader().load(path)


def test_rejects_unknown_uia_selector_field(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: guessed_coordinate
version: 1
steps:
  - id: click
    action: click
    target:
      strategies:
        - type: uia
          process: app
          window:
            title: Safe window
          control:
            control_type: Button
            x: 100
""",
    )

    with pytest.raises(WorkflowValidationError, match="x"):
        WorkflowLoader().load(path)

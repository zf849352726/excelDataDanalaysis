from pathlib import Path

import pytest

from automation.engine import WorkflowLoader, WorkflowValidationError


def write_workflow(tmp_path: Path, content: str) -> Path:
    path = tmp_path / "workflow.yaml"
    path.write_text(content, encoding="utf-8")
    return path


def test_loads_strict_m1_workflow(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: loader_test
version: 1
steps:
  - id: wait_once
    name: Short wait
    action: wait
    seconds: 0.25
  - id: launch_once
    action: launch
    program: cmd.exe
    args: ["/d", "/c", "exit", "0"]
    wait_for_exit: true
""",
    )

    workflow = WorkflowLoader().load(path)

    assert workflow.name == "loader_test"
    assert [step.id for step in workflow.steps] == ["wait_once", "launch_once"]
    assert workflow.steps[0].parameters == {"seconds": 0.25}
    assert workflow.steps[1].parameters["args"] == ("/d", "/c", "exit", "0")


@pytest.mark.parametrize("field", ["coordinates", "screen_changed"])
def test_rejects_unknown_step_fields(
    tmp_path: Path, field: str
) -> None:
    path = write_workflow(
        tmp_path,
        f"""
name: unsupported_field
version: 1
steps:
  - id: wait_once
    action: wait
    seconds: 0
    {field}: invalid
""",
    )

    with pytest.raises(WorkflowValidationError, match=field):
        WorkflowLoader().load(path)


def test_rejects_unknown_action(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: unknown_action
version: 1
steps:
  - id: unsafe_click
    action: click_xy
""",
    )

    with pytest.raises(WorkflowValidationError, match="unsupported"):
        WorkflowLoader().load(path)


def test_rejects_duplicate_step_ids(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """
name: duplicate_steps
version: 1
steps:
  - id: duplicate
    action: wait
    seconds: 0
  - id: duplicate
    action: wait
    seconds: 0
""",
    )

    with pytest.raises(WorkflowValidationError, match="Duplicate step id"):
        WorkflowLoader().load(path)


@pytest.mark.parametrize("seconds", ["-1", ".nan", "true"])
def test_rejects_invalid_wait_duration(tmp_path: Path, seconds: str) -> None:
    path = write_workflow(
        tmp_path,
        f"""
name: invalid_wait
version: 1
steps:
  - id: wait_once
    action: wait
    seconds: {seconds}
""",
    )

    with pytest.raises(WorkflowValidationError, match="finite non-negative"):
        WorkflowLoader().load(path)

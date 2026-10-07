from pathlib import Path

import pytest

from automation.engine import WorkflowLoader, WorkflowValidationError


def write_workflow(tmp_path: Path, step_body: str) -> Path:
    path = tmp_path / "workflow.yaml"
    path.write_text(
        f"""
name: m4_test
version: 1
steps:
  - id: policy_step
    action: wait
    seconds: 0
{step_body}
""",
        encoding="utf-8",
    )
    return path


def test_loads_retry_timeout_and_failure_policy(tmp_path: Path) -> None:
    workflow = WorkflowLoader().load(
        write_workflow(
            tmp_path,
            """    timeout: 2.5
    retry: 3
    retry_interval: 0.25
    on_fail: continue""",
        )
    )
    step = workflow.steps[0]

    assert step.timeout == 2.5
    assert step.retry == 3
    assert step.retry_interval == 0.25
    assert step.on_fail == "continue"


@pytest.mark.parametrize(
    "body,match",
    [
        ("    timeout: 0", "timeout"),
        ("    retry: -1", "retry"),
        ("    retry: true", "retry"),
        ("    retry_interval: -1", "retry_interval"),
        ("    on_fail: ignore", "on_fail"),
    ],
)
def test_rejects_invalid_execution_policy(
    tmp_path: Path, body: str, match: str
) -> None:
    with pytest.raises(WorkflowValidationError, match=match):
        WorkflowLoader().load(write_workflow(tmp_path, body))


def test_loads_workflow_relative_file_expectation(tmp_path: Path) -> None:
    workflow = WorkflowLoader().load(
        write_workflow(
            tmp_path,
            """    expect:
      type: file_exists
      path: output/report.xlsx""",
        )
    )

    assert workflow.steps[0].expectation == {
        "type": "file_exists",
        "target": None,
        "path": "output/report.xlsx",
    }


def test_rejects_parent_relative_file_expectation(tmp_path: Path) -> None:
    with pytest.raises(WorkflowValidationError, match="workflow-relative"):
        WorkflowLoader().load(
            write_workflow(
                tmp_path,
                """    expect:
      type: file_exists
      path: ../report.xlsx""",
            )
        )


def test_window_expectation_rejects_control_selector(tmp_path: Path) -> None:
    path = tmp_path / "workflow.yaml"
    path.write_text(
        """
name: invalid_window_expectation
version: 1
steps:
  - id: launch
    action: launch
    program: app.exe
    expect:
      type: window_exists
      target:
        strategies:
          - type: uia
            process: app
            window:
              title: App
            control:
              control_type: Button
""",
        encoding="utf-8",
    )

    with pytest.raises(WorkflowValidationError, match="UIA window"):
        WorkflowLoader().load(path)

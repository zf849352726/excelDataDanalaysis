import os
from pathlib import Path

import pytest

from automation import (
    ExecutionStatus,
    WorkflowExecutor,
    WorkflowLoader,
    create_default_registry,
)


@pytest.mark.skipif(os.name != "nt", reason="The project and sample workflow target Windows")
def test_basic_workflow_runs_end_to_end() -> None:
    project_root = Path(__file__).resolve().parents[2]
    workflow_path = project_root / "workflows" / "basic_test" / "workflow.yaml"
    workflow = WorkflowLoader().load(workflow_path)

    result = WorkflowExecutor(create_default_registry()).execute(workflow)

    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
    assert [step.step_id for step in result.steps] == [
        "wait_briefly",
        "launch_disposable_process",
    ]
    assert all(step.status is ExecutionStatus.EXECUTED_UNVERIFIED for step in result.steps)

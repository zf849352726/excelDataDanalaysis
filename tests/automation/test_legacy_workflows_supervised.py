import os
from pathlib import Path

import pytest

from automation import ExecutionStatus, WorkflowLoader, create_default_executor


pytestmark = [
    pytest.mark.ui_integration,
    pytest.mark.skipif(os.name != "nt", reason="Legacy desktop workflows require Windows"),
    pytest.mark.skipif(
        os.environ.get("AUTOMATION_LEGACY_UI_TESTS") != "1",
        reason="Set AUTOMATION_LEGACY_UI_TESTS=1 while supervising the desktop",
    ),
]


def test_migrated_workflows_run_as_unverified_under_supervision() -> None:
    project_root = Path(__file__).resolve().parents[2]
    for workflow_path in sorted(
        (project_root / "workflows" / "legacy").glob("*/workflow.yaml")
    ):
        workflow = WorkflowLoader().load(workflow_path)
        result = create_default_executor().execute(workflow)

        assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
        assert all(
            step.status is ExecutionStatus.EXECUTED_UNVERIFIED
            for step in result.steps
        )

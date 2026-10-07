import os
import time
from pathlib import Path

import pytest

from automation import ExecutionStatus, WorkflowLoader, create_default_executor


pytestmark = [
    pytest.mark.ui_integration,
    pytest.mark.skipif(os.name != "nt", reason="Notepad UIA test requires Windows"),
    pytest.mark.skipif(
        os.environ.get("AUTOMATION_UI_TESTS") != "1",
        reason="Set AUTOMATION_UI_TESTS=1 to run desktop integration tests",
    ),
]


def test_notepad_uia_succeeds_five_times() -> None:
    project_root = Path(__file__).resolve().parents[2]
    workflow = WorkflowLoader().load(
        project_root / "workflows" / "notepad_uia" / "workflow.yaml"
    )

    results = []
    for _ in range(5):
        result = create_default_executor().execute(workflow)
        results.append(result)
        if result.status is not ExecutionStatus.VERIFIED:
            pytest.fail(
                repr(
                    [
                        (step.step_id, step.status.value, step.result.message)
                        for step in result.steps
                    ]
                )
            )
        time.sleep(0.2)

    assert all(result.status is ExecutionStatus.VERIFIED for result in results)

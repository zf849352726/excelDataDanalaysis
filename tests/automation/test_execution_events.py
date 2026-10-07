from automation import (
    ExecutionEventType,
    ExecutionStatus,
    WorkflowExecutor,
    WorkflowLoader,
    create_default_registry,
)


def test_executor_emits_ordered_lifecycle_events(tmp_path) -> None:
    workflow_path = tmp_path / "workflow.yaml"
    workflow_path.write_text(
        """
name: events
version: 1
steps:
  - id: first
    action: wait
    seconds: 0
  - id: second
    action: wait
    seconds: 0
""".strip(),
        encoding="utf-8",
    )
    workflow = WorkflowLoader().load(workflow_path)
    events = []

    result = WorkflowExecutor(create_default_registry()).execute(
        workflow, event_handler=events.append
    )

    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
    assert [event.type for event in events] == [
        ExecutionEventType.WORKFLOW_STARTED,
        ExecutionEventType.STEP_STARTED,
        ExecutionEventType.STEP_COMPLETED,
        ExecutionEventType.STEP_STARTED,
        ExecutionEventType.STEP_COMPLETED,
        ExecutionEventType.WORKFLOW_COMPLETED,
    ]
    assert events[1].step_index == 1
    assert events[3].step_index == 2
    assert events[-1].result is result


def test_event_handler_failure_does_not_fail_workflow(tmp_path) -> None:
    workflow_path = tmp_path / "workflow.yaml"
    workflow_path.write_text(
        "name: events\nversion: 1\nsteps:\n  - id: wait\n"
        "    action: wait\n    seconds: 0\n",
        encoding="utf-8",
    )

    def broken_handler(_event) -> None:
        raise RuntimeError("display disconnected")

    result = WorkflowExecutor(create_default_registry()).execute(
        WorkflowLoader().load(workflow_path), event_handler=broken_handler
    )

    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED

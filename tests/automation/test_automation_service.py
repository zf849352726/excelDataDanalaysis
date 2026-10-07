from __future__ import annotations

from pathlib import Path
from threading import Thread
import time

import pytest

from automation import ExecutionEventType, ExecutionStatus
from automation.services import AutomationService, AutomationServiceBusy


def write_wait_workflow(directory: Path, name: str, seconds: float) -> Path:
    directory.mkdir(parents=True)
    path = directory / "workflow.yaml"
    path.write_text(
        f"name: {name}\nversion: 1\nsteps:\n  - id: wait\n"
        f"    action: wait\n    seconds: {seconds}\n",
        encoding="utf-8",
    )
    return path


def test_service_lists_workflows_and_steps(tmp_path) -> None:
    first = write_wait_workflow(tmp_path / "zeta", "Zeta", 0)
    write_wait_workflow(tmp_path / "nested" / "alpha", "Alpha", 0)

    summaries = AutomationService(tmp_path).list_workflows()

    assert [summary.workflow_id for summary in summaries] == [
        "nested/alpha",
        "zeta",
    ]
    assert summaries[1].path == first.resolve()
    assert summaries[1].steps == (("wait", "wait", None),)


def test_service_runs_one_workflow_and_forwards_events(tmp_path) -> None:
    path = write_wait_workflow(tmp_path / "sample", "Sample", 0)
    events = []

    result = AutomationService(tmp_path).run_workflow(path, events.append)

    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
    assert events[0].type is ExecutionEventType.WORKFLOW_STARTED
    assert events[-1].type is ExecutionEventType.WORKFLOW_COMPLETED


def test_service_stops_active_workflow_and_rejects_parallel_run(tmp_path) -> None:
    path = write_wait_workflow(tmp_path / "slow", "Slow", 5)
    service = AutomationService(tmp_path)
    results = []
    thread = Thread(target=lambda: results.append(service.run_workflow(path)))
    thread.start()
    deadline = time.monotonic() + 1
    while not service.is_running and time.monotonic() < deadline:
        time.sleep(0.005)

    with pytest.raises(AutomationServiceBusy):
        service.run_workflow(path)
    assert service.stop_active()
    thread.join(timeout=1)

    assert not thread.is_alive()
    assert results[0].status is ExecutionStatus.CANCELLED
    assert not service.is_running
    assert not service.stop_active()


def test_service_rejects_workflow_outside_managed_root(tmp_path) -> None:
    managed = tmp_path / "managed"
    managed.mkdir()
    outside = write_wait_workflow(tmp_path / "outside", "Outside", 0)

    with pytest.raises(ValueError, match="configured root"):
        AutomationService(managed).run_workflow(outside)

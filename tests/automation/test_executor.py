from __future__ import annotations

import sys
import threading
import time

from automation.actions import create_default_registry
from automation.engine import (
    ActionRegistry,
    ActionResult,
    CancellationToken,
    ExecutionContext,
    ExecutionStatus,
    Step,
    Workflow,
    WorkflowExecutor,
    VerificationResult,
)


class RecordingAction:
    def __init__(self, calls: list[str], result: ActionResult | None = None) -> None:
        self.calls = calls
        self.result = result or ActionResult.executed_unverified()

    def execute(
        self, step: Step, context: ExecutionContext, target=None
    ) -> ActionResult:
        self.calls.append(step.id)
        return self.result


class RaisingAction:
    def execute(
        self, step: Step, context: ExecutionContext, target=None
    ) -> ActionResult:
        raise RuntimeError("expected failure")


def workflow_with(*steps: Step) -> Workflow:
    return Workflow(name="test", version=1, steps=steps)


def test_executor_runs_steps_in_declared_order() -> None:
    calls: list[str] = []
    registry = ActionRegistry()
    registry.register("record", RecordingAction(calls))
    workflow = workflow_with(
        Step("first", "record"),
        Step("second", "record"),
        Step("third", "record"),
    )

    result = WorkflowExecutor(registry).execute(workflow)

    assert calls == ["first", "second", "third"]
    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
    assert all(step.status is ExecutionStatus.EXECUTED_UNVERIFIED for step in result.steps)


def test_executor_stops_after_explicit_failure() -> None:
    calls: list[str] = []
    registry = ActionRegistry()
    registry.register(
        "fail", RecordingAction(calls, ActionResult.failed("expected failure"))
    )
    registry.register("record", RecordingAction(calls))
    workflow = workflow_with(
        Step("failing", "fail"),
        Step("must_not_run", "record"),
    )

    result = WorkflowExecutor(registry).execute(workflow)

    assert calls == ["failing"]
    assert result.status is ExecutionStatus.FAILED
    assert len(result.steps) == 1


def test_executor_converts_action_exception_to_explicit_failure() -> None:
    registry = ActionRegistry()
    registry.register("raise", RaisingAction())

    result = WorkflowExecutor(registry).execute(
        workflow_with(Step("failing", "raise"))
    )

    assert result.status is ExecutionStatus.FAILED
    assert result.steps[0].result.error_type == "RuntimeError"
    assert result.steps[0].result.message == "expected failure"


def test_interruptible_wait_returns_cancelled_promptly() -> None:
    token = CancellationToken()
    context = ExecutionContext(cancellation=token)
    workflow = workflow_with(Step("long_wait", "wait", {"seconds": 10.0}))
    executor = WorkflowExecutor(create_default_registry())
    results = []

    thread = threading.Thread(
        target=lambda: results.append(executor.execute(workflow, context))
    )
    started_at = time.monotonic()
    thread.start()
    time.sleep(0.05)
    token.cancel()
    thread.join(timeout=1.0)

    assert not thread.is_alive()
    assert time.monotonic() - started_at < 1.0
    assert results[0].status is ExecutionStatus.CANCELLED
    assert results[0].steps[0].status is ExecutionStatus.CANCELLED


def test_launch_reports_nonzero_exit_as_failure() -> None:
    workflow = workflow_with(
        Step(
            "exit_three",
            "launch",
            {
                "program": sys.executable,
                "args": ("-c", "raise SystemExit(3)"),
                "wait_for_exit": True,
            },
        )
    )

    result = WorkflowExecutor(create_default_registry()).execute(workflow)

    assert result.status is ExecutionStatus.FAILED
    assert result.steps[0].result.metadata["exit_code"] == 3


def test_waiting_launch_cancels_and_stops_its_owned_process() -> None:
    token = CancellationToken()
    context = ExecutionContext(cancellation=token)
    workflow = workflow_with(
        Step(
            "long_process",
            "launch",
            {
                "program": sys.executable,
                "args": ("-c", "import time; time.sleep(10)"),
                "wait_for_exit": True,
            },
        )
    )
    executor = WorkflowExecutor(create_default_registry())
    results = []

    thread = threading.Thread(
        target=lambda: results.append(executor.execute(workflow, context))
    )
    thread.start()
    time.sleep(0.1)
    token.cancel()
    thread.join(timeout=3.0)

    assert not thread.is_alive()
    assert results[0].status is ExecutionStatus.CANCELLED
    assert results[0].steps[0].result.metadata["pid"] > 0


class StaticResolver:
    def __init__(self, target) -> None:
        self.target = target
        self.began = False

    def begin(self, context: ExecutionContext) -> None:
        self.began = True

    def resolve(self, target, context: ExecutionContext):
        return self.target


class StaticVerificationService:
    def __init__(self, passed: bool) -> None:
        self.passed = passed

    def verify(self, expectation, context, action_target) -> VerificationResult:
        return VerificationResult(self.passed, "checked")


def test_executor_reports_verified_only_after_expectation_passes() -> None:
    calls: list[str] = []
    registry = ActionRegistry()
    registry.register("record", RecordingAction(calls))
    resolver = StaticResolver(object())
    executor = WorkflowExecutor(
        registry,
        target_resolver=resolver,
        verification_service=StaticVerificationService(True),
    )
    workflow = workflow_with(
        Step(
            "verified",
            "record",
            target={"strategies": ()},
            expectation={"type": "check"},
        )
    )

    result = executor.execute(workflow)

    assert resolver.began
    assert result.status is ExecutionStatus.VERIFIED
    assert result.steps[0].status is ExecutionStatus.VERIFIED


def test_executor_exposes_verification_failure_and_stops() -> None:
    calls: list[str] = []
    registry = ActionRegistry()
    registry.register("record", RecordingAction(calls))
    executor = WorkflowExecutor(
        registry,
        target_resolver=StaticResolver(object()),
        verification_service=StaticVerificationService(False),
    )
    workflow = workflow_with(
        Step("unmet", "record", expectation={"type": "check"}),
        Step("must_not_run", "record"),
    )

    result = executor.execute(workflow)

    assert calls == ["unmet"]
    assert result.status is ExecutionStatus.FAILED
    assert result.steps[0].result.error_type == "VerificationFailed"

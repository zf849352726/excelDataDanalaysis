"""Interruptible wait action."""

from typing import Any

from automation.engine.models import ActionResult, ExecutionContext, Step


class WaitAction:
    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        seconds = step.parameters["seconds"]
        remaining = context.remaining_seconds()
        wait_seconds = seconds if remaining is None else min(seconds, remaining)
        if context.cancellation.wait(wait_seconds):
            return ActionResult.cancelled("Wait cancelled")
        if remaining is not None and wait_seconds < seconds:
            return ActionResult.failed(
                "Wait exceeded the step timeout", error_type="StepTimeout"
            )
        return ActionResult.executed_unverified(
            f"Waited {seconds:g} seconds", metadata={"seconds": seconds}
        )

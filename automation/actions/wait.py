"""Interruptible wait action."""

from typing import Any

from automation.engine.models import ActionResult, ExecutionContext, Step


class WaitAction:
    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        seconds = step.parameters["seconds"]
        if context.cancellation.wait(seconds):
            return ActionResult.cancelled("Wait cancelled")
        return ActionResult.executed_unverified(
            f"Waited {seconds:g} seconds", metadata={"seconds": seconds}
        )

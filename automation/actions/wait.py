"""Interruptible wait action."""

from automation.engine.models import ActionResult, ExecutionContext, Step


class WaitAction:
    def execute(self, step: Step, context: ExecutionContext) -> ActionResult:
        seconds = step.parameters["seconds"]
        if context.cancellation.wait(seconds):
            return ActionResult.cancelled("Wait cancelled")
        return ActionResult.executed_unverified(
            f"Waited {seconds:g} seconds", metadata={"seconds": seconds}
        )

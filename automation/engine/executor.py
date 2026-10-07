"""Sequential workflow execution with explicit terminal results."""

from __future__ import annotations

import logging

from automation.engine.errors import AutomationError
from automation.engine.models import (
    ActionResult,
    ExecutionContext,
    ExecutionStatus,
    Step,
    StepResult,
    Workflow,
    WorkflowResult,
)
from automation.engine.registry import ActionRegistry


logger = logging.getLogger(__name__)


class WorkflowExecutor:
    def __init__(self, registry: ActionRegistry) -> None:
        self._registry = registry

    def execute(
        self, workflow: Workflow, context: ExecutionContext | None = None
    ) -> WorkflowResult:
        execution_context = context or ExecutionContext()
        step_results: list[StepResult] = []

        logger.info("workflow_started", extra={"workflow": workflow.name})
        for step in workflow.steps:
            if execution_context.cancellation.is_cancelled:
                result = ActionResult.cancelled()
            else:
                result = self._execute_step(workflow, step, execution_context)

            step_result = StepResult(step.id, step.action, result)
            step_results.append(step_result)
            logger.info(
                "step_completed",
                extra={
                    "workflow": workflow.name,
                    "step_id": step.id,
                    "action": step.action,
                    "status": result.status.value,
                    "error": result.message if result.status is ExecutionStatus.FAILED else None,
                },
            )

            if result.status in {ExecutionStatus.FAILED, ExecutionStatus.CANCELLED}:
                break

        final_status = (
            step_results[-1].status
            if step_results
            and step_results[-1].status
            in {ExecutionStatus.FAILED, ExecutionStatus.CANCELLED}
            else ExecutionStatus.EXECUTED_UNVERIFIED
        )
        logger.info(
            "workflow_completed",
            extra={"workflow": workflow.name, "status": final_status.value},
        )
        return WorkflowResult(workflow.name, final_status, tuple(step_results))

    def _execute_step(
        self, workflow: Workflow, step: Step, context: ExecutionContext
    ) -> ActionResult:
        logger.info(
            "step_started",
            extra={
                "workflow": workflow.name,
                "step_id": step.id,
                "action": step.action,
            },
        )
        try:
            action = self._registry.get(step.action)
            result = action.execute(step, context)
            if not isinstance(result, ActionResult):
                raise TypeError(
                    f"Action '{step.action}' returned {type(result).__name__}, "
                    "expected ActionResult"
                )
            return result
        except AutomationError as exc:
            return ActionResult.failed(str(exc), error_type=type(exc).__name__)
        except Exception as exc:
            logger.exception(
                "step_failed_unexpectedly",
                extra={
                    "workflow": workflow.name,
                    "step_id": step.id,
                    "action": step.action,
                },
            )
            return ActionResult.failed(str(exc), error_type=type(exc).__name__)

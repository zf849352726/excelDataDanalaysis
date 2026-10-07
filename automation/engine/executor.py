"""Sequential workflow execution with explicit terminal results."""

from __future__ import annotations

import logging

from automation.engine.errors import AutomationError
from automation.engine.interfaces import TargetResolver, VerificationService
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
    def __init__(
        self,
        registry: ActionRegistry,
        target_resolver: TargetResolver | None = None,
        verification_service: VerificationService | None = None,
    ) -> None:
        self._registry = registry
        self._target_resolver = target_resolver
        self._verification_service = verification_service

    def execute(
        self, workflow: Workflow, context: ExecutionContext | None = None
    ) -> WorkflowResult:
        execution_context = context or ExecutionContext()
        if execution_context.working_directory is None and workflow.source_path:
            execution_context.working_directory = workflow.source_path.parent
        if self._target_resolver is not None:
            self._target_resolver.begin(execution_context)
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

        if step_results and step_results[-1].status in {
            ExecutionStatus.FAILED,
            ExecutionStatus.CANCELLED,
        }:
            final_status = step_results[-1].status
        elif step_results and all(
            result.status is ExecutionStatus.VERIFIED for result in step_results
        ):
            final_status = ExecutionStatus.VERIFIED
        else:
            final_status = ExecutionStatus.EXECUTED_UNVERIFIED
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
            target = self._resolve_target(step, context)
            result = action.execute(step, context, target)
            if not isinstance(result, ActionResult):
                raise TypeError(
                    f"Action '{step.action}' returned {type(result).__name__}, "
                    "expected ActionResult"
                )
            if result.status in {
                ExecutionStatus.FAILED,
                ExecutionStatus.CANCELLED,
            }:
                return result
            return self._verify_expectation(step, context, target, result)
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

    def _resolve_target(self, step: Step, context: ExecutionContext):
        if step.target is None:
            return None
        if self._target_resolver is None:
            raise RuntimeError(
                f"Step '{step.id}' declares a target but no target resolver is configured"
            )
        return self._target_resolver.resolve(step.target, context)

    def _verify_expectation(
        self,
        step: Step,
        context: ExecutionContext,
        target,
        action_result: ActionResult,
    ) -> ActionResult:
        if step.expectation is None:
            return action_result
        if self._verification_service is None:
            raise RuntimeError(
                f"Step '{step.id}' declares an expectation but no verifier is configured"
            )

        verification = self._verification_service.verify(
            step.expectation, context, target
        )
        metadata = dict(action_result.metadata)
        metadata["verification"] = dict(verification.metadata)
        if not verification.passed:
            return ActionResult.failed(
                verification.message,
                error_type="VerificationFailed",
                metadata=metadata,
            )
        return ActionResult.verified(verification.message, metadata=metadata)

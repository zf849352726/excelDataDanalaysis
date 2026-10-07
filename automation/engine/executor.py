"""Sequential workflow execution with explicit terminal results."""

from __future__ import annotations

import logging
import time
from dataclasses import replace
from typing import Any

from automation.engine.errors import AutomationError, StepTimeout, WorkflowCancelled
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

            if result.status is ExecutionStatus.CANCELLED:
                break
            if result.status is ExecutionStatus.FAILED and step.on_fail == "stop":
                break

        if any(result.status is ExecutionStatus.CANCELLED for result in step_results):
            final_status = ExecutionStatus.CANCELLED
        elif any(result.status is ExecutionStatus.FAILED for result in step_results):
            final_status = ExecutionStatus.FAILED
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
        max_attempts = step.retry + 1
        history: list[dict[str, Any]] = []
        for attempt in range(1, max_attempts + 1):
            result = self._execute_attempt(workflow, step, context, attempt)
            history.append(
                {
                    "attempt": attempt,
                    "status": result.status.value,
                    "error_type": result.error_type,
                    "message": result.message,
                    "metadata": dict(result.metadata),
                }
            )
            if result.status is not ExecutionStatus.FAILED or attempt == max_attempts:
                return self._with_attempt_metadata(result, attempt, max_attempts, history)

            logger.warning(
                "step_attempt_failed",
                extra={
                    "workflow": workflow.name,
                    "step_id": step.id,
                    "action": step.action,
                    "attempt": attempt,
                    "max_attempts": max_attempts,
                    "error": result.message,
                },
            )
            if context.cancellation.wait(step.retry_interval):
                cancelled = ActionResult.cancelled("Cancelled before the next retry")
                return self._with_attempt_metadata(
                    cancelled, attempt, max_attempts, history
                )

        raise AssertionError("Step retry loop completed without a result")

    def _execute_attempt(
        self,
        workflow: Workflow,
        step: Step,
        context: ExecutionContext,
        attempt: int,
    ) -> ActionResult:
        previous_deadline = context.deadline
        if step.timeout is not None:
            attempt_deadline = time.monotonic() + step.timeout
            context.deadline = (
                min(previous_deadline, attempt_deadline)
                if previous_deadline is not None
                else attempt_deadline
            )
        try:
            self._raise_if_timed_out(step, context)
            action = self._registry.get(step.action)
            target = self._resolve_target(step, context)
            self._raise_if_timed_out(step, context)
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
            self._raise_if_timed_out(step, context)
            return self._verify_expectation(step, context, target, result)
        except WorkflowCancelled as exc:
            return ActionResult.cancelled(str(exc))
        except AutomationError as exc:
            return ActionResult.failed(str(exc), error_type=type(exc).__name__)
        except Exception as exc:
            logger.exception(
                "step_failed_unexpectedly",
                extra={
                    "workflow": workflow.name,
                    "step_id": step.id,
                    "action": step.action,
                    "attempt": attempt,
                },
            )
            return ActionResult.failed(str(exc), error_type=type(exc).__name__)
        finally:
            context.deadline = previous_deadline

    @staticmethod
    def _raise_if_timed_out(step: Step, context: ExecutionContext) -> None:
        if context.is_timed_out:
            raise StepTimeout(f"Step '{step.id}' exceeded its timeout")

    @staticmethod
    def _with_attempt_metadata(
        result: ActionResult,
        attempts: int,
        max_attempts: int,
        history: list[dict[str, Any]],
    ) -> ActionResult:
        metadata = dict(result.metadata)
        metadata.update(
            {
                "attempts": attempts,
                "max_attempts": max_attempts,
                "attempt_history": tuple(history),
            }
        )
        return replace(result, metadata=metadata)

    def _resolve_target(self, step: Step, context: ExecutionContext) -> Any | None:
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
        target: Any | None,
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

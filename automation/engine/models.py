"""Immutable workflow definitions and explicit execution results."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from automation.engine.cancellation import CancellationToken


class ExecutionStatus(str, Enum):
    """Terminal state for an action, step, or workflow in Milestone 1."""

    EXECUTED_UNVERIFIED = "executed_unverified"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class Step:
    id: str
    action: str
    parameters: Mapping[str, Any] = field(default_factory=dict)
    name: str | None = None


@dataclass(frozen=True, slots=True)
class Workflow:
    name: str
    version: int
    steps: tuple[Step, ...]
    source_path: Path | None = None


@dataclass(slots=True)
class ExecutionContext:
    cancellation: CancellationToken = field(default_factory=CancellationToken)
    working_directory: Path | None = None


@dataclass(frozen=True, slots=True)
class ActionResult:
    status: ExecutionStatus
    message: str = ""
    error_type: str | None = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    @classmethod
    def executed_unverified(
        cls, message: str = "", *, metadata: Mapping[str, Any] | None = None
    ) -> "ActionResult":
        return cls(
            ExecutionStatus.EXECUTED_UNVERIFIED,
            message=message,
            metadata=metadata or {},
        )

    @classmethod
    def failed(
        cls,
        message: str,
        *,
        error_type: str | None = None,
        metadata: Mapping[str, Any] | None = None,
    ) -> "ActionResult":
        return cls(
            ExecutionStatus.FAILED,
            message=message,
            error_type=error_type,
            metadata=metadata or {},
        )

    @classmethod
    def cancelled(
        cls, message: str = "Workflow cancelled", *, metadata: Mapping[str, Any] | None = None
    ) -> "ActionResult":
        return cls(
            ExecutionStatus.CANCELLED,
            message=message,
            metadata=metadata or {},
        )


@dataclass(frozen=True, slots=True)
class StepResult:
    step_id: str
    action: str
    result: ActionResult

    @property
    def status(self) -> ExecutionStatus:
        return self.result.status


@dataclass(frozen=True, slots=True)
class WorkflowResult:
    workflow_name: str
    status: ExecutionStatus
    steps: tuple[StepResult, ...]

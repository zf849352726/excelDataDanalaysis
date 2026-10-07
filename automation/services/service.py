"""GUI-independent workflow discovery and single-run orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Callable

from automation.engine import (
    CancellationToken,
    ExecutionContext,
    ExecutionEvent,
    Workflow,
    WorkflowLoader,
    WorkflowResult,
)
from automation.runtime import create_default_executor


class AutomationServiceBusy(RuntimeError):
    """Raised when a second run is requested while one is active."""


@dataclass(frozen=True, slots=True)
class WorkflowSummary:
    workflow_id: str
    name: str
    path: Path
    steps: tuple[tuple[str, str, str | None], ...]


class AutomationService:
    """Own workflow discovery, execution state, and cooperative stopping."""

    def __init__(
        self,
        workflows_root: str | Path,
        *,
        loader: WorkflowLoader | None = None,
        executor_factory: Callable[[], object] = create_default_executor,
    ) -> None:
        self.workflows_root = Path(workflows_root).resolve()
        self._loader = loader or WorkflowLoader()
        self._executor_factory = executor_factory
        self._state_lock = Lock()
        self._active_context: ExecutionContext | None = None

    @property
    def is_running(self) -> bool:
        with self._state_lock:
            return self._active_context is not None

    def list_workflows(self) -> tuple[WorkflowSummary, ...]:
        if not self.workflows_root.is_dir():
            return ()
        summaries = [
            self._summarize(self._loader.load(path))
            for path in self.workflows_root.rglob("workflow.yaml")
        ]
        return tuple(sorted(summaries, key=lambda item: item.workflow_id.casefold()))

    def run_workflow(
        self,
        workflow_path: str | Path,
        event_handler: Callable[[ExecutionEvent], None] | None = None,
    ) -> WorkflowResult:
        workflow = self._load_managed_workflow(workflow_path)
        context = ExecutionContext(cancellation=CancellationToken())
        with self._state_lock:
            if self._active_context is not None:
                raise AutomationServiceBusy("A workflow is already running")
            self._active_context = context
        try:
            executor = self._executor_factory()
            return executor.execute(workflow, context, event_handler=event_handler)
        finally:
            with self._state_lock:
                self._active_context = None

    def stop_active(self) -> bool:
        with self._state_lock:
            context = self._active_context
        if context is None:
            return False
        context.cancellation.cancel()
        return True

    def _load_managed_workflow(self, workflow_path: str | Path) -> Workflow:
        path = Path(workflow_path).resolve()
        try:
            path.relative_to(self.workflows_root)
        except ValueError as exc:
            raise ValueError(
                "Workflow path must be inside the configured root"
            ) from exc
        if path.name != "workflow.yaml":
            raise ValueError("Workflow path must name workflow.yaml")
        return self._loader.load(path)

    def _summarize(self, workflow: Workflow) -> WorkflowSummary:
        if workflow.source_path is None:
            raise ValueError("A catalog workflow must have a source path")
        workflow_id = workflow.source_path.parent.relative_to(
            self.workflows_root
        ).as_posix()
        return WorkflowSummary(
            workflow_id=workflow_id,
            name=workflow.name,
            path=workflow.source_path,
            steps=tuple((step.id, step.action, step.name) for step in workflow.steps),
        )

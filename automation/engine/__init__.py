"""Public interfaces for the Automation Hub workflow engine."""

from automation.engine.cancellation import CancellationToken
from automation.engine.errors import (
    ActionRegistrationError,
    ActionFailed,
    AutomationError,
    AmbiguousTarget,
    LocatorRegistrationError,
    StepTimeout,
    TargetNotFound,
    UnknownActionError,
    VerificationFailed,
    VerifierRegistrationError,
    WorkflowCancelled,
    WorkflowValidationError,
)
from automation.engine.executor import WorkflowExecutor
from automation.engine.loader import WorkflowLoader
from automation.engine.models import (
    ActionResult,
    ExecutionContext,
    ExecutionStatus,
    ProcessReference,
    Step,
    StepResult,
    Workflow,
    WorkflowResult,
    VerificationResult,
)
from automation.engine.registry import Action, ActionRegistry

__all__ = [
    "Action",
    "ActionRegistry",
    "ActionRegistrationError",
    "ActionFailed",
    "ActionResult",
    "AmbiguousTarget",
    "AutomationError",
    "CancellationToken",
    "ExecutionContext",
    "ExecutionStatus",
    "LocatorRegistrationError",
    "StepTimeout",
    "ProcessReference",
    "Step",
    "StepResult",
    "UnknownActionError",
    "TargetNotFound",
    "VerificationFailed",
    "VerifierRegistrationError",
    "VerificationResult",
    "Workflow",
    "WorkflowExecutor",
    "WorkflowLoader",
    "WorkflowResult",
    "WorkflowCancelled",
    "WorkflowValidationError",
]

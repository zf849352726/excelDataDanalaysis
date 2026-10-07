"""Domain errors exposed by the Automation Hub engine."""


class AutomationError(Exception):
    """Base class for expected Automation Hub failures."""


class WorkflowValidationError(AutomationError):
    """Raised when workflow data does not match the supported schema."""


class ActionRegistrationError(AutomationError):
    """Raised when an action cannot be registered safely."""


class UnknownActionError(AutomationError):
    """Raised when a workflow requests an unregistered action."""


class LocatorRegistrationError(AutomationError):
    """Raised when a locator strategy cannot be registered safely."""


class VerifierRegistrationError(AutomationError):
    """Raised when a verifier cannot be registered safely."""


class ActionFailed(AutomationError):
    """Raised when an action cannot perform its declared operation."""


class TargetNotFound(AutomationError):
    """Raised when no declared locator strategy resolves a target."""


class AmbiguousTarget(AutomationError):
    """Raised when a locator cannot safely choose one candidate."""


class WorkflowCancelled(AutomationError):
    """Raised when cancellation interrupts target resolution or verification."""


class VerificationFailed(AutomationError):
    """Raised when an action's declared expectation is not met."""

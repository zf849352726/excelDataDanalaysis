"""Domain errors exposed by the Automation Hub engine."""


class AutomationError(Exception):
    """Base class for expected Automation Hub failures."""


class WorkflowValidationError(AutomationError):
    """Raised when workflow data does not match the supported schema."""


class ActionRegistrationError(AutomationError):
    """Raised when an action cannot be registered safely."""


class UnknownActionError(AutomationError):
    """Raised when a workflow requests an unregistered action."""

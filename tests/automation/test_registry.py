import pytest

from automation.engine import (
    ActionRegistrationError,
    ActionRegistry,
    UnknownActionError,
)


class PlaceholderAction:
    def execute(self, step, context):  # pragma: no cover - registry does not execute it
        raise AssertionError("not called")


def test_registry_uses_exact_action_names() -> None:
    registry = ActionRegistry()
    action = PlaceholderAction()
    registry.register("wait", action)

    assert registry.get("wait") is action
    with pytest.raises(UnknownActionError):
        registry.get("please_wait")


def test_registry_rejects_duplicate_names() -> None:
    registry = ActionRegistry()
    registry.register("wait", PlaceholderAction())

    with pytest.raises(ActionRegistrationError, match="already registered"):
        registry.register("wait", PlaceholderAction())

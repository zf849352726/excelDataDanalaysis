"""Built-in actions for the current Automation Hub milestone."""

from automation.actions.launch import LaunchAction
from automation.actions.uia import ClickAction, CloseWindowAction, TypeTextAction
from automation.actions.wait import WaitAction
from automation.engine.registry import ActionRegistry


def create_default_registry() -> ActionRegistry:
    registry = ActionRegistry()
    registry.register("wait", WaitAction())
    registry.register("launch", LaunchAction())
    registry.register("click", ClickAction())
    registry.register("type_text", TypeTextAction())
    registry.register("close_window", CloseWindowAction())
    return registry


__all__ = [
    "ClickAction",
    "CloseWindowAction",
    "LaunchAction",
    "TypeTextAction",
    "WaitAction",
    "create_default_registry",
]

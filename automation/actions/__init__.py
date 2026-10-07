"""Built-in actions for the current Automation Hub milestone."""

from automation.actions.launch import LaunchAction
from automation.actions.wait import WaitAction
from automation.engine.registry import ActionRegistry


def create_default_registry() -> ActionRegistry:
    registry = ActionRegistry()
    registry.register("wait", WaitAction())
    registry.register("launch", LaunchAction())
    return registry


__all__ = ["LaunchAction", "WaitAction", "create_default_registry"]

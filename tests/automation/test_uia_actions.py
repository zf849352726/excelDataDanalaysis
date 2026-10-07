from types import SimpleNamespace

import pytest

from automation.actions import ClickAction
from automation.actions.uia import CloseWindowAction, TypeTextAction
from automation.engine import ActionFailed, ExecutionContext, ExecutionStatus, Step
from automation.locators import LocatorResult


class FakeInvoke:
    def __init__(self) -> None:
        self.called = False

    def Invoke(self) -> None:
        self.called = True


class FakeValue:
    def __init__(self) -> None:
        self.CurrentValue = ""

    def SetValue(self, value: str) -> None:
        self.CurrentValue = value


class FakeWindow:
    def __init__(self) -> None:
        self.closed = False

    def Close(self) -> None:
        self.closed = True


class FakeElement:
    def __init__(self, control_type: str, automation_id: str = "") -> None:
        self.element_info = SimpleNamespace(
            control_type=control_type, automation_id=automation_id
        )
        self.iface_invoke = FakeInvoke()
        self.iface_value = FakeValue()
        self.iface_window = FakeWindow()
        self.children = []

    def top_level_parent(self):
        return self

    def descendants(self):
        return list(self.children)


def target_for(element: FakeElement) -> LocatorResult:
    return LocatorResult(
        True,
        "uia",
        element=element,
        metadata={"automation_id": "target", "window_is_new": True},
    )


def test_click_uses_semantic_invoke() -> None:
    element = FakeElement("Button")

    result = ClickAction().execute(
        Step("click", "click"), ExecutionContext(), target_for(element)
    )

    assert element.iface_invoke.called
    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED


def test_click_uses_only_resolved_image_coordinates() -> None:
    clicks: list[tuple[int, int]] = []
    target = LocatorResult(
        True,
        "image",
        x=42,
        y=73,
        confidence=0.97,
        metadata={"template": "button.png"},
    )

    result = ClickAction(lambda x, y: clicks.append((x, y))).execute(
        Step("click", "click"), ExecutionContext(), target
    )

    assert clicks == [(42, 73)]
    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED


def test_type_text_uses_semantic_set_value() -> None:
    element = FakeElement("Document")

    result = TypeTextAction().execute(
        Step("type", "type_text", {"text": "Hello"}),
        ExecutionContext(),
        target_for(element),
    )

    assert element.iface_value.CurrentValue == "Hello"
    assert result.metadata["text_length"] == 5


def test_close_window_requires_window_target() -> None:
    with pytest.raises(ActionFailed, match="CloseButton"):
        CloseWindowAction().execute(
            Step("close", "close_window"),
            ExecutionContext(),
            target_for(FakeElement("Button")),
        )


def test_close_window_closes_only_resolved_window() -> None:
    element = FakeElement("Window")

    CloseWindowAction().execute(
        Step("close", "close_window"), ExecutionContext(), target_for(element)
    )

    assert element.iface_window.closed


def test_close_window_invokes_resolved_document_close_button() -> None:
    element = FakeElement("Button", "CloseButton")

    CloseWindowAction().execute(
        Step("close", "close_window"), ExecutionContext(), target_for(element)
    )

    assert element.iface_invoke.called


def test_close_window_discards_only_declared_save_prompt() -> None:
    element = FakeElement("Window")
    discard = FakeElement("Button", "CommandButton_7")
    element.children = [discard]

    CloseWindowAction().execute(
        Step("close", "close_window", {"discard_changes": True}),
        ExecutionContext(),
        target_for(element),
    )

    assert element.iface_window.closed
    assert discard.iface_invoke.called

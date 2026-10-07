from types import SimpleNamespace

from automation.engine import ExecutionContext
from automation.locators import LocatorResult
from automation.verification.uia import (
    UIADisappearedVerifier,
    UIAExistsVerifier,
    UIATextEqualsVerifier,
)


class StaticChain:
    def __init__(self, result) -> None:
        self.result = result

    def resolve(self, target, context):
        return self.result

    def locate_once(self, target, context):
        return self.result


def text_target(value: str) -> LocatorResult:
    element = SimpleNamespace(iface_value=SimpleNamespace(CurrentValue=value))
    return LocatorResult(True, "uia", element=element)


def test_uia_exists_reports_resolved_metadata() -> None:
    resolved = LocatorResult(True, "uia", element=object(), metadata={"handle": 10})

    result = UIAExistsVerifier().verify(
        {"target": {"strategies": ()}},
        ExecutionContext(),
        None,
        StaticChain(resolved),
    )

    assert result.passed
    assert result.metadata["handle"] == 10


def test_uia_text_equals_uses_action_target() -> None:
    result = UIATextEqualsVerifier().verify(
        {"target": None, "value": "Hello"},
        ExecutionContext(),
        text_target("Hello"),
        StaticChain(None),
    )

    assert result.passed


def test_uia_disappeared_passes_when_locator_returns_none() -> None:
    result = UIADisappearedVerifier().verify(
        {"target": {"strategies": ()}},
        ExecutionContext(),
        None,
        StaticChain(None),
    )

    assert result.passed

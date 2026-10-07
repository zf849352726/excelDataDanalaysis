import pytest

from automation.engine import AmbiguousTarget, CancellationToken, ExecutionContext
from automation.engine.errors import WorkflowCancelled
from automation.locators import LocatorChain, LocatorRegistry, LocatorResult


class FakeLocator:
    def __init__(self, result: LocatorResult, calls: list[str], name: str) -> None:
        self.result = result
        self.calls = calls
        self.name = name
        self.began = False

    def begin(self, context: ExecutionContext) -> None:
        self.began = True

    def locate(self, selector, context: ExecutionContext) -> LocatorResult:
        self.calls.append(self.name)
        return self.result


def test_locator_chain_honors_declared_strategy_order() -> None:
    calls: list[str] = []
    registry = LocatorRegistry()
    first = FakeLocator(LocatorResult(False, "first"), calls, "first")
    second = FakeLocator(LocatorResult(True, "second", element=object()), calls, "second")
    registry.register("first", first)
    registry.register("second", second)
    chain = LocatorChain(registry, timeout_seconds=0)
    context = ExecutionContext()
    chain.begin(context)

    result = chain.resolve(
        {"strategies": ({"type": "first"}, {"type": "second"})}, context
    )

    assert result.strategy == "second"
    assert calls == ["first", "second"]
    assert first.began and second.began


def test_locator_chain_stops_on_ambiguity() -> None:
    registry = LocatorRegistry()
    registry.register(
        "uia",
        FakeLocator(
            LocatorResult(
                False,
                "uia",
                ambiguous=True,
                metadata={"candidate_count": 2},
            ),
            [],
            "uia",
        ),
    )

    with pytest.raises(AmbiguousTarget, match="candidate_count"):
        LocatorChain(registry, timeout_seconds=0).resolve(
            {"strategies": ({"type": "uia"},)}, ExecutionContext()
        )


def test_locator_chain_honors_cancellation() -> None:
    token = CancellationToken()
    token.cancel()
    registry = LocatorRegistry()
    registry.register(
        "none", FakeLocator(LocatorResult(False, "none"), [], "none")
    )

    with pytest.raises(WorkflowCancelled):
        LocatorChain(registry, timeout_seconds=5).resolve(
            {"strategies": ({"type": "none"},)},
            ExecutionContext(cancellation=token),
        )

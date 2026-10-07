"""Ordered, cancellable locator strategy execution."""

from __future__ import annotations

import time
from typing import Any, Mapping

from automation.engine.errors import (
    AmbiguousTarget,
    TargetNotFound,
    WorkflowCancelled,
)
from automation.engine.models import ExecutionContext
from automation.locators.models import LocatorResult
from automation.locators.registry import LocatorRegistry


class LocatorChain:
    def __init__(
        self,
        registry: LocatorRegistry,
        *,
        timeout_seconds: float = 5.0,
        poll_interval_seconds: float = 0.1,
    ) -> None:
        self._registry = registry
        self._timeout_seconds = timeout_seconds
        self._poll_interval_seconds = poll_interval_seconds

    def begin(self, context: ExecutionContext) -> None:
        for locator in self._registry.locators:
            locator.begin(context)

    def resolve(
        self, target: Mapping[str, Any], context: ExecutionContext
    ) -> LocatorResult:
        deadline = time.monotonic() + self._timeout_seconds
        attempts: list[Mapping[str, Any]] = []
        while True:
            result = self.locate_once(target, context, attempts=attempts)
            if result is not None:
                return result
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled("Target resolution cancelled")
            if time.monotonic() >= deadline:
                raise TargetNotFound(
                    f"No locator strategy resolved the target; attempts={attempts}"
                )
            context.cancellation.wait(self._poll_interval_seconds)

    def locate_once(
        self,
        target: Mapping[str, Any],
        context: ExecutionContext,
        *,
        attempts: list[Mapping[str, Any]] | None = None,
    ) -> LocatorResult | None:
        for selector in target["strategies"]:
            strategy = selector["type"]
            result = self._registry.get(strategy).locate(selector, context)
            if attempts is not None:
                attempts.append(
                    {
                        "strategy": strategy,
                        "found": result.found,
                        "ambiguous": result.ambiguous,
                        **dict(result.metadata),
                    }
                )
            if result.ambiguous:
                raise AmbiguousTarget(
                    f"Locator strategy '{strategy}' returned ambiguous candidates: "
                    f"{dict(result.metadata)}"
                )
            if result.found:
                return result
        return None

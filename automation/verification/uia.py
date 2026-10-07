"""Minimal UIA verifiers required by the Notepad vertical slice."""

from __future__ import annotations

import time
from typing import Any, Mapping

from automation.engine.errors import WorkflowCancelled
from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain
from automation.locators.models import LocatorResult


class UIAExistsVerifier:
    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        result = locator_chain.resolve(expectation["target"], context)
        return VerificationResult(
            True,
            "UIA target exists",
            metadata=dict(result.metadata),
        )


class UIATextEqualsVerifier:
    _TIMEOUT_SECONDS = 5.0
    _POLL_INTERVAL_SECONDS = 0.1

    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        target_spec = expectation.get("target")
        target = (
            locator_chain.resolve(target_spec, context)
            if target_spec is not None
            else action_target
        )
        if not isinstance(target, LocatorResult) or target.element is None:
            return VerificationResult(False, "UIA text verification has no target")

        expected = expectation["value"]
        deadline = time.monotonic() + self._TIMEOUT_SECONDS
        actual = None
        while True:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled("UIA text verification cancelled")
            actual = target.element.iface_value.CurrentValue
            if actual == expected:
                return VerificationResult(
                    True,
                    "UIA text equals expected value",
                    metadata={"expected": expected, "actual": actual},
                )
            if time.monotonic() >= deadline:
                return VerificationResult(
                    False,
                    f"UIA text mismatch: expected {expected!r}, got {actual!r}",
                    metadata={"expected": expected, "actual": actual},
                )
            context.cancellation.wait(self._POLL_INTERVAL_SECONDS)


class UIADisappearedVerifier:
    _TIMEOUT_SECONDS = 5.0
    _POLL_INTERVAL_SECONDS = 0.1

    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        deadline = time.monotonic() + self._TIMEOUT_SECONDS
        while True:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled("UIA disappearance verification cancelled")
            target = locator_chain.locate_once(expectation["target"], context)
            if target is None:
                return VerificationResult(True, "UIA target disappeared")
            if time.monotonic() >= deadline:
                return VerificationResult(
                    False,
                    "UIA target still exists",
                    metadata=dict(target.metadata),
                )
            context.cancellation.wait(self._POLL_INTERVAL_SECONDS)

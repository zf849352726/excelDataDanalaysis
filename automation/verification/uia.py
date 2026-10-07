"""Minimal UIA verifiers required by the Notepad vertical slice."""

from __future__ import annotations

from typing import Any, Mapping

from automation.engine.errors import WorkflowCancelled
from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain
from automation.locators.models import LocatorResult
from automation.verification.target import (
    TargetDisappearedVerifier,
    TargetExistsVerifier,
)
from automation.verification.timing import verification_deadline, wait_for_poll


class UIAExistsVerifier(TargetExistsVerifier):
    def __init__(self) -> None:
        super().__init__("UIA target")


class UIATextEqualsVerifier:
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
        deadline = verification_deadline(context)
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
            if not wait_for_poll(context, deadline):
                return VerificationResult(
                    False,
                    f"UIA text mismatch: expected {expected!r}, got {actual!r}",
                    metadata={"expected": expected, "actual": actual},
                )


class UIADisappearedVerifier(TargetDisappearedVerifier):
    def __init__(self) -> None:
        super().__init__("UIA target")

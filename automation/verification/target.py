"""Reusable existence and disappearance verification for locator targets."""

from __future__ import annotations

from typing import Any, Mapping

from automation.engine.errors import WorkflowCancelled
from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain
from automation.verification.timing import verification_deadline, wait_for_poll


class TargetExistsVerifier:
    def __init__(self, label: str = "Target") -> None:
        self._label = label

    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        deadline = verification_deadline(context)
        attempts = 0
        while True:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled(f"{self._label} existence verification cancelled")
            attempts += 1
            result = locator_chain.locate_once(expectation["target"], context)
            if result is not None:
                metadata = dict(result.metadata)
                metadata.update(
                    {
                        "attempts": attempts,
                        "strategy": result.strategy,
                        "confidence": result.confidence,
                    }
                )
                return VerificationResult(True, f"{self._label} exists", metadata)
            if not wait_for_poll(context, deadline):
                return VerificationResult(
                    False,
                    f"{self._label} did not appear before timeout",
                    {"attempts": attempts},
                )


class TargetDisappearedVerifier:
    def __init__(self, label: str = "Target") -> None:
        self._label = label

    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        deadline = verification_deadline(context)
        attempts = 0
        last_metadata: dict[str, Any] = {}
        while True:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled(
                    f"{self._label} disappearance verification cancelled"
                )
            attempts += 1
            result = locator_chain.locate_once(expectation["target"], context)
            if result is None:
                return VerificationResult(
                    True,
                    f"{self._label} disappeared",
                    {"attempts": attempts},
                )
            last_metadata = dict(result.metadata)
            if not wait_for_poll(context, deadline):
                last_metadata["attempts"] = attempts
                return VerificationResult(
                    False,
                    f"{self._label} still exists after timeout",
                    last_metadata,
                )

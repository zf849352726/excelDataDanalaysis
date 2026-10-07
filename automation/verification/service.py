"""Verification dispatcher used by the workflow executor."""

from __future__ import annotations

from typing import Any, Mapping

from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain
from automation.verification.registry import VerificationRegistry


class DefaultVerificationService:
    def __init__(
        self, registry: VerificationRegistry, locator_chain: LocatorChain
    ) -> None:
        self._registry = registry
        self._locator_chain = locator_chain

    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
    ) -> VerificationResult:
        verifier = self._registry.get(expectation["type"])
        return verifier.verify(
            expectation, context, action_target, self._locator_chain
        )

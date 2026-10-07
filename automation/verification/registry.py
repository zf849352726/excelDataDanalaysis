"""Explicit verifier registration."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from automation.engine.errors import VerificationFailed, VerifierRegistrationError
from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain


class Verifier(Protocol):
    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        """Evaluate an expectation without executing an action."""


class VerificationRegistry:
    def __init__(self) -> None:
        self._verifiers: dict[str, Verifier] = {}

    def register(self, name: str, verifier: Verifier) -> None:
        if not isinstance(name, str) or not name:
            raise VerifierRegistrationError("Verifier name must be a non-empty string")
        if name in self._verifiers:
            raise VerifierRegistrationError(f"Verifier '{name}' is already registered")
        self._verifiers[name] = verifier

    def get(self, name: str) -> Verifier:
        try:
            return self._verifiers[name]
        except KeyError as exc:
            raise VerificationFailed(f"Verifier '{name}' is not registered") from exc

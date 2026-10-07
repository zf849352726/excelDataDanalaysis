"""Narrow engine-facing interfaces for target resolution and verification."""

from __future__ import annotations

from typing import Any, Mapping, Protocol

from automation.engine.models import ExecutionContext, VerificationResult


class TargetResolver(Protocol):
    def begin(self, context: ExecutionContext) -> None:
        """Capture any per-run state before the first action executes."""

    def resolve(
        self, target: Mapping[str, Any], context: ExecutionContext
    ) -> Any:
        """Resolve exactly one target or raise a domain error."""


class VerificationService(Protocol):
    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
    ) -> VerificationResult:
        """Evaluate one expectation without performing the action."""

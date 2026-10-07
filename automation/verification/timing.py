"""Shared cooperative timing helpers for verification loops."""

from __future__ import annotations

import time

from automation.engine.errors import WorkflowCancelled
from automation.engine.models import ExecutionContext


def verification_deadline(
    context: ExecutionContext, default_timeout_seconds: float = 5.0
) -> float:
    return context.deadline or time.monotonic() + default_timeout_seconds


def wait_for_poll(
    context: ExecutionContext, deadline: float, poll_interval_seconds: float = 0.1
) -> bool:
    if context.cancellation.is_cancelled:
        raise WorkflowCancelled("Verification cancelled")
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        return False
    if context.cancellation.wait(min(poll_interval_seconds, remaining)):
        raise WorkflowCancelled("Verification cancelled")
    return time.monotonic() < deadline

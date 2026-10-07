"""Workflow-relative filesystem outcome verification."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

from automation.engine.errors import WorkflowCancelled
from automation.engine.models import ExecutionContext, VerificationResult
from automation.locators.chain import LocatorChain
from automation.verification.timing import verification_deadline, wait_for_poll


class FileExistsVerifier:
    def verify(
        self,
        expectation: Mapping[str, Any],
        context: ExecutionContext,
        action_target: Any | None,
        locator_chain: LocatorChain,
    ) -> VerificationResult:
        path = Path(expectation["path"])
        if context.working_directory is not None:
            path = context.working_directory / path
        path = path.resolve()
        deadline = verification_deadline(context)
        attempts = 0
        while True:
            if context.cancellation.is_cancelled:
                raise WorkflowCancelled("File existence verification cancelled")
            attempts += 1
            if path.is_file():
                return VerificationResult(
                    True,
                    "File exists",
                    {"path": str(path), "attempts": attempts},
                )
            if not wait_for_poll(context, deadline):
                return VerificationResult(
                    False,
                    "File did not appear before timeout",
                    {"path": str(path), "attempts": attempts},
                )

"""Safe process launch action with cooperative cancellation while waiting."""

from __future__ import annotations

import subprocess
from typing import Any

from automation.engine.models import (
    ActionResult,
    ExecutionContext,
    ProcessReference,
    Step,
)


class LaunchAction:
    _POLL_INTERVAL_SECONDS = 0.05
    _TERMINATE_TIMEOUT_SECONDS = 2.0

    def execute(
        self, step: Step, context: ExecutionContext, target: Any | None = None
    ) -> ActionResult:
        program = step.parameters["program"]
        args = step.parameters["args"]
        wait_for_exit = step.parameters["wait_for_exit"]
        process_alias = step.parameters.get("process_alias")
        command = [program, *args]

        if process_alias and process_alias in context.processes:
            return ActionResult.failed(
                f"Process alias '{process_alias}' is already in use",
                error_type="ActionFailed",
            )

        try:
            process = subprocess.Popen(
                command,
                cwd=context.working_directory,
                shell=False,
            )
        except OSError as exc:
            return ActionResult.failed(
                f"Could not launch '{program}': {exc}",
                error_type=type(exc).__name__,
                metadata={"program": program},
            )

        metadata: dict[str, Any] = {"pid": process.pid, "program": program}
        if process_alias:
            context.processes[process_alias] = ProcessReference(
                alias=process_alias,
                starter_pid=process.pid,
                program=program,
            )
            metadata["process_alias"] = process_alias
        if not wait_for_exit:
            return ActionResult.executed_unverified(
                f"Launched '{program}'", metadata=metadata
            )

        while True:
            if context.cancellation.is_cancelled:
                self._stop_owned_process(process)
                return ActionResult.cancelled(
                    f"Cancelled while waiting for '{program}'", metadata=metadata
                )

            exit_code = process.poll()
            if exit_code is not None:
                metadata["exit_code"] = exit_code
                if exit_code != 0:
                    return ActionResult.failed(
                        f"'{program}' exited with code {exit_code}",
                        error_type="ProcessExitError",
                        metadata=metadata,
                    )
                return ActionResult.executed_unverified(
                    f"'{program}' exited with code 0", metadata=metadata
                )

            context.cancellation.wait(self._POLL_INTERVAL_SECONDS)

    def _stop_owned_process(self, process: subprocess.Popen[Any]) -> None:
        if process.poll() is not None:
            return
        process.terminate()
        try:
            process.wait(timeout=self._TERMINATE_TIMEOUT_SECONDS)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=self._TERMINATE_TIMEOUT_SECONDS)

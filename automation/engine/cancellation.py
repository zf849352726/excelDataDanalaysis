"""Cooperative cancellation primitives."""

from threading import Event


class CancellationToken:
    """Thread-safe cancellation signal shared by an execution and its actions."""

    def __init__(self) -> None:
        self._event = Event()

    def cancel(self) -> None:
        self._event.set()

    @property
    def is_cancelled(self) -> bool:
        return self._event.is_set()

    def wait(self, timeout: float) -> bool:
        """Wait up to ``timeout`` seconds and return whether cancellation occurred."""

        return self._event.wait(timeout)

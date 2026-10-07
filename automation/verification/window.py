"""Top-level window outcome verifiers."""

from automation.verification.target import (
    TargetDisappearedVerifier,
    TargetExistsVerifier,
)


class WindowExistsVerifier(TargetExistsVerifier):
    def __init__(self) -> None:
        super().__init__("Window")


class WindowDisappearedVerifier(TargetDisappearedVerifier):
    def __init__(self) -> None:
        super().__init__("Window")

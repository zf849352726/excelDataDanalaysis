"""Image outcome verifiers."""

from automation.verification.target import (
    TargetDisappearedVerifier,
    TargetExistsVerifier,
)


class ImageExistsVerifier(TargetExistsVerifier):
    def __init__(self) -> None:
        super().__init__("Image target")


class ImageDisappearedVerifier(TargetDisappearedVerifier):
    def __init__(self) -> None:
        super().__init__("Image target")

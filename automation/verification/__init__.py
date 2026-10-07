"""Outcome verification for Automation Hub workflows."""

from automation.verification.registry import VerificationRegistry
from automation.verification.service import DefaultVerificationService
from automation.verification.file import FileExistsVerifier
from automation.verification.image import ImageDisappearedVerifier, ImageExistsVerifier
from automation.verification.uia import (
    UIADisappearedVerifier,
    UIAExistsVerifier,
    UIATextEqualsVerifier,
)
from automation.verification.window import WindowDisappearedVerifier, WindowExistsVerifier

__all__ = [
    "DefaultVerificationService",
    "FileExistsVerifier",
    "ImageDisappearedVerifier",
    "ImageExistsVerifier",
    "UIADisappearedVerifier",
    "UIAExistsVerifier",
    "UIATextEqualsVerifier",
    "VerificationRegistry",
    "WindowDisappearedVerifier",
    "WindowExistsVerifier",
]

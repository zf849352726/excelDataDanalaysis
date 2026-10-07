"""Outcome verification for Automation Hub workflows."""

from automation.verification.registry import VerificationRegistry
from automation.verification.service import DefaultVerificationService
from automation.verification.uia import (
    UIADisappearedVerifier,
    UIAExistsVerifier,
    UIATextEqualsVerifier,
)

__all__ = [
    "DefaultVerificationService",
    "UIADisappearedVerifier",
    "UIAExistsVerifier",
    "UIATextEqualsVerifier",
    "VerificationRegistry",
]

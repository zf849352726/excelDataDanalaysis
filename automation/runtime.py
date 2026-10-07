"""Composition root for the local deterministic Automation Hub runtime."""

from automation.actions import create_default_registry
from automation.engine.executor import WorkflowExecutor
from automation.locators import ImageLocator, LocatorChain, LocatorRegistry, UIALocator
from automation.verification import (
    DefaultVerificationService,
    UIADisappearedVerifier,
    UIAExistsVerifier,
    UIATextEqualsVerifier,
    VerificationRegistry,
)


def create_default_executor() -> WorkflowExecutor:
    locator_registry = LocatorRegistry()
    locator_registry.register("uia", UIALocator())
    locator_registry.register("image", ImageLocator())
    locator_chain = LocatorChain(locator_registry)

    verifier_registry = VerificationRegistry()
    verifier_registry.register("uia_exists", UIAExistsVerifier())
    verifier_registry.register("uia_text_equals", UIATextEqualsVerifier())
    verifier_registry.register("uia_disappeared", UIADisappearedVerifier())

    verification_service = DefaultVerificationService(
        verifier_registry, locator_chain
    )
    return WorkflowExecutor(
        create_default_registry(),
        target_resolver=locator_chain,
        verification_service=verification_service,
    )

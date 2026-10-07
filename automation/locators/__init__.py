"""Target resolution for Automation Hub workflows."""

from automation.locators.chain import LocatorChain
from automation.locators.image import ImageLocator
from automation.locators.models import LocatorResult
from automation.locators.registry import Locator, LocatorRegistry
from automation.locators.uia import UIALocator

__all__ = [
    "Locator",
    "LocatorChain",
    "LocatorRegistry",
    "LocatorResult",
    "ImageLocator",
    "UIALocator",
]

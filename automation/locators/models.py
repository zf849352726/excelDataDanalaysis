"""Common locator result shape."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True, slots=True)
class LocatorResult:
    found: bool
    strategy: str
    x: int | None = None
    y: int | None = None
    bounds: tuple[int, int, int, int] | None = None
    confidence: float | None = None
    element: Any | None = None
    ambiguous: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

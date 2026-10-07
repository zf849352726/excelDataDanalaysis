"""Multi-scale image locator with confidence and ambiguity reporting."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Mapping

import cv2
import numpy as np

from automation.engine.models import ExecutionContext
from automation.locators.models import LocatorResult


@dataclass(frozen=True, slots=True)
class _Candidate:
    confidence: float
    left: int
    top: int
    width: int
    height: int
    scale: float

    @property
    def center(self) -> tuple[int, int]:
        return self.left + self.width // 2, self.top + self.height // 2


def _capture_primary_screen() -> np.ndarray:
    import pyautogui

    return np.asarray(pyautogui.screenshot())


class ImageLocator:
    """Resolve the best distinct template match across declared scales."""

    def __init__(
        self, screenshot_provider: Callable[[], np.ndarray] | None = None
    ) -> None:
        self._screenshot_provider = screenshot_provider or _capture_primary_screen

    def begin(self, context: ExecutionContext) -> None:
        return None

    def locate(
        self, selector: Mapping[str, Any], context: ExecutionContext
    ) -> LocatorResult:
        template_path = self._resolve_template(selector["template"], context)
        template = cv2.imread(str(template_path), cv2.IMREAD_GRAYSCALE)
        if template is None:
            return LocatorResult(
                False,
                "image",
                metadata={"template": str(template_path), "reason": "template_unreadable"},
            )

        screen = self._to_grayscale(self._screenshot_provider())
        candidates: list[_Candidate] = []
        for scale in selector["scales"]:
            width = max(1, round(template.shape[1] * scale))
            height = max(1, round(template.shape[0] * scale))
            if width > screen.shape[1] or height > screen.shape[0]:
                continue
            interpolation = cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR
            resized = cv2.resize(template, (width, height), interpolation=interpolation)
            scores = cv2.matchTemplate(screen, resized, cv2.TM_CCOEFF_NORMED)
            candidates.extend(self._best_two(scores, width, height, scale))

        distinct = self._distinct_candidates(candidates)
        threshold = selector["threshold"]
        metadata: dict[str, Any] = {
            "template": str(template_path),
            "threshold": threshold,
            "scales": tuple(selector["scales"]),
            "candidate_count": len(distinct),
        }
        if not distinct or distinct[0].confidence < threshold:
            if distinct:
                metadata["best_confidence"] = distinct[0].confidence
            return LocatorResult(False, "image", metadata=metadata)

        best = distinct[0]
        metadata.update({"scale": best.scale, "best_confidence": best.confidence})
        if len(distinct) > 1:
            second = distinct[1]
            metadata["second_confidence"] = second.confidence
            if (
                second.confidence >= threshold
                and best.confidence - second.confidence <= selector["ambiguity_margin"]
            ):
                metadata["ambiguity_margin"] = selector["ambiguity_margin"]
                return LocatorResult(
                    False,
                    "image",
                    confidence=best.confidence,
                    ambiguous=True,
                    metadata=metadata,
                )

        center_x, center_y = best.center
        return LocatorResult(
            True,
            "image",
            x=center_x,
            y=center_y,
            bounds=(best.left, best.top, best.left + best.width, best.top + best.height),
            confidence=best.confidence,
            metadata=metadata,
        )

    @staticmethod
    def _resolve_template(template: str, context: ExecutionContext) -> Path:
        path = Path(template)
        if context.working_directory is not None:
            path = context.working_directory / path
        return path.resolve()

    @staticmethod
    def _to_grayscale(image: np.ndarray) -> np.ndarray:
        array = np.asarray(image)
        if array.ndim == 2:
            return array
        if array.ndim == 3 and array.shape[2] in {3, 4}:
            conversion = cv2.COLOR_RGBA2GRAY if array.shape[2] == 4 else cv2.COLOR_RGB2GRAY
            return cv2.cvtColor(array, conversion)
        raise ValueError(f"Unsupported screenshot shape: {array.shape}")

    @staticmethod
    def _best_two(
        scores: np.ndarray, width: int, height: int, scale: float
    ) -> list[_Candidate]:
        remaining = scores.copy()
        found: list[_Candidate] = []
        for _ in range(2):
            _, confidence, _, location = cv2.minMaxLoc(remaining)
            if not np.isfinite(confidence):
                break
            left, top = location
            found.append(_Candidate(float(confidence), left, top, width, height, scale))
            x0 = max(0, left - width // 2)
            y0 = max(0, top - height // 2)
            x1 = min(remaining.shape[1], left + width // 2 + 1)
            y1 = min(remaining.shape[0], top + height // 2 + 1)
            remaining[y0:y1, x0:x1] = -np.inf
        return found

    @staticmethod
    def _distinct_candidates(candidates: list[_Candidate]) -> list[_Candidate]:
        distinct: list[_Candidate] = []
        for candidate in sorted(candidates, key=lambda item: item.confidence, reverse=True):
            cx, cy = candidate.center
            if any(
                abs(cx - other.center[0]) <= max(3, min(candidate.width, other.width) // 4)
                and abs(cy - other.center[1]) <= max(3, min(candidate.height, other.height) // 4)
                for other in distinct
            ):
                continue
            distinct.append(candidate)
        return distinct

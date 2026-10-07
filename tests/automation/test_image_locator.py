from pathlib import Path

import cv2
import numpy as np

from automation.engine import ExecutionContext
from automation.locators import ImageLocator


def make_template() -> np.ndarray:
    template = np.zeros((14, 18), dtype=np.uint8)
    template[2:12, 3:15] = 180
    template[4:9, 7:11] = 255
    template[10:12, 13:16] = 70
    return template


def selector(template: Path, *, scales=None, ambiguity_margin=0.02):
    return {
        "type": "image",
        "template": template.name,
        "threshold": 0.9,
        "scales": tuple(scales or [1.0]),
        "ambiguity_margin": ambiguity_margin,
    }


def test_image_locator_returns_best_match_and_confidence(tmp_path: Path) -> None:
    template = make_template()
    template_path = tmp_path / "target.png"
    cv2.imwrite(str(template_path), template)
    screen = np.zeros((90, 120), dtype=np.uint8)
    screen[31:45, 52:70] = template

    result = ImageLocator(lambda: screen).locate(
        selector(template_path), ExecutionContext(working_directory=tmp_path)
    )

    assert result.found
    assert not result.ambiguous
    assert result.bounds == (52, 31, 70, 45)
    assert result.x == 61 and result.y == 38
    assert result.confidence is not None and result.confidence > 0.99
    assert result.metadata["scale"] == 1.0


def test_image_locator_selects_matching_scale(tmp_path: Path) -> None:
    template = make_template()
    template_path = tmp_path / "target.png"
    cv2.imwrite(str(template_path), template)
    scaled = cv2.resize(template, (27, 21), interpolation=cv2.INTER_LINEAR)
    screen = np.zeros((100, 140), dtype=np.uint8)
    screen[40:61, 70:97] = scaled

    result = ImageLocator(lambda: screen).locate(
        selector(template_path, scales=[1.0, 1.5]),
        ExecutionContext(working_directory=tmp_path),
    )

    assert result.found
    assert result.metadata["scale"] == 1.5
    assert result.bounds == (70, 40, 97, 61)


def test_image_locator_reports_two_similar_matches_as_ambiguous(tmp_path: Path) -> None:
    template = make_template()
    template_path = tmp_path / "target.png"
    cv2.imwrite(str(template_path), template)
    screen = np.zeros((100, 150), dtype=np.uint8)
    screen[15:29, 20:38] = template
    screen[60:74, 100:118] = template

    result = ImageLocator(lambda: screen).locate(
        selector(template_path), ExecutionContext(working_directory=tmp_path)
    )

    assert not result.found
    assert result.ambiguous
    assert result.confidence is not None and result.confidence > 0.99
    assert result.metadata["second_confidence"] > 0.99

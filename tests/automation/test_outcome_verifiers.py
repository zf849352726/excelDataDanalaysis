import time
from pathlib import Path

from automation.engine import ExecutionContext
from automation.locators import LocatorResult
from automation.verification import (
    FileExistsVerifier,
    ImageDisappearedVerifier,
    ImageExistsVerifier,
    WindowExistsVerifier,
)


class SequenceChain:
    def __init__(self, results) -> None:
        self.results = list(results)
        self.calls = 0

    def locate_once(self, target, context):
        index = min(self.calls, len(self.results) - 1)
        self.calls += 1
        return self.results[index]


def short_context(tmp_path: Path | None = None) -> ExecutionContext:
    return ExecutionContext(
        working_directory=tmp_path,
        deadline=time.monotonic() + 0.15,
    )


def test_image_exists_reports_locator_confidence() -> None:
    located = LocatorResult(
        True,
        "image",
        confidence=0.94,
        metadata={"template": "button.png"},
    )

    result = ImageExistsVerifier().verify(
        {"target": {"strategies": ()}},
        short_context(),
        None,
        SequenceChain([None, located]),
    )

    assert result.passed
    assert result.metadata["confidence"] == 0.94
    assert result.metadata["attempts"] == 2


def test_image_disappeared_polls_until_absent() -> None:
    located = LocatorResult(True, "image", confidence=0.9)

    result = ImageDisappearedVerifier().verify(
        {"target": {"strategies": ()}},
        short_context(),
        None,
        SequenceChain([located, None]),
    )

    assert result.passed
    assert result.metadata["attempts"] == 2


def test_window_exists_failure_is_explicit() -> None:
    result = WindowExistsVerifier().verify(
        {"target": {"strategies": ()}},
        short_context(),
        None,
        SequenceChain([None]),
    )

    assert not result.passed
    assert "timeout" in result.message


def test_file_exists_resolves_from_workflow_directory(tmp_path: Path) -> None:
    output = tmp_path / "output" / "report.xlsx"
    output.parent.mkdir()
    output.write_bytes(b"report")

    result = FileExistsVerifier().verify(
        {"path": "output/report.xlsx"},
        short_context(tmp_path),
        None,
        SequenceChain([None]),
    )

    assert result.passed
    assert result.metadata["path"] == str(output.resolve())

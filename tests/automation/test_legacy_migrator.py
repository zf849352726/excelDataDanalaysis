import hashlib
from pathlib import Path

import pytest

from automation.actions import ClickAction, WaitAction
from automation.engine import (
    ActionRegistry,
    ExecutionContext,
    ExecutionStatus,
    WorkflowExecutor,
    WorkflowLoader,
)
from automation.engine.errors import LegacyMigrationError
from automation.legacy import migrate_task_directory, parse_legacy_filename
from automation.locators import LocatorResult


class StaticTargetResolver:
    def begin(self, context: ExecutionContext) -> None:
        return None

    def resolve(self, target, context: ExecutionContext) -> LocatorResult:
        return LocatorResult(True, "image", x=25, y=30, confidence=0.95)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_parse_legacy_filename_is_explicit() -> None:
    step = parse_legacy_filename("12-click_export.png")

    assert step.order == 12
    assert step.action == "click"
    assert step.argument == "export"

    with pytest.raises(LegacyMigrationError, match="unsupported"):
        parse_legacy_filename("0-press_enter.png")


def test_migration_copies_assets_and_generates_runnable_unverified_workflow(
    tmp_path: Path,
) -> None:
    source = tmp_path / "legacy_task"
    source.mkdir()
    (source / "0-click_button.png").write_bytes(b"click-asset")
    (source / "1-sleep_0.png").write_bytes(b"sleep-asset")
    source_hashes = {path.name: digest(path) for path in source.iterdir()}
    destination = tmp_path / "workflow"

    migration = migrate_task_directory(source, destination)
    workflow = WorkflowLoader().load(migration.workflow_path)

    assert [step.action for step in workflow.steps] == ["click", "wait"]
    assert all(step.expectation is None for step in workflow.steps)
    assert {path.name: digest(path) for path in source.iterdir()} == source_hashes
    assert {
        path.name: digest(path) for path in (destination / "assets").iterdir()
    } == source_hashes

    clicks: list[tuple[int, int]] = []
    registry = ActionRegistry()
    registry.register("click", ClickAction(lambda x, y: clicks.append((x, y))))
    registry.register("wait", WaitAction())
    result = WorkflowExecutor(registry, StaticTargetResolver()).execute(workflow)

    assert result.status is ExecutionStatus.EXECUTED_UNVERIFIED
    assert clicks == [(25, 30)]
    assert all(
        step.status is ExecutionStatus.EXECUTED_UNVERIFIED for step in result.steps
    )


def test_migration_refuses_to_overwrite_destination(tmp_path: Path) -> None:
    source = tmp_path / "legacy_task"
    source.mkdir()
    (source / "0-sleep_0.png").write_bytes(b"asset")
    destination = tmp_path / "workflow"
    destination.mkdir()

    with pytest.raises(LegacyMigrationError, match="refusing to overwrite"):
        migrate_task_directory(source, destination)


def test_committed_workflows_are_reproducible_from_active_legacy_tasks(
    tmp_path: Path,
) -> None:
    project_root = Path(__file__).resolve().parents[2]
    fixture_root = Path(__file__).parent / "fixtures" / "legacy"
    for task_name in ("auto_click", "click_next_page"):
        generated = tmp_path / task_name
        result = migrate_task_directory(
            fixture_root / task_name, generated
        )
        committed = project_root / "workflows" / "legacy" / task_name

        assert result.workflow_path.read_bytes() == (committed / "workflow.yaml").read_bytes()
        assert {
            path.name: digest(path) for path in result.copied_assets
        } == {
            path.name: digest(path) for path in (committed / "assets").iterdir()
        }

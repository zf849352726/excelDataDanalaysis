"""Convert the active filename-driven legacy tasks into V2 YAML workflows."""

from __future__ import annotations

import argparse
import logging
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

import yaml

from automation.engine.errors import LegacyMigrationError


_FILENAME_PATTERN = re.compile(r"^(?P<order>\d+)-(?P<body>.+)\.png$", re.IGNORECASE)
_SAFE_ID_PATTERN = re.compile(r"[^a-zA-Z0-9]+")
logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class LegacyStep:
    order: int
    action: str
    argument: str
    source_path: Path


@dataclass(frozen=True, slots=True)
class MigrationResult:
    source_directory: Path
    workflow_directory: Path
    workflow_path: Path
    copied_assets: tuple[Path, ...]
    step_count: int


def parse_legacy_filename(path: str | Path) -> LegacyStep:
    source_path = Path(path)
    match = _FILENAME_PATTERN.fullmatch(source_path.name)
    if match is None:
        raise LegacyMigrationError(
            f"Legacy step filename must match '<order>-<action>_<argument>.png': "
            f"{source_path.name}"
        )

    body = match.group("body")
    action, separator, argument = body.partition("_")
    if not separator or not argument:
        raise LegacyMigrationError(
            f"Legacy step '{source_path.name}' has no action argument"
        )
    if action not in {"click", "sleep"}:
        raise LegacyMigrationError(
            f"Legacy action '{action}' is unsupported by the Milestone 3 migrator"
        )
    if action == "sleep":
        try:
            seconds = int(argument)
        except ValueError as exc:
            raise LegacyMigrationError(
                f"Legacy sleep duration must be an integer: {source_path.name}"
            ) from exc
        if seconds < 0:
            raise LegacyMigrationError(
                f"Legacy sleep duration must be non-negative: {source_path.name}"
            )

    return LegacyStep(
        order=int(match.group("order")),
        action=action,
        argument=argument,
        source_path=source_path.resolve(),
    )


def migrate_task_directory(
    source_directory: str | Path, workflow_directory: str | Path
) -> MigrationResult:
    source = Path(source_directory).resolve()
    destination = Path(workflow_directory).resolve()
    if not source.is_dir():
        raise LegacyMigrationError(f"Legacy task directory does not exist: {source}")
    if destination.exists():
        raise LegacyMigrationError(
            f"Migration destination already exists; refusing to overwrite: {destination}"
        )

    files = sorted(source.glob("*.png"), key=lambda item: item.name.lower())
    if not files:
        raise LegacyMigrationError(f"Legacy task contains no PNG steps: {source}")
    steps = sorted((parse_legacy_filename(path) for path in files), key=lambda item: item.order)
    orders = [step.order for step in steps]
    if orders != list(range(len(steps))):
        raise LegacyMigrationError(
            f"Legacy step numbers must be contiguous from zero; found {orders}"
        )

    assets_directory = destination / "assets"
    assets_directory.mkdir(parents=True)
    copied_assets: list[Path] = []
    for step in steps:
        copied = assets_directory / step.source_path.name
        shutil.copy2(step.source_path, copied)
        copied_assets.append(copied)

    workflow_data = {
        "name": source.name,
        "version": 1,
        "steps": [_workflow_step(step) for step in steps],
    }
    workflow_path = destination / "workflow.yaml"
    workflow_path.write_text(
        yaml.safe_dump(workflow_data, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return MigrationResult(
        source_directory=source,
        workflow_directory=destination,
        workflow_path=workflow_path,
        copied_assets=tuple(copied_assets),
        step_count=len(steps),
    )


def _workflow_step(step: LegacyStep) -> dict[str, object]:
    slug = _SAFE_ID_PATTERN.sub("_", f"{step.action}_{step.argument}").strip("_").lower()
    result: dict[str, object] = {
        "id": f"step_{step.order:03d}_{slug}",
        "name": f"{step.action}_{step.argument}",
    }
    if step.action == "sleep":
        result.update({"action": "wait", "seconds": float(step.argument)})
        return result

    result.update(
        {
            "action": "click",
            "target": {
                "strategies": [
                    {
                        "type": "image",
                        "template": f"assets/{step.source_path.name}",
                        "threshold": 0.8,
                        "scales": [0.9, 1.0, 1.1],
                        "ambiguity_margin": 0.02,
                    }
                ]
            },
        }
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    arguments = parser.parse_args()
    result = migrate_task_directory(arguments.source, arguments.destination)
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    logger.info(
        f"Migrated {result.step_count} steps to {result.workflow_path} "
        f"with {len(result.copied_assets)} copied assets"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

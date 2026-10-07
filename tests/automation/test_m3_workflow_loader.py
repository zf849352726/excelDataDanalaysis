from pathlib import Path

import pytest

from automation.engine import WorkflowLoader, WorkflowValidationError


def write_workflow(tmp_path: Path, strategy: str, action: str = "click") -> Path:
    path = tmp_path / "workflow.yaml"
    path.write_text(
        f"""
name: image_test
version: 1
steps:
  - id: use_image
    action: {action}
    {'text: hello' if action == 'type_text' else ''}
    target:
      strategies:
        - {strategy}
""",
        encoding="utf-8",
    )
    return path


def test_loads_strict_image_strategy(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """type: image
          template: assets/button.png
          threshold: 0.86
          scales: [0.9, 1.0, 1.1]
          ambiguity_margin: 0.03""",
    )

    workflow = WorkflowLoader().load(path)
    strategy = workflow.steps[0].target["strategies"][0]

    assert strategy["type"] == "image"
    assert strategy["threshold"] == 0.86
    assert strategy["scales"] == (0.9, 1.0, 1.1)


@pytest.mark.parametrize(
    "field,value",
    [
        ("threshold", "1.1"),
        ("scales", "[]"),
        ("ambiguity_margin", "-0.1"),
    ],
)
def test_rejects_invalid_image_matching_values(
    tmp_path: Path, field: str, value: str
) -> None:
    path = write_workflow(
        tmp_path,
        f"""type: image
          template: assets/button.png
          {field}: {value}""",
    )

    with pytest.raises(WorkflowValidationError, match=field):
        WorkflowLoader().load(path)


def test_rejects_parent_relative_template(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """type: image
          template: ../button.png""",
    )

    with pytest.raises(WorkflowValidationError, match="workflow-relative"):
        WorkflowLoader().load(path)


def test_type_text_cannot_use_image_target(tmp_path: Path) -> None:
    path = write_workflow(
        tmp_path,
        """type: image
          template: assets/editor.png""",
        action="type_text",
    )

    with pytest.raises(WorkflowValidationError, match="only UIA"):
        WorkflowLoader().load(path)

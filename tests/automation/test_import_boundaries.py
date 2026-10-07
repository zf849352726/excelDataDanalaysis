from __future__ import annotations

import ast
from pathlib import Path


LEGACY_MODULES = {"main", "config", "final_cal", "price", "ui"}


def test_automation_package_has_no_legacy_imports() -> None:
    package_root = Path(__file__).resolve().parents[2] / "automation"
    violations = []
    for path in package_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports = [node.module]
            else:
                continue
            for module in imports:
                if module.split(".", 1)[0] in LEGACY_MODULES:
                    violations.append((path.relative_to(package_root), module))

    assert violations == []

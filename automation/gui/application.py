"""Standalone Automation Hub main window and application entry point."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from PyQt5 import QtWidgets

from automation.gui.qt import AutomationPanel


def default_workflows_root() -> Path:
    """Return the workflow catalog shipped beside the source package."""

    return Path(__file__).resolve().parents[2] / "workflows"


class AutomationMainWindow(QtWidgets.QMainWindow):
    """Top-level window for the standalone Automation Hub product."""

    def __init__(
        self,
        workflows_root: str | Path | None = None,
        parent: QtWidgets.QWidget | None = None,
    ) -> None:
        super().__init__(parent)
        self.setObjectName("automationHubMainWindow")
        self.setWindowTitle("Automation Hub V2")
        self.resize(960, 640)
        self.automation_panel = AutomationPanel(
            workflows_root or default_workflows_root(), self
        )
        self.setCentralWidget(self.automation_panel)

    def closeEvent(self, event: object) -> None:
        if self.automation_panel.shutdown():
            event.accept()
        else:
            event.ignore()


def main(argv: Sequence[str] | None = None) -> int:
    """Start the standalone PyQt5 application and return its exit code."""

    app = QtWidgets.QApplication.instance()
    if app is None:
        app = QtWidgets.QApplication(list(argv) if argv is not None else [])
    app.setApplicationName("Automation Hub V2")
    window = AutomationMainWindow()
    window.show()
    exit_code = app.exec_()
    if window.isVisible():
        window.close()
    return exit_code

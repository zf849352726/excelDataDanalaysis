from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5 import QtCore, QtWidgets

from automation.engine import ExecutionStatus, WorkflowResult
from automation.gui import AutomationMainWindow, AutomationPanel
from automation.gui.application import main


def write_wait_workflow(directory: Path, seconds: float) -> None:
    directory.mkdir(parents=True)
    (directory / "workflow.yaml").write_text(
        "name: responsive_gui\nversion: 1\nsteps:\n  - id: long_wait\n"
        f"    action: wait\n    seconds: {seconds}\n",
        encoding="utf-8",
    )


def get_application() -> QtWidgets.QApplication:
    return QtWidgets.QApplication.instance() or QtWidgets.QApplication([])


def test_panel_keeps_event_loop_responsive_and_stops_active_run(tmp_path) -> None:
    app = get_application()
    write_wait_workflow(tmp_path / "sample", 5)
    panel = AutomationPanel(tmp_path)
    loop = QtCore.QEventLoop()
    ticks = []
    results = []
    heartbeat = QtCore.QTimer()
    heartbeat.setInterval(10)
    heartbeat.timeout.connect(lambda: ticks.append(1))
    panel.workflow_finished.connect(results.append)
    panel.workflow_finished.connect(loop.quit)
    timeout = QtCore.QTimer()
    timeout.setSingleShot(True)
    timeout.timeout.connect(loop.quit)

    try:
        panel.run_button.click()
        heartbeat.start()
        QtCore.QTimer.singleShot(100, panel.stop_button.click)
        timeout.start(2000)
        loop.exec_()

        assert len(ticks) >= 5
        assert len(results) == 1
        assert isinstance(results[0], WorkflowResult)
        assert results[0].status is ExecutionStatus.CANCELLED
        assert "已请求停止" in panel.log_output.toPlainText()
        assert panel.stop_button.isEnabled() is False
        assert panel.run_button.isEnabled() is True
    finally:
        heartbeat.stop()
        assert panel.shutdown()
        panel.deleteLater()
        app.processEvents()


def test_standalone_window_lists_and_runs_basic_workflow(tmp_path) -> None:
    app = get_application()
    write_wait_workflow(tmp_path / "basic_test", 0)
    window = AutomationMainWindow(tmp_path)
    loop = QtCore.QEventLoop()
    results = []
    window.automation_panel.workflow_finished.connect(results.append)
    window.automation_panel.workflow_finished.connect(loop.quit)
    timeout = QtCore.QTimer()
    timeout.setSingleShot(True)
    timeout.timeout.connect(loop.quit)

    try:
        assert window.automation_panel.workflow_list.count() == 1
        window.automation_panel.run_button.click()
        timeout.start(2000)
        loop.exec_()

        assert len(results) == 1
        assert isinstance(results[0], WorkflowResult)
        assert results[0].status is ExecutionStatus.EXECUTED_UNVERIFIED
    finally:
        assert window.automation_panel.shutdown()
        window.deleteLater()
        app.processEvents()


def test_standalone_application_entry_point_starts_and_exits() -> None:
    app = get_application()
    QtCore.QTimer.singleShot(0, app.quit)

    assert main([]) == 0

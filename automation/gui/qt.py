"""PyQt5 worker and panel for single-run Automation Hub execution."""

from __future__ import annotations

from pathlib import Path

from PyQt5 import QtCore, QtWidgets

from automation.engine import (
    ActionResult,
    ExecutionEvent,
    ExecutionEventType,
    WorkflowResult,
)
from automation.services import AutomationService, WorkflowSummary


class AutomationWorker(QtCore.QObject):
    """Run blocking automation on its assigned QThread."""

    workflow_started = QtCore.pyqtSignal(str)
    step_started = QtCore.pyqtSignal(str, str, int, int)
    step_completed = QtCore.pyqtSignal(str, str, str, int, int)
    workflow_completed = QtCore.pyqtSignal(object)
    workflow_failed = QtCore.pyqtSignal(str)
    log = QtCore.pyqtSignal(str)
    busy_changed = QtCore.pyqtSignal(bool)

    def __init__(self, service: AutomationService) -> None:
        super().__init__()
        self._service = service

    @QtCore.pyqtSlot(str)
    def run_workflow(self, workflow_path: str) -> None:
        self.busy_changed.emit(True)
        try:
            result = self._service.run_workflow(workflow_path, self._handle_event)
        except Exception as exc:
            self.log.emit(f"启动失败: {type(exc).__name__}: {exc}")
            self.workflow_failed.emit(str(exc))
        else:
            self.workflow_completed.emit(result)
        finally:
            self.busy_changed.emit(False)

    def _handle_event(self, event: ExecutionEvent) -> None:
        if event.type is ExecutionEventType.WORKFLOW_STARTED:
            self.workflow_started.emit(event.workflow_name)
            self.log.emit(f"工作流开始: {event.workflow_name}")
        elif event.type is ExecutionEventType.STEP_STARTED:
            self.step_started.emit(
                event.step_id or "",
                event.action or "",
                event.step_index or 0,
                event.step_count or 0,
            )
            self.log.emit(
                f"步骤 {event.step_index}/{event.step_count} 开始: "
                f"{event.step_id} [{event.action}]"
            )
        elif event.type is ExecutionEventType.STEP_COMPLETED:
            result = event.result
            if not isinstance(result, ActionResult):
                return
            self.step_completed.emit(
                event.step_id or "",
                result.status.value,
                result.message,
                event.step_index or 0,
                event.step_count or 0,
            )
            message = f": {result.message}" if result.message else ""
            self.log.emit(
                f"步骤 {event.step_id} 完成: {result.status.value}{message}"
            )


class AutomationPanel(QtWidgets.QWidget):
    """Main-thread-only widgets backed by a persistent automation worker."""

    run_requested = QtCore.pyqtSignal(str)
    workflow_finished = QtCore.pyqtSignal(object)

    def __init__(
        self,
        workflows_root: str | Path,
        parent: QtWidgets.QWidget | None = None,
        *,
        service: AutomationService | None = None,
    ) -> None:
        super().__init__(parent)
        self._service = service or AutomationService(workflows_root)
        self._summaries: dict[str, WorkflowSummary] = {}
        self._build_ui()

        self._thread = QtCore.QThread(self)
        self._thread.setObjectName("automationV2WorkerThread")
        self._worker = AutomationWorker(self._service)
        self._worker.moveToThread(self._thread)
        self.run_requested.connect(self._worker.run_workflow)
        self._worker.workflow_started.connect(self._on_workflow_started)
        self._worker.step_started.connect(self._on_step_started)
        self._worker.step_completed.connect(self._on_step_completed)
        self._worker.workflow_completed.connect(self._on_workflow_completed)
        self._worker.workflow_failed.connect(self._on_workflow_failed)
        self._worker.log.connect(self._append_log)
        self._worker.busy_changed.connect(self._set_busy)
        self._thread.finished.connect(self._worker.deleteLater)
        self._thread.start()
        self.refresh_workflows()

    def _build_ui(self) -> None:
        layout = QtWidgets.QVBoxLayout(self)
        toolbar = QtWidgets.QHBoxLayout()
        self.refresh_button = QtWidgets.QPushButton("刷新工作流", self)
        self.refresh_button.setObjectName("automationV2RefreshButton")
        self.run_button = QtWidgets.QPushButton("运行一次", self)
        self.run_button.setObjectName("automationV2RunButton")
        self.stop_button = QtWidgets.QPushButton("停止", self)
        self.stop_button.setObjectName("automationV2StopButton")
        self.stop_button.setEnabled(False)
        self.status_label = QtWidgets.QLabel("就绪", self)
        self.status_label.setObjectName("automationV2StatusLabel")
        toolbar.addWidget(self.refresh_button)
        toolbar.addWidget(self.run_button)
        toolbar.addWidget(self.stop_button)
        toolbar.addWidget(self.status_label, 1)
        layout.addLayout(toolbar)

        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal, self)
        self.workflow_list = QtWidgets.QListWidget(splitter)
        self.workflow_list.setObjectName("automationV2WorkflowList")
        self.step_list = QtWidgets.QListWidget(splitter)
        self.step_list.setObjectName("automationV2StepList")
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        layout.addWidget(splitter, 2)

        self.progress = QtWidgets.QProgressBar(self)
        self.progress.setObjectName("automationV2Progress")
        self.progress.setRange(0, 1)
        self.progress.setValue(0)
        layout.addWidget(self.progress)
        self.log_output = QtWidgets.QPlainTextEdit(self)
        self.log_output.setObjectName("automationV2Log")
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output, 1)

        self.refresh_button.clicked.connect(self.refresh_workflows)
        self.run_button.clicked.connect(self.run_selected)
        self.stop_button.clicked.connect(self.stop_active)
        self.workflow_list.currentItemChanged.connect(self._show_selected_steps)

    @QtCore.pyqtSlot()
    def refresh_workflows(self) -> None:
        selected_id = self._selected_workflow_id()
        try:
            summaries = self._service.list_workflows()
        except Exception as exc:
            self._append_log(f"刷新失败: {type(exc).__name__}: {exc}")
            self.status_label.setText("工作流加载失败")
            return

        self._summaries = {item.workflow_id: item for item in summaries}
        self.workflow_list.clear()
        selected_row = 0
        for row, summary in enumerate(summaries):
            item = QtWidgets.QListWidgetItem(
                f"{summary.name}  ({summary.workflow_id})"
            )
            item.setData(QtCore.Qt.UserRole, summary.workflow_id)
            self.workflow_list.addItem(item)
            if summary.workflow_id == selected_id:
                selected_row = row
        if summaries:
            self.workflow_list.setCurrentRow(selected_row)
            self.status_label.setText(f"已加载 {len(summaries)} 个工作流")
        else:
            self.step_list.clear()
            self.status_label.setText("没有可用工作流")
        self.run_button.setEnabled(bool(summaries) and not self._service.is_running)

    @QtCore.pyqtSlot()
    def run_selected(self) -> None:
        workflow_id = self._selected_workflow_id()
        summary = self._summaries.get(workflow_id or "")
        if summary is None or self._service.is_running:
            return
        self.log_output.clear()
        self.progress.setRange(0, len(summary.steps))
        self.progress.setValue(0)
        self._set_busy(True)
        self.run_requested.emit(str(summary.path))

    @QtCore.pyqtSlot()
    def stop_active(self) -> None:
        if self._service.stop_active():
            self.status_label.setText("正在停止…")
            self._append_log("已请求停止当前工作流")

    def _show_selected_steps(self, current: object, _previous: object) -> None:
        self.step_list.clear()
        if not isinstance(current, QtWidgets.QListWidgetItem):
            return
        workflow_id = current.data(QtCore.Qt.UserRole)
        summary = self._summaries.get(workflow_id)
        if summary is None:
            return
        for index, (step_id, action, name) in enumerate(summary.steps, start=1):
            label = name or step_id
            self.step_list.addItem(f"{index}. {label}  [{action}]")

    @QtCore.pyqtSlot(str)
    def _on_workflow_started(self, name: str) -> None:
        self.status_label.setText(f"运行中: {name}")

    @QtCore.pyqtSlot(str, str, int, int)
    def _on_step_started(
        self, step_id: str, _action: str, index: int, count: int
    ) -> None:
        self.status_label.setText(f"步骤 {index}/{count}: {step_id}")
        if 0 < index <= self.step_list.count():
            self.step_list.setCurrentRow(index - 1)

    @QtCore.pyqtSlot(str, str, str, int, int)
    def _on_step_completed(
        self, _step_id: str, _status: str, _message: str, index: int, count: int
    ) -> None:
        self.progress.setRange(0, max(1, count))
        self.progress.setValue(index)

    @QtCore.pyqtSlot(object)
    def _on_workflow_completed(self, result: object) -> None:
        if isinstance(result, WorkflowResult):
            self.status_label.setText(f"完成: {result.status.value}")
            self._append_log(f"工作流完成: {result.status.value}")
        self.workflow_finished.emit(result)

    @QtCore.pyqtSlot(str)
    def _on_workflow_failed(self, message: str) -> None:
        self.status_label.setText(f"启动失败: {message}")
        self.workflow_finished.emit(None)

    @QtCore.pyqtSlot(str)
    def _append_log(self, message: str) -> None:
        self.log_output.appendPlainText(message)

    @QtCore.pyqtSlot(bool)
    def _set_busy(self, busy: bool) -> None:
        self.workflow_list.setEnabled(not busy)
        self.refresh_button.setEnabled(not busy)
        self.run_button.setEnabled(not busy and bool(self._summaries))
        self.stop_button.setEnabled(busy)

    def shutdown(self, timeout_ms: int = 5000) -> bool:
        if not self._thread.isRunning():
            return True
        self._service.stop_active()
        self._thread.quit()
        return self._thread.wait(timeout_ms)

    def _selected_workflow_id(self) -> str | None:
        item = self.workflow_list.currentItem()
        return item.data(QtCore.Qt.UserRole) if item is not None else None

    def closeEvent(self, event: object) -> None:
        if self.shutdown():
            event.accept()
        else:
            event.ignore()

from types import SimpleNamespace

from automation.engine import ExecutionContext, ProcessReference
from automation.locators.uia import UIALocator


class FakeRectangle:
    left = 10
    top = 20
    right = 110
    bottom = 70


class FakeElement:
    def __init__(
        self,
        *,
        handle: int,
        pid: int,
        name: str,
        control_type: str,
        automation_id: str = "",
        class_name: str = "",
        children=(),
    ) -> None:
        self.handle = handle
        self._pid = pid
        self._name = name
        self._children = list(children)
        self.element_info = SimpleNamespace(
            control_type=control_type,
            automation_id=automation_id,
            class_name=class_name,
        )

    def window_text(self) -> str:
        return self._name

    def process_id(self) -> int:
        return self._pid

    def descendants(self):
        return list(self._children)

    def rectangle(self):
        return FakeRectangle()


class FakeDesktop:
    def __init__(self, windows) -> None:
        self.current_windows = list(windows)

    def windows(self, process=None):
        if process is None:
            return list(self.current_windows)
        return [window for window in self.current_windows if window.process_id() == process]


def selector():
    return {
        "type": "uia",
        "process": "notepad",
        "allow_process_handoff": True,
        "window": {
            "title_contains": "automation_hub_m2.txt",
            "class_name": "Notepad",
        },
        "control": {
            "control_type": "Document",
            "class_name": "RichEditD2DPT",
        },
    }


def test_uia_locator_safely_binds_changed_baseline_window(monkeypatch) -> None:
    old_root = FakeElement(
        handle=10,
        pid=500,
        name="Existing document - Notepad",
        control_type="Window",
        class_name="Notepad",
    )
    desktop = FakeDesktop([old_root])
    monkeypatch.setattr("automation.locators.uia.Desktop", lambda backend: desktop)
    context = ExecutionContext()
    context.processes["notepad"] = ProcessReference("notepad", 100, "notepad.exe")
    locator = UIALocator()
    locator.begin(context)

    document = FakeElement(
        handle=0,
        pid=500,
        name="",
        control_type="Document",
        class_name="RichEditD2DPT",
    )
    desktop.current_windows = [
        FakeElement(
            handle=10,
            pid=500,
            name="automation_hub_m2.txt - Notepad",
            control_type="Window",
            class_name="Notepad",
            children=[document],
        )
    ]

    result = locator.locate(selector(), context)

    assert result.found
    assert result.element is document
    assert context.processes["notepad"].bound_pid == 500
    assert result.bounds == (10, 20, 110, 70)


def test_uia_locator_reports_ambiguity(monkeypatch) -> None:
    first = FakeElement(
        handle=0,
        pid=500,
        name="",
        control_type="Document",
        class_name="RichEditD2DPT",
    )
    second = FakeElement(
        handle=0,
        pid=500,
        name="",
        control_type="Document",
        class_name="RichEditD2DPT",
    )
    root = FakeElement(
        handle=20,
        pid=500,
        name="automation_hub_m2.txt - Notepad",
        control_type="Window",
        class_name="Notepad",
        children=[first, second],
    )
    desktop = FakeDesktop([])
    monkeypatch.setattr("automation.locators.uia.Desktop", lambda backend: desktop)
    context = ExecutionContext()
    context.processes["notepad"] = ProcessReference("notepad", 100, "notepad.exe")
    locator = UIALocator()
    locator.begin(context)
    desktop.current_windows = [root]

    result = locator.locate(selector(), context)

    assert not result.found
    assert result.ambiguous
    assert result.metadata["candidate_count"] == 2

import importlib


def test_legacy_main_imports() -> None:
    """The current legacy application should remain importable on the V2 Python baseline."""
    module = importlib.import_module("main")
    assert module is not None

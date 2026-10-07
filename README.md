# excel_data / Automation Hub V2

This repository contains an existing PyQt-based Excel/WPS/data-processing desktop application and a legacy desktop automation subsystem.

Automation Hub V2 is being introduced incrementally without replacing the existing application in one rewrite.

## Project documents

- `AGENTS.md` — repository rules and architectural constraints for coding agents.
- `plan.md` — Automation Hub V2 roadmap, milestones, deliverables, and acceptance criteria.

## Python baseline

Automation Hub V2 targets:

```text
Python 3.11
```

A dedicated development environment on the current machine is:

```text
D:\Anaconda\envs\automation_hub
```

Recreate it with:

```powershell
conda create -n automation_hub python=3.11 pip -y
conda activate automation_hub
python -m pip install -e ".[dev]"
```

If the configured PyPI mirror does not provide a required wheel, use the official index explicitly:

```powershell
python -m pip install -i https://pypi.org/simple -e ".[dev]"
```

The legacy application may contain code created under older Python environments; compatibility should be verified incrementally rather than rewritten pre-emptively.

## Existing application

Legacy application entry point:

```powershell
python main.py
```

A Python 3.11 import smoke check is:

```powershell
python -c "import main; print('import main: OK')"
```

## Tests

Automation V2 tests belong under:

```text
tests/automation/
```

Run tests with:

```powershell
python -m pytest
```

## Development status

The current active milestone is defined in `plan.md`.

Do not skip milestones automatically. Complete, validate, report, and stop for review before proceeding to the next milestone.

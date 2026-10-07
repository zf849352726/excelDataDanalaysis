# Automation Hub V2

This branch contains the standalone Automation Hub V2 desktop application.

The complete legacy business application with the M5 Automation V2 tab is preserved on the `legacy-integrated` branch.

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

## Start the application

```powershell
python -m automation
```

The application discovers workflows from the repository's `workflows` directory. Workflow execution remains available through the GUI without importing the historical business application.

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

# AGENTS.md

> Repository: `D:\python_learn\excel_data`
>
> This file answers: **How must coding agents work in this repository?**
>
> Project roadmap, milestone scope, sequencing, and acceptance criteria live in `plan.md`. Read `plan.md` before implementing substantial Automation Hub work.

---

# 1. Rule Precedence

When working in this repository:

1. follow the user's current explicit request
2. follow this `AGENTS.md`
3. follow the active milestone and scope in `plan.md`
4. preserve existing project behavior unless the task explicitly changes it

If `plan.md` proposes work outside the user's requested scope, do not implement it automatically.

---

# 2. Protect the Existing Application

The repository contains working legacy business logic and automation.

Do not casually delete, rename, or rewrite:

```text
main.py
config.py
price\
price\static\
final_cal\
ui\
```

Existing images and task folders are user assets.

Treat legacy automation as migration input.

Prefer additive V2 development under:

```text
automation\
workflows\
tests\automation\
runs\
```

The legacy typo:

```text
price\moudle
```

may be depended on by imports. Do not rename it unless migration is explicit and verified.

---

# 3. Keep V2 Independent from the GUI

The Automation V2 core must work without launching PyQt.

These layers must remain GUI-independent:

```text
automation\engine
automation\actions
automation\locators
automation\verification
automation\legacy
```

Correct dependency direction:

```text
PyQt GUI
   ↓
AutomationService
   ↓
WorkflowExecutor
```

Incorrect dependency direction:

```text
WorkflowExecutor
   ↓
MainWindow / Qt widgets
```

Do not put workflow execution logic back into `main.py`.

Use `main.py` only for thin integration hooks when necessary.

---

# 4. Preserve the Core Responsibility Boundaries

Automation V2 must keep these concepts separate:

```text
Workflow
   │
Executor
   │
   ├── Action
   ├── Locator
   └── Verifier
```

## Workflow

Describes intent and configuration.

## Executor

Controls step order, retries, cancellation, failure policy, and run state.

## Locator

Finds a target.

It must not click.

## Action

Performs one operation.

It must not own workflow iteration or verification policy.

## Verifier

Determines whether the expected outcome occurred.

It must not execute the action itself.

Do not recreate a single all-purpose `Automator` god object.

---

# 5. Automation Preference Order

When several implementation methods are possible, prefer:

```text
Native API / application API / MCP
        ↓
UI Automation (UIA)
        ↓
Image matching
        ↓
OCR
        ↓
AI Vision
        ↓
Explicit coordinate
```

Examples:

- Excel/WPS data operations should use COM/API/macro interfaces when reliable
- native Windows controls should prefer UIA
- image matching should be a fallback, not the default for every control
- coordinate clicks must be explicitly declared

Do not screen-click something that has a reliable programmatic interface.

---

# 6. Never Blind Click

This is a hard safety invariant.

If target resolution fails:

```text
STOP
```

Do not silently use:

- previous coordinates
- stale coordinates
- guessed coordinates
- old match positions
- a first arbitrary similar image result

Coordinate actions are allowed only when the workflow explicitly asks for coordinates.

Uncertainty must remain visible to the caller.

---

# 7. Action Execution Is Not Success

Never equate:

```text
action executed
```

with:

```text
desired outcome achieved
```

Where a workflow defines an expectation, execution should conceptually follow:

```text
Locate
→ Act
→ Verify
→ Retry if configured
→ Continue only on success
```

Do not swallow verification failures.

---

# 8. Action Registry Rules

V2 must use explicit action types.

Do not copy legacy substring dispatch such as:

```python
if "click" in task_name:
    ...

if "sleep" in task_name:
    ...
```

Use a registry or equivalent explicit mapping.

Actions should have narrow responsibilities and clear input/output contracts.

---

# 9. Locator Rules

Locators should expose a common result shape where practical.

A locator result may include:

```text
found
strategy
x
y
bounds
confidence
element
ambiguous
metadata
```

Do not force every locator to populate irrelevant fields.

A locator chain should honor the workflow's declared strategy order.

If every strategy fails, return/raise a meaningful resolution failure.

---

# 10. UIA Rules

For native Windows UI, prefer semantic UI Automation.

When using pywinauto, `backend="uia"` is the default direction unless a target application proves otherwise.

Useful selector fields may include:

```text
process
window title
control_type
name
automation_id
class_name
```

When a UIA element supports reliable semantic actions such as Invoke or SetValue, prefer those over converting the element into raw screen coordinates.

Do not overfit automation to window position when stable UI metadata exists.

---

# 11. Image Matching Rules

Do not repeat the legacy behavior of taking the first result above a threshold.

For template matching:

- choose the best candidate
- report actual confidence
- support configurable threshold
- support DPI/scale variation where needed
- detect ambiguity when practical

For OpenCV template matching, `cv2.minMaxLoc` is preferred over selecting the first `np.where` result.

If two candidate matches are too similar to distinguish safely, return ambiguity rather than clicking arbitrarily.

Thresholds and ambiguity margins should be configurable rather than scattered constants.

---

# 12. Retry, Timeout, and Cancellation

Retries must be bounded.

A retry should represent the logical step attempt where appropriate:

```text
Locate
→ Action
→ Verify
```

Do not implement infinite retry by default.

All long-running waits, locator loops, verification loops, and retry loops must support cooperative cancellation.

Do not use a single long blocking:

```python
time.sleep(30)
```

when the operation is expected to be cancellable.

Prefer small wait intervals with cancellation checks.

---

# 13. Pause / Resume / Stop

Pause and stop are execution-control concerns.

Do not implement pause by blocking the Qt UI thread.

A stop request should be capable of interrupting an active cancellable workflow, not merely prevent the next timer cycle.

---

# 14. PyQt Threading Rules

Desktop automation must not block the GUI event loop.

When GUI integration is introduced, use a worker model such as:

```text
PyQt Main Thread
      │
AutomationService
      │
Worker Thread
      │
WorkflowExecutor
```

Potential signals/events:

```text
workflow_started
step_started
step_completed
step_failed
workflow_completed
workflow_failed
progress
log
```

OpenCV matching, waits, and workflow execution do not belong in the main UI thread.

---

# 15. Workflow and Asset Paths

Do not scatter new hard-coded absolute paths throughout V2.

Prefer:

- project-relative paths
- workflow-relative asset paths
- explicit configuration
- environment variables only when appropriate

For example:

```text
assets/export.png
```

should resolve relative to the owning workflow directory.

Existing hard-coded legacy paths do not justify adding new ones.

---

# 16. Legacy Compatibility Rules

Do not modify or delete original assets during migration.

Legacy migration should:

- parse legacy filename semantics
- generate V2 workflow data
- copy assets into the new workflow directory
- preserve source task folders

Known legacy defects must not be copied into V2:

- `MouseControl.click(position)` mismatch
- incorrect list use with `pyautogui.hotkey`
- substring-based action dispatch
- first-image-match selection
- timer-only stopping behavior

---

# 17. Recorder Scope

Do not build a heavyweight full-session recorder unless explicitly requested.

The preferred authoring aid is a Target Picker / Step Capture:

```text
user chooses capture target
→ user clicks UI element
→ inspect UIA metadata
→ crop local screenshot
→ generate locator strategies
```

Avoid prematurely introducing:

- continuous video recording
- mouse-trajectory databases
- raw keyboard capture databases
- record→compile pipelines

Roadmap timing for Target Picker is defined in `plan.md`.

---

# 18. Excel / WPS Rules

Application-specific automation must be isolated behind adapters/actions.

Do not add Excel/WPS-specific branches to the generic executor.

Prefer:

```text
COM / native API / macro interface
        ↓
UIA
        ↓
image automation
```

Use GUI automation only where a reliable application API is unavailable.

---

# 19. MCP / AI Rules

The core must remain usable without MCP or an LLM.

When MCP is introduced later, expose semantic workflow capabilities rather than raw mouse primitives.

Preferred:

```text
run_workflow("export_report")
```

Not preferred:

```text
click(522, 311)
```

Do not add AI Vision merely because it is available. Deterministic interfaces take priority.

---

# 20. Logging and Diagnostics

New V2 code should use structured logging rather than scattered `print()` calls.

A failed step should expose enough information to diagnose:

- workflow
- step ID
- action
- locator strategy attempted
- confidence where relevant
- retry/attempt count
- error
- screenshot path where available

Do not report a workflow as successful when a required verification failed.

---

# 21. Error Handling

Avoid:

```python
except Exception:
    pass
```

and avoid broad exceptions that only print and continue.

Catch errors at the layer that can meaningfully handle them.

Prefer explicit domain errors for cases such as:

```text
TargetNotFound
AmbiguousTarget
VerificationFailed
WorkflowCancelled
ActionFailed
```

Do not hide failures from the executor.

---

# 22. Code Quality

Use:

- clear type annotations
- focused modules
- small classes/functions
- explicit return/result models
- meaningful names
- `pathlib` where practical
- composition over deep inheritance
- docstrings for non-obvious behavior

Avoid:

- giant classes
- new god objects
- hidden mutable globals
- circular imports
- speculative abstraction
- style-only rewrites of unrelated code

Prefer a working vertical slice over a broad unfinished framework.

---

# 23. Dependency Discipline

Before adding a dependency:

1. check whether the project already has a suitable dependency
2. justify why the new package is necessary
3. isolate it behind an adapter where appropriate
4. avoid making optional capabilities mandatory

Do not add packages simply because they are mentioned in planning documents.

---

# 24. Tests

New deterministic automation logic should have tests under:

```text
tests\automation\
```

Unit-test:

- parsing
- workflow loading
- registries
- retry behavior
- cancellation
- result models
- migration logic

OS/UI integration tests should be clearly marked and skippable where the required application/environment is unavailable.

Do not rely only on manual testing.

---

# 25. Validation Before Claiming Completion

Before saying work is complete:

1. run the relevant tests
2. run import/static checks appropriate to touched code
3. run at least one meaningful integration workflow when the environment permits
4. inspect generated artifacts/logs
5. inspect `git diff`
6. inspect `git status`
7. report limitations honestly

If a test cannot be run, say so.

Do not invent success.

---

# 26. Git Safety Rules

Before editing substantial code:

- inspect `git status`
- inspect the current branch
- inspect recent history

Do not discard unrelated working-tree changes.

Do not run destructive commands such as:

```text
git reset --hard
git clean -fd
```

without explicit user authorization.

Do not:

- force-push
- amend unrelated commits
- push without request
- delete branches/tags casually

When asked to commit, prefer small coherent commits.

Roadmap-specific commit boundaries belong in `plan.md` or the current task, not here.

---

# 27. Working Style for Coding Agents

For substantial work:

1. inspect the relevant existing code first
2. read the current active milestone in `plan.md`
3. identify the smallest coherent slice
4. implement only that slice
5. test it
6. inspect the result
7. report concrete evidence

Do not ask the user to repeat information already available in the repository.

Do not rewrite unrelated modules for style.

Do not automatically continue into later milestones.

---

# 28. Milestone Gating

`plan.md` owns milestone scope.

If the active task or `plan.md` says to implement one milestone:

```text
implement that milestone
→ validate
→ report
→ stop
```

Wait for confirmation before entering the next milestone.

This is a repository-wide working rule.

---

# 29. Reporting

For substantial implementation work, report:

- what changed
- key files modified/added
- tests and results
- integration/manual validation
- known limitations
- recommended next step

Keep reports evidence-based and concise.

---

# 30. Safety Around Destructive Automation

Desktop automation can cause real side effects.

Actions involving:

- file deletion
- overwrite
- form submission
- sending messages
- purchases
- system configuration
- closing unsaved applications

must be explicit in the workflow/task.

Do not introduce destructive behavior into test workflows without clear user intent.

---

# 31. Definition of Good Automation

For this repository, robust automation is:

- understandable by a human
- not unnecessarily tied to absolute coordinates
- semantic/API-driven where possible
- explicit about locator strategy
- verifiable after important actions
- bounded in retries
- cancellable
- diagnosable on failure
- conservative under uncertainty
- executable without the PyQt editor being open

Use this definition when making implementation tradeoffs.

---

# 32. Document Ownership

Keep documentation responsibilities separate:

| Document | Purpose |
|---|---|
| `plan.md` | what to build, milestone order, deliverables, acceptance criteria, active milestone |
| `AGENTS.md` | how agents must work, architectural invariants, safety, testing, Git, repository discipline |

Do not copy milestone descriptions into this file.

Do not put detailed coding-agent behavioral rules into `plan.md`.

When one document needs the other, link to it instead of duplicating it.

---

# 33. Final Rule

Prefer:

```text
observable
testable
cancellable
verifiable
maintainable
```

over:

```text
quick but fragile
```

But do not over-engineer.

The goal is a practical local automation system that is easier to use, safer to run, and easier to extend than the legacy implementation.

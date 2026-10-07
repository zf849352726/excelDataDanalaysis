# Automation Hub V2 — Development Plan

> Repository: `D:\python_learn\excel_data`
>
> This file answers: **What are we building, in what order, and how do we know each phase is complete?**
>
> Long-lived coding rules and architectural constraints belong in `AGENTS.md`. Do not duplicate them here.

---

# 1. Project Goal

Upgrade the existing desktop automation subsystem into a local, developer-oriented **Automation Hub V2**.

Current legacy automation lives mainly under:

```text
price\moudle\
price\static\
```

The long-term product direction is:

```text
PyQt GUI / Codex / DSH
          │
          ↓
AutomationService
          │
          ↓
Workflow Engine
          │
    ┌─────┼─────┐
    ↓     ↓     ↓
 Action Locator Verifier
          │
    UIA / Image / OCR / Vision
          │
          ↓
       Windows
```

The V2 system should gradually replace filename-driven execution while preserving legacy workflows and existing business features.

---

# 2. Product Direction

The system should evolve toward these capabilities:

1. Human-readable YAML workflows
2. Reusable workflow execution engine
3. UIA-first Windows automation
4. Image fallback for UI elements UIA cannot reliably reach
5. Explicit post-action verification
6. Retry, timeout, cancellation, pause/resume
7. Legacy workflow migration
8. Existing PyQt GUI integration
9. Target Picker / Step Capture
10. Excel/WPS native adapters
11. MCP exposure for Codex / DSH / ChatGPT
12. OCR / AI Vision only after deterministic layers are stable

The intended automation preference is:

```text
Native API / MCP
      ↓
UIA
      ↓
Image
      ↓
OCR
      ↓
AI Vision
      ↓
Explicit Coordinate
```

Detailed enforcement rules are defined in `AGENTS.md`.

---

# 3. Legacy Baseline

Before V2 changes, preserve the current legacy automation model:

```text
Task folder
→ numbered step files
→ Automator
→ ImageRecognition
→ MouseControl / KeyboardControl
```

Example:

```text
price\static\auto_click\
    0-click_xlsxfile.png
    1-click_xlsxfile1.png
    2-sleep_10.png
```

Known legacy issues already identified:

- coordinate-click path has a parameter mismatch
- `pyautogui.hotkey()` is called incorrectly for a list
- action parsing relies on substring matching
- image matching selects the first match above threshold rather than the best candidate
- task stopping only stops future timer cycles, not necessarily the current action
- automation logic is mixed into the PyQt application

These are migration inputs and technical debt, not reasons to rewrite the entire application.

---

# 4. Target V2 Shape

The expected direction is:

```text
automation/
├── engine/
├── actions/
├── locators/
├── verification/
├── adapters/
├── legacy/
├── services/
└── recorder/

workflows/
runs/
tests/automation/
```

This is a direction, not a requirement to create empty files prematurely.

The actual module boundaries should emerge milestone by milestone.

---

# 5. Milestone 0 — Baseline and Safety Point

## Goal

Establish a safe starting point before structural changes.

## Deliverables

- inspect current Git status and history
- preserve existing working tree changes
- confirm current application/import baseline
- create a legacy safety reference if appropriate
- document the current automation entry points

## Acceptance

- legacy project is still intact
- no unrelated files are rewritten
- V2 work can begin without losing legacy behavior

---

# 6. Milestone 1 — Core Workflow Engine

## Goal

Create a GUI-independent workflow runtime.

## Deliverables

Implement:

- `Workflow`
- `Step`
- YAML workflow loader
- `ExecutionContext`
- `ActionResult`
- `WorkflowExecutor`
- Action Registry
- `CancellationToken`

Initial actions:

- `wait`
- `launch`
- `type_text`
- `hotkey`
- `click_xy`
- `close_window`

Create:

```text
workflows/basic_test/workflow.yaml
```

## Acceptance

- workflow loads from YAML
- workflow can run without starting PyQt
- actions execute in declared order
- interruptible wait can be cancelled
- errors produce explicit step failures
- unit tests pass
- at least one simple workflow is run end-to-end

## Out of Scope

Do not add UIA, image matching, GUI refactoring, MCP, OCR, or AI Vision in this milestone.

---

# 7. Milestone 2 — UIA Locator

## Goal

Prove semantic Windows automation without image templates.

## Deliverables

Add:

- common `LocatorResult`
- locator interface
- UIA locator
- locator-chain foundation
- UIA selectors for process/window/control metadata

Primary integration workflow:

```text
launch Notepad
→ locate editor using UIA
→ type "Hello Automation Hub"
→ verify editor/window state
→ close Notepad
```

If the save prompt appears, handle it through UIA.

## Acceptance

- workflow does not depend on fixed window position
- no image template is required
- Notepad scenario succeeds 5/5 times in the same supported environment
- locator failures stop safely and are diagnosable

---

# 8. Milestone 3 — Image Locator and Legacy Migration

## Goal

Add robust image fallback and move legacy tasks into the new workflow format.

## Deliverables

Image locator:

- `cv2.minMaxLoc`
- confidence reporting
- configurable threshold
- multi-scale matching
- ambiguity detection

Legacy migration:

- parse legacy filename DSL
- generate YAML workflows
- copy PNG assets
- preserve original legacy files

Migrate programmatically:

```text
price\static\auto_click
price\static\click_next_page
```

## Acceptance

- migrated workflows are generated by the migrator, not handwritten
- old source assets remain untouched
- image locator reports confidence
- ambiguous matches can halt instead of blindly clicking
- migrated workflows execute through V2

---

# 9. Milestone 4 — Verification and Retry

## Goal

Make V2 outcome-aware instead of assuming that an action succeeded.

## Deliverables

Initial verifiers:

- `window_exists`
- `window_disappeared`
- `uia_exists`
- `uia_disappeared`
- `image_exists`
- `image_disappeared`
- `file_exists`
- `screen_changed`

Execution policy:

```text
Locate
→ Action
→ Verify
→ Retry when configured
→ Success / Fail
```

Support:

- timeout
- retry count
- retry interval
- `on_fail: stop | continue`

## Acceptance

- failed verification is not reported as success
- retry covers the logical step attempt
- retries are bounded and cancellable
- final failures generate useful diagnostics
- representative success and failure tests exist

---

# 10. Milestone 5 — PyQt Integration

## Goal

Reconnect the new engine to the existing application without moving execution back into the GUI thread.

## Deliverables

Add:

- `AutomationService`
- worker-thread integration
- status/progress signals

Wire existing automation UI concepts to V2:

- workflow list
- step list
- run
- pause
- resume
- stop
- run count / loop mode
- logs/status

## Acceptance

- long-running automation does not freeze the GUI
- GUI does not directly call OpenCV / pyautogui / pywinauto
- stop works on an active workflow
- legacy business features outside automation remain intact

---

# 11. Milestone 6 — Target Picker / Step Capture

## Goal

Make workflow authoring easier without building a heavyweight full-session recorder.

## User Flow

```text
Click "Capture Target"
→ click a desktop element
→ inspect UIA metadata
→ crop local screenshot
→ create target strategies
```

Generated target should prefer:

```yaml
target:
  strategies:
    - type: uia
      ...
    - type: image
      ...
```

## Deliverables

Capture:

- process
- window
- control type
- name
- automation ID
- class name
- bounds
- element image

## Acceptance

- target can be captured without recording an entire desktop session
- generated target is human-readable
- UIA is primary where available
- image is a fallback, not the only locator

---

# 12. Milestone 7 — Excel / WPS Adapters

## Goal

Move spreadsheet automation away from visual clicking wherever APIs exist.

## Planned Capabilities

Excel:

- open workbook
- read/write values
- refresh
- save
- close
- run macro where appropriate

WPS:

- available COM/API integration
- WPS JS Macro integration where useful
- UIA/image only for capabilities lacking an API

## Acceptance

- spreadsheet operations prefer application APIs
- application-specific behavior is isolated behind adapters/actions
- generic workflow engine does not contain Excel/WPS-specific logic

---

# 13. Milestone 8 — MCP Interface

## Goal

Expose Automation Hub as a semantic tool surface for Codex / DSH / ChatGPT.

## Candidate MCP Operations

```text
list_workflows
get_workflow
run_workflow
get_run_status
pause_workflow
resume_workflow
stop_workflow
list_windows
capture_target
get_failed_step
```

## Acceptance

AI clients invoke meaningful workflows rather than raw desktop coordinates.

Preferred:

```text
run_workflow("export_report")
```

Not preferred:

```text
click(522, 311)
```

---

# 14. Milestone 9 — OCR and AI Vision

## Goal

Add higher-level visual fallbacks only after deterministic automation is reliable.

Potential order:

```text
OCR
→ bounded vision locator
→ optional VLM assistance
```

AI Vision should not replace UIA or native APIs when those are available.

This milestone is intentionally deferred.

---

# 15. Workflow Format Direction

Primary V2 workflow format:

```text
YAML
```

Representative example:

```yaml
name: export_report
version: 1

steps:
  - id: click_export
    name: 点击导出
    action: click

    target:
      strategies:
        - type: uia
          control_type: Button
          name: 导出

        - type: image
          template: assets/export.png
          threshold: 0.86

    expect:
      type: window_exists
      title_contains: 保存

    timeout: 5
    retry: 3
    retry_interval: 1
    on_fail: stop
```

The exact schema may evolve during implementation.

Architectural ownership rules for Action / Locator / Verifier belong in `AGENTS.md`.

---

# 16. Run Artifacts Direction

Each workflow run should eventually produce structured artifacts:

```text
runs/<run_id>/
    run.json
    log.txt
    screenshots/
```

A run should make it possible to answer:

- what workflow ran
- which step failed
- which locator strategy was used
- confidence / attempts
- how long it took
- what error occurred
- what the screen looked like on failure

Detailed implementation policy belongs in `AGENTS.md`.

---

# 17. Phase Dependencies

The intended dependency order is:

```text
M1 Core Engine
   ↓
M2 UIA
   ↓
M3 Image + Legacy Migration
   ↓
M4 Verification
   ↓
M5 GUI Integration
   ↓
M6 Target Picker
   ↓
M7 Excel/WPS Adapters
   ↓
M8 MCP
   ↓
M9 OCR / AI Vision
```

A later milestone may be pulled forward only when there is a concrete need and doing so does not undermine the core architecture.

---

# 18. Current Active Milestone

## Current target

**Milestone 1 — Core Workflow Engine**

Do not implement later milestones unless explicitly approved.

Expected work for the current milestone:

1. inspect current repository state
2. establish the V2 package skeleton needed for M1
3. implement workflow/step models
4. implement YAML loader
5. implement Action Registry
6. implement WorkflowExecutor
7. implement CancellationToken
8. implement the six initial actions
9. add `basic_test` workflow
10. add focused tests
11. run real validation
12. report results and stop

After Milestone 1 is complete, wait for review before starting Milestone 2.

---

# 19. Milestone Completion Report

For each milestone, report:

- delivered capabilities
- key files added/changed
- tests run and results
- real/integration validation
- known limitations
- migration impact
- recommended next milestone

Do not declare a milestone complete based only on code generation.

---

# 20. Document Ownership

Use this split going forward:

| Document | Owns |
|---|---|
| `plan.md` | roadmap, milestone scope, sequencing, deliverables, acceptance criteria, current active milestone |
| `AGENTS.md` | coding-agent behavior, architectural invariants, safety rules, Git discipline, testing discipline, repository working rules |

If a rule changes how agents must behave on every task, put it in `AGENTS.md`.

If a change affects what the project will build or when it will be built, put it in `plan.md`.

Avoid duplicating the same section in both documents.

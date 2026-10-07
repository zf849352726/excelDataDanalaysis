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

The V2 system should gradually replace filename-driven execution while preserving the current supported legacy workflows and existing business features.

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

The current migration baseline contains:

```text
price\static\auto_click
price\static\click_next_page
```

The historical `bim_cal`, `export_startand`, and `temporary_deletion_task` task folders and their 18 step images were retired before V2 implementation. They remain recoverable from Git history but are not part of the active legacy baseline or the planned migration scope.

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

**Status: Completed — 2026-10-07**

## Goal

Establish a safe starting point before structural changes.

## Deliverables

- inspect current Git status and history
- preserve existing working tree changes
- confirm current application/import baseline
- create a legacy safety reference if appropriate
- document the current automation entry points

## Acceptance

- current supported legacy code and the two active task folders are intact
- retired historical task assets are documented and remain recoverable from Git history
- no unrelated files are rewritten
- the documented Python 3.11 environment imports the legacy application successfully
- V2 work can begin without losing current supported legacy behavior

---

# 6. Milestone 1 — Core Workflow Engine

**Status: Completed — 2026-10-07**

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

M1 workflow loading must use a strict, minimal schema. Unsupported actions and fields, including `target`, `expect`, `retry`, and `on_fail`, must fail validation instead of being accepted and ignored.

Execution results must distinguish:

- action executed but not verified
- failed
- cancelled

The executor stops at the first failed step. Cancellation is cooperative and must interrupt `wait` promptly.

Create:

```text
workflows/basic_test/workflow.yaml
```

## Acceptance

- workflow loads from YAML
- unsupported fields and action names are rejected with explicit validation errors
- workflow can run without starting PyQt
- actions execute in declared order
- interruptible wait can be cancelled
- errors produce explicit step failures and stop later steps
- cancellation and unverified execution are represented explicitly in results
- unit tests pass
- `basic_test` runs end-to-end by launching a disposable process that exits by itself

## Out of Scope

Do not add UIA, image matching, GUI refactoring, MCP, OCR, AI Vision, global keyboard input, coordinate clicking, or window-closing actions in this milestone.

---

# 7. Milestone 2 — UIA Vertical Slice

**Status: Completed — 2026-10-07**

## Goal

Prove a complete semantic Windows automation path without image templates.

## Deliverables

Add:

- common `LocatorResult`
- locator interface
- UIA locator
- locator-chain foundation
- UIA selectors for process/window/control metadata
- target-bound `click`, `type_text`, and `close_window` actions
- the minimum window/UIA verification needed by the Notepad scenario

Target-bound actions must operate only on an element resolved for the current step. `close_window` must close only a window identified by the current run. It must not send a focus-based close command to an arbitrary foreground window.

Modern Windows Notepad may reuse an existing process and top-level window. The integration workflow therefore opens a uniquely named test document and invokes that active test tab's exact UIA `CloseButton`. It must not close the shared Notepad window or disturb pre-existing tabs.

Primary integration workflow:

```text
launch Notepad
→ locate editor using UIA
→ type "Hello Automation Hub"
→ verify editor/window state
→ close the uniquely identified test tab
```

The supported validation environment closes this test tab without a save prompt. If another supported variant displays one, it must be handled through a declared UIA target; without such a selector, the workflow stops safely instead of guessing.

## Acceptance

- workflow does not depend on fixed window position
- no image template is required
- the workflow verifies the expected text/window state before reporting success
- only the uniquely identified test document/tab owned by the run is closed
- pre-existing Notepad windows and tabs remain open
- Notepad scenario succeeds 5/5 times in the same supported environment
- locator failures stop safely and are diagnosable

---

# 8. Milestone 3 — Image Locator and Legacy Migration

**Status: Completed — 2026-10-07**

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
- migrated workflows can be run through V2 under human supervision
- runs without an explicit expectation are reported as action-executed-but-unverified, never as verified success

---

# 9. Milestone 4 — Verification Expansion and Retry

**Status: Completed — 2026-10-07**

## Goal

Expand the M2 vertical-slice verification into reusable outcome-aware policies instead of assuming that an action succeeded.

## Deliverables

Initial verifiers:

- `window_exists`
- `window_disappeared`
- `uia_exists`
- `uia_disappeared`
- `image_exists`
- `image_disappeared`
- `file_exists`

Only verifiers required by the M2 and M3 integration workflows are completion requirements for this milestone. Additional verifiers such as `screen_changed` should be added only with a concrete workflow and acceptance case.

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

# 10. Milestone 5 — PyQt5 Single-Run Integration

## Goal

Reconnect the new engine to the existing PyQt5 application without moving execution back into the GUI thread. Do not rewrite the GUI in C++ or migrate Qt bindings in this milestone.

## Deliverables

Add:

- `AutomationService`
- a `QObject` worker moved to a dedicated `QThread`
- status/progress signals

Worker-to-GUI communication must use queued signals/slots. Worker lifecycle and cleanup must be explicit; widgets are created and updated only on the main thread.

Threading model:

```text
PyQt5 main thread
      │ signals / slots
      ↓
AutomationService worker
      │
      ↓
WorkflowExecutor
```

Wire existing automation UI concepts to V2:

- workflow list
- step list
- single workflow run
- stop active workflow
- logs/status

## Acceptance

- long-running automation does not freeze the GUI
- V2 workflow execution paths in the GUI do not directly call OpenCV / pyautogui / pywinauto
- worker events update widgets only through main-thread signals/slots
- stop works on an active workflow
- legacy business features outside automation remain intact
- the existing screenshot button may retain its current behavior because it is outside the V2 execution path

---

# 10a. Milestone 5b — Pause, Resume, and Loop Control

## Goal

Complete execution controls before adding workflow authoring tools.

## Deliverables

- GUI-independent pause/resume control in the executor/service layer
- GUI pause and resume controls
- run count and loop mode
- cooperative pause/stop checks during waits, retries, and between loop iterations

## Acceptance

- pause does not block the Qt main thread
- resume continues the same active run safely
- stop can interrupt a paused run
- loop count is bounded when configured and does not hide individual run failures
- pause/resume and loop behavior have deterministic tests outside PyQt plus GUI integration validation

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

Only workflows explicitly marked as MCP-callable may be exposed for execution. Any workflow with desktop or other external side effects requires confirmation from the local operator through the PyQt5 application. If the confirmation UI is not running or approval cannot be obtained, `run_workflow` must reject the request explicitly.

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

- read-only discovery remains available without the GUI confirmation surface
- only allowlisted workflows can be requested through MCP
- side-effectful runs do not start before local confirmation
- missing or rejected confirmation produces an explicit refusal result

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

M1 supports only a strict minimal subset:

```yaml
name: basic_test
version: 1

steps:
  - id: wait_briefly
    action: wait
    seconds: 0.1

  - id: launch_disposable_process
    action: launch
    program: cmd.exe
    args: ["/d", "/c", "exit", "0"]
    wait_for_exit: true
```

The M1 `launch` action passes `program` and `args` directly to a process API with shell execution disabled. The loader must reject unknown workflow fields, step fields, and action names. Fields introduced by later milestones must not be silently retained or ignored.

Target format after M2-M4 capabilities are available:

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

The schema evolves only when its owning milestone implements and validates the corresponding behavior.

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
M4 Verification Expansion / Retry
   ↓
M5 PyQt5 Single-Run Integration
   ↓
M5b Pause / Resume / Loop Control
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

# 18. Current Milestone Gate

## Current state

**Milestone 4 — Verification Expansion and Retry is complete. Milestone 5 is pending review and is not active.**

Milestone 1 is complete and committed locally as `5c1f9fb`.

Milestone 1 delivered:

- GUI-independent workflow and result models
- strict M1 YAML loader
- explicit Action Registry
- sequential WorkflowExecutor with fail-fast behavior
- cooperative CancellationToken
- `wait` and shell-disabled `launch` actions
- `basic_test` workflow
- focused unit and integration tests

Validation completed with the documented Python 3.11 environment:

- full test suite: 20 passed
- `automation` imports without loading PyQt5
- `basic_test` completed end-to-end with both steps reported as `executed_unverified`

Milestone 2 delivered:

- common locator results, explicit locator/verifier registries, and a declared-order locator chain
- UIA process/window/control selectors with safe ambiguity handling and Windows process handoff support
- semantic UIA `click`, `type_text`, and target-bound `close_window` actions
- `uia_exists`, `uia_text_equals`, and `uia_disappeared` verification
- a Notepad workflow that opens, edits, verifies, and closes only its uniquely named test tab
- deterministic unit tests and an opt-in Windows UI integration test

Validation completed with the documented Python 3.11 environment:

- full default test suite: 38 passed, 1 UI integration test skipped by default
- opt-in Notepad UI integration: 5/5 verified runs in the same Windows environment
- `automation` imports without loading PyQt5
- the test document is restored unchanged and no test tab remains open after validation

Milestone 3 delivered:

- an image locator using `cv2.minMaxLoc`, actual confidence, configurable thresholds, declared scales, and ambiguity detection
- image-backed clicks that use only coordinates returned by the current locator result
- strict image strategy validation with workflow-relative template paths
- a deterministic legacy filename parser and non-overwriting migration command
- programmatically generated V2 workflows for `auto_click` and `click_next_page`
- byte-for-byte asset copies while preserving all source task files
- an explicitly enabled, supervised desktop test for migrated workflows

Validation completed with the documented Python 3.11 environment:

- full default test suite: 52 passed, 2 desktop integration tests skipped by default
- generated workflows load through V2 and contain no implicit expectations
- migrated workflow execution with controlled targets reports `executed_unverified`
- all four copied PNG assets match their source SHA-256 hashes
- committed migration output is reproducible from the active legacy task directories
- `automation` imports without loading PyQt5

The real migrated desktop workflows were not clicked during unattended validation. They are available through an opt-in test that requires `AUTOMATION_LEGACY_UI_TESTS=1` and human supervision, and it requires the final result to remain `executed_unverified`.

Milestone 4 delivered:

- per-attempt cooperative timeouts and bounded retries across locate, action, and verify
- cancellable retry intervals and explicit `on_fail: stop | continue` behavior
- final workflow failure retention when a failed step is allowed to continue
- structured attempt history, attempt counts, and verification diagnostics in step results
- reusable window, UIA, image, and workflow-relative file outcome verifiers
- strict schema validation for timeout, retry, retry interval, failure policy, and verifier targets
- a Notepad workflow compatible with both tabbed and classic UIA trees
- safe Notepad closing through a declared document close button or a new run-owned window
- explicit `discard_changes` handling for the run-owned classic Notepad save prompt

Validation completed with the documented Python 3.11 environment:

- full default test suite: 71 passed, 2 desktop integration tests skipped by default
- opt-in Notepad UI integration: 5/5 verified runs in the current classic Notepad environment
- timeout, retry success, retry exhaustion, retry cancellation, and continue-on-failure tests pass
- success and failure coverage exists for window, UIA, image, and file verification
- the Notepad test asset remains unchanged and no test window remains open
- `automation` imports without loading PyQt5

The migrated legacy desktop workflows remain supervised opt-in runs and still report `executed_unverified` when no expectation is declared.

Wait for review before starting Milestone 5.

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

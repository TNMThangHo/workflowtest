# Implementation Plan - Test Generation Improvements

## Phase 1: Matrix Engine Upgrade (v2.x) - [COMPLETED]

Goal: Transform the engine from "Field Validator" to "Business Logic Validator".

- [x] **v2.1: Semantic Rule Exploder** (Completed)
  - [x] Basic Happy/Negative paths.
  - [x] State Transition checks (e.g. Status changes).
- [x] **v2.2: Advanced Semantic Logic** (Completed)
  - [x] `_expand_search_advanced`: Multi-select, Dropdown Search.
  - [x] `_expand_ui_ux_gaps`: Link Nav, Notification checks.
  - [x] `_expand_security_implicit`: Unauthorized role checks.
- [x] **v2.3: Refinement & Fixes** (Completed)
  - [x] Fix Duplicates: Concurrency vs Approval Flow.
  - [x] Force Multi-select: Applied to all filter selects.
  - [x] Detail Popup Verification: Explicit field checks.
  - [x] Categorization: `Business Logic` -> `Functional`.
- [x] **v2.4: Human-like Titles** (Completed)
  - [x] Smart Title Extraction: `_get_rule_summary`.
  - [x] Professional Suffixes: "Standard Flow", "Violation Check".
  - [x] Removed robotic "Happy Path" naming.

## Phase 2: Apply to New Feature (Project Detail) - [NEXT]

Goal: Prove the new engine works on a complex, real-world PRD (`projectPrd.md`).

### 1. Extract Schema

- **Input**: `input/projectPrd.md`
- **Action**: Run `extract` step.
- **Verification**: Check `output/schema_input.json` for:
  - Correct "Tab" structure.
  - "Tree View" components.
  - "Task Management" sections.

### 2. Generate Test Cases

- **Action**: Run `explode` and `format` steps.
- **Verification**:
  - Verify Tree View test cases (Expand/Collapse, Drag&Drop).
  - Verify Tab navigation test cases.
  - Verify CRUD for sub-items (Tasks).
  - Confirm titles are human-readable.

### 3. Review & Refine

- **Action**: User review of `tc_project_v1.md`.
- **Feedback Loop**: Adjust engine if complex UI widgets (timeline, kanban) need specific logic.

## Phase 3: Documentation & Handover

- [ ] Update `README.md` with v2.x capabilities.
- [ ] Create `CONTRIBUTING.md` for adding new logic to `matrix_engine.py`.

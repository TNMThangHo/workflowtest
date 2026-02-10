# Implementation Plan - Test Generation Improvements

## Problem Analysis

The user's review of `tc4_e2e.md` against `projectPrd.md` reveals significant gaps:

- **Coverage**: Only ~35% of PRD is covered.
- **Missing Core Features**:
  - **Document Management**: Tree view, upload/OCR, versioning, permissions (Blocker).
  - **Task Management**: CRUD, filtering, deadline logic (Critical).
  - **Permissions**: Complex role mapping and logic (Critical).
  - **Project Details**: Tabs for "General Info" and "Progress" are largely ignored.
- **Current Behavior**: The generator seems to focus heavily on "Form Fields" (Section 4 & 5 of PRD) and generic validations/security, but misses the "Business Logic" and "Complex UI interactions" described in Section 3.

## Root Cause

- The **Test Generation Prompt** likely over-prioritizes "Inputs" and "forms" while under-analyzing "Workflow" and "Structure" descriptions in the PRD.
- The **Schema Extraction** might be missing nested structures or complex functional descriptions (like Tree View or Tabbed interfaces).
- **Matrix Engine** might not be configured to "explode" functional requirements that aren't simple field validations.

## Proposed Changes

### 1. Enhance `prompts.py` (The Architect)

- **Goal**: Force the AI to extract _Functional Flows_ and _UI Structures_ (Tabs, Trees, Tables) not just "Fields".
- **Action**:
  - Update `SYSTEM_PROMPT` or specific extraction prompts to explicitly look for:
    - "Tabbed Interfaces" -> Generate TCs for each tab.
    - "Tree/Hierarchical Structures" -> Generate TCs for expand/collapse, drag&drop.
    - "Business Rules" -> Explicitly map "Logic" interactions (e.g., "If Status=X then Y").
  - Add a "Rule Extraction" step that specifically lists actionable business rules from the PRD.

### 2. Update `matrix_engine.py` (The Factory)

- **Goal**: Add specialized generators for "Complex Widgets".
- **Action**:
  - Add logic to handle `view_type="tree"` or `view_type="kanban"` if detected in schema.
  - Implement a `generate_business_logic_tcs` function that takes the extracted rules and converts them into:
    - `Pre-condition`: [Rule Condition]
    - `Step`: [Action triggering rule]
    - `Expected`: [Rule Consequence]

### 3. Refine `schema_models.py`

- **Goal**: Capture more metadata from PRD.
- **Action**:
  - Add `features` list to `Schema` to capture high-level features (e.g., "Document Tree", "OCR").
  - Add `business_rules` list to explicitly store logic extracted from PRD.

## Verification Plan

1.  **Regenerate Test Cases**:
    - Run the `extract` and `finish` steps on `input/projectPrd.md`.
    - Command: `python -m test-gen.main --step init --prd input/projectPrd.md && python -m test-gen.main --step finish --prd input/projectPrd.md --filename tc4_improved`
2.  **Compare Coverage**:
    - Manually check if the new `tc4_improved.md` contains TCs for:
      - "Tab Hồ sơ" (Tree view, Upload).
      - "Tab Công việc" (Task CRUD).
      - "Tab Phân quyền".
3.  **Cross-reference with Review Report**:
    - Ensure the specific "Missing" items in `test_case_review_report.md` are now present.

## User Review Required

- **Prompts**: Changing prompts affects all future generations. Need to ensure it doesn't break simple cases.

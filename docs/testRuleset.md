# 🛡️ The Antigravity Testing Standard (Test Ruleset)

**Status**: ACTIVE | **Version**: 5.0 (Smart Schema Edition) | **Enforcement**: STRICT

## 1. Core Philosophy: "Defense in Depth"

This document verifies NOT just "if it works", but "if it can fail".
**Antigravity Agents** must apply these rules rigorously when generating test cases, reviewing code, or analyzing requirements.

> **The Golden Rule**: If a behavior is not explicitly defined, assume the STRICTEST possible interpretation until clarified.

> **The Source File Principle**: ⚠️ **ALWAYS trust source files (PRD, Swagger, specs) as the single source of truth**. NEVER rely on verbal communication, assumptions, or memory. Extract exact values from files and validate against them.

---

## 2. Functional Precision & Data Validation

### 2.1. Strict Input Validation (The "Atomic Splitting" Protocol)

**Goal**: Convert 1 Requirement into at least 4 Test Cases.

| Requirement Type | Splitting Strategy                                                                                                           |
| :--------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| **Input Fields** | 1. Valid Input (Happy Path)<br>2. Empty/Null (Validation)<br>3. Max Length + 1 (Boundary)<br>4. Special Chars/XSS (Security) |
| **Filters**      | 1. Single Select<br>2. Multi-Select<br>3. Select All<br>4. No Result Found                                                   |
| **Workflow**     | 1. Forward (Happy)<br>2. Backward (Cancel/Undo)<br>3. Interrupted (Network Fail)<br>4. Permission Denied                     |

### 2.2. State Transition Integrity

- **Illegal States**: Attempting to skip steps (e.g., "Checkout" without "Cart").
- **Idempotency**: Clicking "Submit" multiple times rapidly (Race condition check).
- **Concurrency**: Two users editing the same record simultaneously.

### 2.3. Matrix Testing Strategy (Combinatorial)

Refer to the "Orthogonal Array" method for combinatorics.

- If there are 3 Filters (A, B, C), do not just test A, B, C separately.
- **MUST TEST**: A+B, B+C, A+B+C.

---

## 3. UI/UX Perfection Standards (Eagle Eye)

**Goal**: The app must not only work but look and feel Premium.

### 3.1. Visual Fidelity (vs Design)

- **Pixel/Spacing**: Margins and paddings must match Design System tokens.
- **Typography**: No generic fonts. Check weights (Bold vs Semibold).
- **Empty States**: Must verify "No data found" illustration, not just blank space.

### 3.2. Responsive & Adaptive

- **Breakpoints**: Test at 320px, 768px, 1024px+.
- **Content Scaling**: Long text must truncate (`...`) or wrap, NEVER break layout.

### 3.3. Interaction & Feedback

- **Loading States**: Skeletons or Spinners must appear for async actions > 300ms.
- **Error State**: Verify red border and text specific to the error.
- **Feedback**: Success (Green Toast), Error (Red Message).

---

## 4. Security & Compliance (The "Dark Path")

### 4.1. Negative Testing Focus

- **Ratio**: 30% Positive / 70% Negative.
- **Focus**:
  - Double Submit (Click button twice fast).
  - SQL Injection in Search fields (`' OR 1=1`).
  - XSS in Name fields (`<script>`).
  - IDOR (Change ID in URL).

### 4.2. Authentication & Session

- **Token Expiry**: Redirect to Login cleanly.
- **Logout**: Invalidate session server-side.
- **Public vs Private**: Verify private routes redirect unauthenticated users.

---

## 5. Performance & Reliability

- **Timeouts**: Client should handle API delays > 30s gracefully.
- **Network Failure**: Show "Network Error" on disconnect.
- **Pagination**: Lists > 20 items must be paginated.

---

## 6. Output Standard for Test Cases

When Antigravity generates Test Cases, they MUST follow this JSON/Excel structure:

- **ID**: `[Feature]-[Sub]-[001]`
- **Title**: Action + Context + Expected Result.
- **Pre-condition**: Precise setup state.
- **Steps**: Numbered, atomic actions.
- **Expected Result**: Detailed outcome (UI Change, Data Change).
- **Type**: `Functional` | `Visual` | `Security` | `Performance`
- **Priority**: `P0` (Blocker) | `P1` (Critical) | `P2` (Major) | `P3` (Minor)

### 6.1. Excel Format Requirements

- **Created Date** (Format: `YYYY-MM-DD`): Timestamp when added.
- **Update Logic**: Append new rows, preserve existing formatting.

### 6.2. JSON Output Schema (Smart Schema v5.0)

See `test-gen/schema_models.py` for full definition.

Supported Types: `text` | `email` | `password` | `number` | `date` | `select` | `checkbox` | `radio` | `textarea` | `file` | `chart` | `list` | `table` | `label` | `text_display` | `tree_view` | `kanban_board` | `permission_matrix` | `tabs` | `file_upload`

**Input Format (For Architect):**

```json
{
  "feature_name": "Project Management",
  "sections": [
    {
      "name": "Document Management",
      "fields": [
        {
          "name": "Document Tree",
          "type": "tree_view",
          "required": true
        }
      ]
    }
  ],
  "business_rules": [
    {
      "id": "BR-01",
      "description": "...",
      "condition": "...",
      "expected_result": "..."
    }
  ]
}
```

## 7. Requirement Explosion Protocol

**CRITICAL RULE**: Do not map 1 Requirement to 1 Test Case. You must "explode" requirements into exhaustive scenarios using the **Atomic Splitting Protocol** defined in Section 2.1.

Mandatory Check:

1.  **Input Fields**: 4 TCs per field.
2.  **Complex Widgets**:
    - **Tree View**: Expand, Collapse, Drag&Drop, Search.
    - **Kanban**: Move Card, Status Update.
    - **Permissions**: Assign Role, Conflict check.
    - **Upload**: Valid file, Invalid ext, Max size, Malware.
3.  **Forms**: Happy Path + Validation Error + System Edge Case.
4.  **Features**: Check for Analytics, Rate Limiting, and Performance.

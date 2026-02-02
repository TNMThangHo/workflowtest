# 🛡️ The Antigravity Testing Standard (Test Ruleset)

**Status**: ACTIVE | **Version**: 2.1 | **Enforcement**: STRICT

## 1. Core Philosophy: "Defense in Depth"

This document verifies NOT just "if it works", but "if it can fail".
**Antigravity Agents** must apply these rules rigorously when generating test cases, reviewing code, or analyzing requirements.

> **The Golden Rule**: If a behavior is not explicitly defined, assume the STRICTEST possible interpretation until clarified.

> **The Source File Principle**: ⚠️ **ALWAYS trust source files (PRD, Swagger, specs) as the single source of truth**. NEVER rely on verbal communication, assumptions, or memory. Extract exact values from files and validate against them.

---

## 2. Functional Precision & Data Validation

### 2.1. Strict Input Validation (The "Zero Trust" Policy)

Every input field must be tested against these specific vectors:

- **Whitespace Handling**:
  - Leading/Trailing spaces must be TRIMMED before processing.
  - " " (Space only) must be treated as EMPTY/NULL.
- **Data Type integrity**:
  - Injecting `String` into `Number` fields.
  - Injecting `Boolean` into `Enum` fields.
  - Special Characters: Emojis, SQL Injection chars (`' --`), HTML/Script tags (`<script>`).
- **Boundaries**:
  - `Min Length - 1` (Underflow)
  - `Max Length + 1` (Overflow)
  - Exact Boundaries.

### 2.2. State Transition Integrity

- **Illegal States**: Attempting to skip steps (e.g., "Checkout" without "Cart", "Payment" without "Address").
- **Idempotency**: Clicking "Submit" multiple times rapidly (Race condition check).
- **Concurrency**: Two users editing the same record simultaneously.

### 2.3. Business Logic Constraints

- **Role Isolation**: Can a 'Viewer' trigger an 'Admin' API endpoint directly?
- **Data Ownership**: Can User A access User B's resource ID by changing the URL param? (IDOR).
- **Hard Limits**: Testing system limits (max items in cart, max file upload size).

---

## 3. UI/UX Perfection Standards

**Goal**: The app must not only work but look and feel Premium.

### 3.1. Visual Fidelity (vs Design)

- **Pixel/Spacing**: Margins and paddings must match the Design System tokens (4px, 8px, 16px...).
- **Typography**: No generic fonts (Time New Roman/Arial) unless specified. Checking correct Weights (Bold vs Semibold).
- **Empty States**: Every list/table must have a designed "No Data" state, not just blank space.

### 3.2. Responsive & Adaptive

- **Breakpoints**: Test at 320px (Mobile S), 768px (Tablet), 1024px+ (Desktop).
- **Content Scaling**: Long text must truncate (`...`) or wrap gracefully, NEVER break layout.

### 3.3. Interaction & Feedback

- **Loading States**: Skeletons or Spinners must appear for any async action > 300ms.
- **Feedback**:
  - Success: Toast/Notification (Green).
  - Error: User-friendly message (Red), NO "Server Error 500" raw dumps.
  - Button State: Buttons must be DISABLED while loading.

---

## 4. Security & Compliance Protocol

### 4.1. Authentication & Session

- **Token Expiry**: Actions after token expires must redirect to Login cleanly.
- **Logout**: Must invalidate session server-side.
- **Public vs Private**: Verify private routes redirect unauthenticated users.

### 4.2. Sensitive Data

- **Passwords**: Never visible in plain text (Input type=`password`).
- **PII**: Emails, Phones should be masked in logs/non-admin UIs if required.

---

## 5. Performance & Reliability

- **Timeouts**: What happens if the API takes 30s to respond? (Client should handle gracefully).
- **Network Failure**: Disconnect internet -> Click Action -> Should show "Network Error".
- **Pagination**: Lists > 20 items must be paginated or lazy-loaded.

---

## 6. Output Standard for Test Cases

When Antigravity generates Test Cases, they MUST follow this JSON/Excel structure:

- **ID**: `[Feature]-[Sub]-[001]`
- **Title**: Action + Context + expected Result.
- **Pre-condition**: Precise setup state.
- **Steps**: Numbered, atomic actions.
- **Test Data**: Exact strings/numbers used.
- **Expected Result**:
  - UI Change: "Toast appears..."
  - Data Change: "Record created in DB..."
  - System State: "User redirected to..."
- **Type**: `Functional` | `UI/UX` | `Security` | `Performance`
- **Priority**: `P0` (Blocker) | `P1` (Critical) | `P2` (Major) | `P3` (Minor)

### 6.1. Excel Format Requirements

**Testcase Excel Schema:**

When generating or updating testcase Excel files, include these mandatory columns:

- **Created Date** (Format: `YYYY-MM-DD`): Timestamp when the test case was added
  - For initial generation: All rows have the same creation date
  - For `/update-tc`: New rows have current date, existing rows keep original date
  - Purpose: Transparency and audit trail for test case lifecycle

**Update Workflow Rules:**

- When using `/update-tc`:
  - NEVER delete existing test cases
  - ALWAYS append new test cases at the end
  - PRESERVE all formatting, themes, and column widths
  - ADD "Created Date" column if not present (mark all as current date)
- When using `/update-tr`:
  - UPDATE only: Status, Actual Result, Evidence, Execution Date
  - PRESERVE: TestCase ID, Description, Expected Result, Test Steps, Priority
  - RECALCULATE summary statistics automatically

---

## 7. Riske Assessment Matrix

| Probability \ Impact   | Minor (Cosmetic) | Major (Function) | Critical (Data/Auth) |
| :--------------------- | :--------------- | :--------------- | :------------------- |
| **High (Common)**      | Medium           | High             | **Blocker**          |
| **Medium (Edge case)** | Low              | Medium           | High                 |
| **Low (Rare)**         | Info             | Low              | Medium               |

---

**Note**: This ruleset is dynamic. If a new usage pattern emerges, update this document immediately.

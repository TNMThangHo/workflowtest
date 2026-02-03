---
description: Generate Test Cases from PRD (Zero-Click)
---

// turbo-all

# WORKFLOW: /testcase - Zero-Click Test Case Generator

Workflow này **TỰ ĐỘNG HÓA TỐI ĐA** từ khâu đọc PRD đến khi ra file Test Case cuối cùng.

## 1. Input Collection

- [ ] Đường dẫn PRD (PDF, MarkDown, Docx) - (Bắt buộc).

## 2. Execute Pipeline (Automated - 2 Clicks)

1.  **Click 1: Khởi tạo (Init)**:
    // turbo
    - Lệnh: `python -m test-gen.main --step init --prd <prd_path>`
    - Tự động chạy Prepare + Extract trong 1 lệnh.

2.  **Agent Generates Test Cases**:
    - **Action**:
      - Đọc `output/requirements.json`.
      - Đọc `testRuleset.md`, `best_practices.md`.
      - **GENERATE**: Viết JSON vào `output/raw_testcases.json`.
      - **CRITICAL**: Phải bao phủ 100% Atomic Requirements (Functional, Security, Performance, Compatibility).

3.  **Click 2: Hoàn thiện (Finish)**:
    // turbo
    - Lệnh: `python -m test-gen.main --step finish --prd <prd_path> --filename tc_auto`
    - Tự động chạy Format + Validate trong 1 lệnh.

## 3. Finalize

- Pipeline tự động validate và báo kết quả.
- Thông báo: "Đã sinh xong Test Case tại `output/tc_auto.md` và đã Validate thành công!".

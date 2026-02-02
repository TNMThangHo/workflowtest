---
description: 🧪 Chỉ sinh Test Cases (Excel) từ PRD
---

// turbo-all

# WORKFLOW: /testcase - AI Test Case Generator

Workflow này chuyên biệt để sinh **Test Cases** chi tiết và xuất ra file MarkDown.

## 1. Input Collection

- [ ] Đường dẫn PRD (PDF, MarkDown, Docx).
- [ ] Đường dẫn Design (Folder ảnh) - Optional.

## 2. Prepare Context (Automated)

1.  **Chạy Orchestrator (Phase 1)**:
    // turbo
    - Lệnh: `python test-gen/main.py --step prepare`
    - Tool sẽ tự động quét `input/` (Swagger, Matrix, PRD) và `docs/references.md`.
    - Kết quả tổng hợp lưu trong `output/run_context.json`.

## 3. Agent Intelligence (Processing)

1.  **Nạp Context**:
    - `view_file output/run_context.json`.
    - `view_file` các file PRD.
    - `view_file docs/references.md` và `docs/test_generation_best_practices.md` (MANDATORY).
    - `view_file output/technical_specs.json` (Để lấy chính xác MaxLength, Regex, Error Codes).
    - `view_file output/test_matrix.json` (Để lấy các Scenario tổ hợp).

2.  **Sinh Test Cases (Strict Mode)**:
    - **Yêu cầu BẮT BUỘC**:
      - Đọc kỹ `docs/testRuleset.md`.
      - Test case sinh ra PHẢI bao gồm đủ: Functional, Validation (Boundaries), Security (Injection/Auth), UX, và Matrix Scenarios.
      - **CRITICAL PRINCIPLE**: ⚠️ **ALWAYS trust source files (PRD, Swagger), NOT verbal communication or assumptions**. Extract EXACT values from files (e.g., "< 1 giây" means 1000ms, not 3000ms).
      - **Self-Correction**: Trước khi lưu, tự hỏi "Mình đã có case check XSS chưa? Có case check min/max length chưa?". Nếu chưa, hãy bổsung ngay.
    - Output file: `output/raw_testcases.json`.

## 4. Finalize & Validate (Automated)

1.  **Chạy Orchestrator (Phase 2)**:
    // turbo
    - Lệnh: `python test-gen/main.py --step format`
    - Tool sinh file `output/test_cases.md`.

2.  **CRITICAL: Run Validation**:
    // turbo
    - Lệnh: `python test-gen/validate_testcases.py --prd <prd_path> --testcases output/test_cases.md`
    - **If validation fails (exit code 1):**
      - Review reported discrepancies
      - Fix test cases in `raw_testcases.json`
      - Re-run format step
      - Re-run validation until PASS (exit code 0)

3.  **Review**:
    - Kiểm tra `output/test_cases.md` (Đây là file kết quả cuối cùng để User sử dụng).

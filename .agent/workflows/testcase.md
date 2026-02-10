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
    - Lệnh: `python -m test_gen.main --step init --prd <prd_path>`
    - Tự động chạy Prepare + Extract trong 1 lệnh.

2.  **Agent Generates Test Cases**:
    - **Step 2.1: Eagle Eye Analysis (Visual QA)** (Optional):
      - **Check**: Đọc `metadata` từ Output `init` để tìm `figma_links`.
      - **Action**:
        - **Case A (Có ảnh trong `input/`)**:
          - **Action**: Dùng tool `view_file` để xem file ảnh này.
          - **Analysis**: Sau khi xem ảnh, tự phân tích bằng **Native Vision** (Mắt của Agent).
        - **Case B (Có Figma Link Public)**:
          - Dùng tool `browser_subagent` truy cập URL Figma -> Chụp màn hình (`screenshot`) -> lưu `input/figma_capture.png`.
          - Dùng tool `view_file` để xem ảnh `input/figma_capture.png`.
        - **Case C (Không có gì)**: Bỏ qua bước này.
      - **GENERATE**:
        - Dựa trên hình ảnh vừa xem, sinh danh sách Test Case JSON (category='Visual') kiểm tra: Layout, Contrast, Typography, Premium Feel.
        - _Lưu ý_: Không cần chạy script bên ngoài, hãy dùng khả năng nhìn của chính bạn.

    - **Step 2.2: Smart Schema Generation (v5.0)**:
      - **Input**: Đọc `output/requirements.json` và PRD.
      - **Action**: Đóng vai trò "Architect", trích xuất dữ liệu thành file **JSON Schema** theo cấu trúc trong `docs/testRuleset.md` (Smart Schema section).
      - **Output**: Lưu file tại `output/schema_input.json`.
      - **CRITICAL**: Không được tự viết test case. Chỉ viết Schema (Fields, Rules).

    - **Step 2.3: Matrix Explosion**:
      - **Command**: `python -m test_gen.main --step explode --schema output/schema_input.json`
      - **Effect**: Tool Matrix Engine sẽ tự động nhân bản Schema thành 50-100 Test Case (Valid/Invalid/Security/Edge) vào `output/raw_testcases.json`.

3.  **Click 2: Hoàn thiện (Finish)**:
    // turbo
    - Lệnh: `python -m test_gen.main --step finish --prd <prd_path> --filename tc_auto`
    - Tự động chạy Format + Validate trong 1 lệnh.

## 3. Finalize

- Pipeline tự động validate và báo kết quả.
- Thông báo: "Đã sinh xong Test Case tại `output/tc_auto.md` và đã Validate thành công!".

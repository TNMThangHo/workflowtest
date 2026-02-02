---
description: 📝 Chỉ sinh Test Plan (Markdown) từ PRD
---

// turbo-all

# WORKFLOW: /test-plan - AI Test Plan Generator

Workflow này chuyên biệt để lập **Test Plan** (Kế hoạch kiểm thử).

## 1. Input Collection

- [ ] Đường dẫn PRD.

## 2. Agent Processing

1.  **Đọc PRD**: Hiểu phạm vi và yêu cầu dự án.
2.  **Lập Test Plan**:
    - Xác định Scope (In-scope, Out-scope).
    - Chiến lược kiểm thử (Manual, Auto, API, UI).
    - Môi trường & Tài nguyên.
    - Lịch trình & Rủi ro.

## 3. Output Generation

1.  **Lưu kết quả JSON**:
    - Tạo file `output/raw_testplan.json`.
    - Cấu trúc:
      ```json
      {
        "test_plan": "# Test Plan Title\n\n## Scope..."
      }
      ```
2.  **Chạy Formatter**:
    // turbo
    - Lệnh: `python test-gen/format_output.py --input output/raw_testplan.json`

## 4. Review

- Kiểm tra file `output/TEST_PLAN.md`.

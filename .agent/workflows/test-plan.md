---
description: Generate Test Plan from PRD (Zero-Click)
---

// turbo-all

# WORKFLOW: /test-plan - Automated Test Plan Generator

Workflow này **TỰ ĐỘNG HÓA HOÀN TOÀN** việc sinh Test Plan từ PRD.

## 1. Input Collection

- [ ] Đường dẫn PRD (PDF, MarkDown, Docx) - (Mặc định: `input/*.md` nếu không chỉ định).

## 2. Generate Plan (Automated)

1.  **Đọc Tài Liệu Nguồn**:
    - `view_file` PRD của User.
    - `view_file test-gen/templates/test-plan-template.md`.

2.  **Sinh Nội Dung (Agent Action)**:
    - **Nhiệm vụ**: Dựa vào PRD, hãy điền thông tin vào Template Test Plan.
    - **Yêu cầu**:
      - Giữ nguyên cấu trúc của Template.
      - Điền Feature Name, Scope, Environment (lấy từ PRD requirements).
      - Schedule: Để Placeholder [TBD] nếu chưa có.
    - **Lưu file**: `output/TEST_PLAN.md`.

3.  **Review**:
    - Thông báo cho User: "File Test Plan đã được sinh tự động tại `output/TEST_PLAN.md`. Mời anh review!".

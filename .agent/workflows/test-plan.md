---
description: Generate Test Plan from PRD (Zero-Click)
---

// turbo-all

# WORKFLOW: /test-plan - Automated Test Plan Generator

Workflow này **TỰ ĐỘNG HÓA HOÀN TOÀN** việc sinh Test Plan từ PRD.

## 1. Input Collection

- [ ] Đường dẫn PRD (PDF, MarkDown, Docx) - (Mặc định: `input/*.md` nếu không chỉ định).

## 2. Generate Plan (Automated)

1.  **Đọc Metadata từ PRD (CRITICAL FIRST STEP)**:
    - `view_file` PRD **dòng 1-15** để lấy metadata table.
    - **Extract thông tin sau**:
      - **Dự án**: Project Name
      - **QA Lead**: Tên QA Lead
      - **Tester(s)**: Danh sách Testers (có thể nhiều người, phân tách bằng dấu phẩy)
      - **Supporting Developer**: Tên Developer
      - **BA/PO**: Tên BA/PO
    - **Lưu ý**: Nếu PRD không có metadata này, để [TBD].

2.  **Đọc Template và PRD Requirements**:
    - `view_file test-gen/templates/test-plan-template.md`.
    - `view_file` phần Requirements của PRD (In-scope, Out-scope, Security, Performance...).

3.  **Sinh Nội Dung (Agent Action)**:
    - **Nhiệm vụ**: Dựa vào PRD metadata và requirements, điền thông tin vào Template Test Plan.
    - **Yêu cầu**:
      - Giữ nguyên cấu trúc của Template.
      - **Section 6 (Resources & Roles)**:
        - Sử dụng tên thật từ metadata (không để [TBD] nếu có data).
        - **QUAN TRỌNG**:
          - Dùng role **"Supporting Developer"** (không tách Backend/Frontend).
          - Dùng role **"Tester(s)"** (không tách QA Engineer 1/2/Automation).
        - Map đúng: QA Lead, Tester(s), Supporting Developer, BA/PO, DevOps.
      - Điền Feature Name, Scope, Environment (lấy từ PRD requirements).
      - Schedule: Để Placeholder [TBD] nếu chưa có.
    - **Lưu file**: `output/TEST_PLAN.md`.

4.  **Review**:
    - Thông báo cho User: "File Test Plan đã được sinh tự động tại `output/TEST_PLAN.md`. Mời anh review!".

---
description: Generate Release Notes (Zero-Click)
---

// turbo-all

# WORKFLOW: /release-note - Automated Release Note Generator

Workflow này **TỰ ĐỘNG HÓA HOÀN TOÀN** việc sinh Release Note từ PRD hoặc Change Log.

## 1. Input Collection

- [ ] Đường dẫn PRD hoặc List thay đổi.

## 2. Generate Notes (Automated)

1.  **Đọc Tài Liệu Nguồn**:
    - `view_file` PRD của User.
    - `view_file test-gen/templates/release-note-template.md`.

2.  **Sinh Nội Dung (Agent Action)**:
    - **Nhiệm vụ**: Tổng hợp các tính năng mới, bug fix (giả định hoặc từ task list) vào Release Note.
    - **Yêu cầu**:
      - Version: Lấy từ PRD (nếu có) hoặc để [vX.Y.Z].
      - Features: Liệt kê các User Stories chính.
      - Known Issues: Liệt kê các giới hạn Out-scope từ PRD.
    - **Lưu file**: `output/RELEASE_NOTES.md`.

3.  **Review**:
    - Thông báo cho User: "File Release Note đã được sinh tự động tại `output/RELEASE_NOTES.md`.".

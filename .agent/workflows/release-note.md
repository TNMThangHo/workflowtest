---
description: 📢 Chỉ sinh Release Note (Markdown) từ PRD
---

// turbo-all

# WORKFLOW: /release-note - AI Release Note Generator

Workflow này chuyên biệt để viết **Release Note** cho người dùng cuối.

## 1. Input Collection

- [ ] Đường dẫn PRD (để biết tính năng mới).
- [ ] (Optional) Danh sách bug đã fix.

## 2. Agent Processing

1.  **Đọc PRD**: Nắm bắt các tính năng mới và giá trị cốt lõi.
2.  **Viết Release Note**:
    - Sử dụng ngôn ngữ marketing/user-friendly.
    - Highlight tính năng nổi bật.
    - Liệt kê Bug fixes (nếu có).

## 3. Output Generation

1.  **Lưu kết quả JSON**:
    - Tạo file `output/raw_releasenote.json`.
    - Cấu trúc:
      ```json
      {
        "release_note": "# Release Note v1.0\n\n## 🚀 New Features..."
      }
      ```
2.  **Chạy Formatter**:
    // turbo
    - Lệnh: `python test-gen/format_output.py --input output/raw_releasenote.json`

## 4. Review

- Kiểm tra file `output/RELEASE_NOTE.md`.

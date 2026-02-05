---
description: 👁️ Eagle Eye - Visual QA & UX Critique (No API Key required)
---

# WORKFLOW: /visual-qa

Workflow này sử dụng **Antigravity Vision (Multimodal Skill)** để phân tích giao diện UI/UX mà **KHÔNG cần cài đặt API Key**.

## 1. Setup

1.  User chụp ảnh màn hình cần test.
2.  Lưu file vào folder `input/` (ví dụ: `input/screenshot.png`).

## 2. Execute (Eagle Eye Scan)

**Agent Steps:**

1.  **Locate Image**:
    - Tìm file ảnh mới nhất trong folder `input/`.
    - Nếu không thấy, yêu cầu user cung cấp đường dẫn tuyệt đối.

2.  **Visual Analysis (Native Vision)**:
    - **Tool**: Sử dụng tool `view_file` để xem file ảnh.
    - **Analysis**:
      - Agent tự quan sát ảnh bằng "Mắt thần" (Native Capabilities).
      - KHÔNG gọi script bên ngoài. KHÔNG cần API Key.
    - **Prompt**:
      > "Đóng vai Senior UX/UI Expert. Phân tích ảnh chụp màn hình này dựa trên:
      >
      > 1.  **Layout & Spacing**: Canh lề có chuẩn không? Khoảng cách có đều không?
      > 2.  **Color & Contrast**: Độ tương phản có đạt chuẩn Accessibility (WCAG) không?
      > 3.  **Typography**: Font chữ có dễ đọc và phân cấp rõ ràng không?
      > 4.  **Premium Feel**: Đánh giá độ thẩm mỹ (1-10).
      >
      > Output format: Markdown Report chuyên nghiệp."

3.  **Report Generation**:
    - Lưu kết quả phân tích vào file: `output/visual_review.md`.
    - Format lại nội dung cho đẹp (dùng Github Alert nếu phát hiện lỗi nghiêm trọng).

## 3. Finalize

- Thông báo cho user: "Đã hoàn thành Visual Review tại `output/visual_review.md`. Mời bạn xem kết quả!"

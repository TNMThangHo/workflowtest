# 🚀 ROADMAP: The "Eagle Eye" Strategy (Visual Intelligence Focus)

User định hướng: **Bỏ qua sinh code & self-healing -> Tập trung tối đa vào Visual AI.**
Mục tiêu mới: Trở thành công cụ **"QA Thẩm mỹ & Trải nghiệm" (Visual & UX Quality Gate)** số 1.

Chúng ta sẽ không cạnh tranh với Playwright/Selenium (về chạy test). Chúng ta sẽ làm điều họ làm rất tệ: **"Nhìn và Đánh giá giao diện"** như một Designer/Product Owner thực thụ.

---

## 👁️ Core Pillar: AI Visual Validator (The "Eagle Eye")

Biến tool thành một "AI Design Reviewer" tích hợp trong quy trình test.

### 1. UI Consistency Check (Soi điểm ảnh thông minh)

- **Vấn đề:** Các tool so sánh ảnh truyền thống (Pixel-diff) rất ngu. Lệch 1px cũng báo lỗi.
- **Giải pháp AI:** Dùng **Native Agent Vision** (Mắt của AI) để so sánh **"Ý nghĩa"** giao diện.
  - _Input:_ Ảnh Mockup (Figma) vs Ảnh chụp màn hình thật (Live).
  - _AI Check:_ "Font chữ này có vẻ nhỏ hơn design", "Màu nút này đỏ quá, design là đỏ đô", "Khoảng cách padding hơi chật".
  - _Output:_ Report khoanh vùng các lỗi Visual/CSS sai lệch với Design System.

### 2. UX Heuristic Evaluation (Đánh giá trải nghiệm)

- **Tính năng:** Chấm điểm UX dựa trên Nielsen's Heuristics.
- **Workflow:**
  - Chụp ảnh màn hình (hoặc upload ảnh).
  - AI đóng vai "UX Expert" phân tích:
    - "Nút Cancel quá gần nút OK -> Dễ bấm nhầm."
    - "Contrast text thấp -> Khó đọc."
    - "Flow này thiếu nút Back."
- **Giá trị:** Tìm ra lỗi thiết kế _trước khi_ user tìm thấy.

### 3. Accessibility (A11y) Deep Scan

- **Tính năng:** Không chỉ check code (như Lighthouse), mà check **Ngữ cảnh**.
- **Ví dụ:**
  - AI nhìn ảnh và bảo: "Văn bản này đè lên ảnh nền phức tạp -> Người mắt kém không đọc được" (Lighthouse không bắt được cái này).
  - "Thứ tự tab (Tab order) trong form này không logic với bố cục nhìn thấy."

---

## 🗺️ Implementation Plan (Giai đoạn tiếp theo)

### Phase 1: The "Visual Critic" (MVP)

- **Input:** User upload 1 ảnh màn hình (hoặc URL để bot tự chụp).
- **Action:** AI phân tích theo checklist: Layout, Color, Typography, Spacing.
- **Output:** Markdown Report nhận xét về độ đẹp/chuẩn của UI.

### Phase 2: Design vs Implementation Check

- **Input:** File ảnh Design + File ảnh Thực tế.
- **Action:** So sánh và chỉ ra các điểm sai lệch (Visual Diffing).

### Phase 3: Automated Visual Testing Pipeline

- Tích hợp vào CI/CD: Mỗi khi deploy -> Tự chụp ảnh -> Gửi AI check -> Báo cáo về Slack nếu giao diện bị vỡ.

---

**Khác biệt cạnh tranh:** Hầu hết tool hiện nay chỉ check _Functional_ (Đúng logic). Tool của chúng ta sẽ check _Quality_ (Đẹp & Chuẩn). Đây là "Đại dương xanh" của Testing Tools.

# Outline Presentation: AI-Driven Quality Control Workflow

Dưới đây là nội dung chi tiết cho bài thuyết trình của bạn. Bạn có thể copy từng phần vào Google Slides.

---

## Slide 1: Trang Tiêu đề

**Tiêu đề lớn:** Next-Gen QA Automation Workflow
**Tiêu đề phụ:** Tự động hóa Test Case & Kiểm soát chất lượng với AI Hybrid Architecture
**Người trình bày:** [Tên của bạn]
**Nội dung chính:**

- Giới thiệu hệ thống "Test Gen v5.0"
- Demo quy trình AWF
- Các công cụ hỗ trợ QC hiện đại (Schemathesis, Hypothesis)

---

## Slide 2: Vấn đề (The Consultant's Dilemma)

**Tiêu đề:** Tại sao chúng ta cần tự động hóa?
**Nội dung:**

- **Thách thức:**
  - Viết Test Case thủ công tốn quá nhiều thời gian (Manual Effort).
  - Độ bao phủ thấp (Low Coverage) - thường bỏ sót các ca biên/corner cases.
  - PRD thay đổi liên tục -> Test Case nhanh chóng lỗi thời.
  - Thiếu nhất quán giữa các tester.
- **Mục tiêu:**
  - Giảm thời gian viết TC từ _giờ_ xuống _giây_.
  - Tăng độ bao phủ lên 100% yêu cầu PRD.
  - Chuẩn hóa định dạng và chất lượng.

---

## Slide 3: Giải pháp - Test Gen v5.0

**Tiêu đề:** Smart Schema Architecture (AI + Python)
**Nội dung:**

- **Khái niệm:** Một quy trình Hybrid kết hợp sức mạnh của AI (Gemini) và sự chính xác của Code (Python).
- **Sự khác biệt:**
  - _AI thuần túy:_ Có thể gặp vấn đề về ảo giác (hallucination) hoặc thiếu nhất quán.
  - _Test Gen v5.0:_ AI đóng vai trò "Kiến trúc sư" (Architect) trích xuất cấu trúc -> Python đóng vai trò "Nhà máy" (Factory) sản xuất Test Case hàng loạt.
- **Kết quả:** Tạo ra hàng chục Test Cases chi tiết với cấu trúc chuẩn xác trong thời gian ngắn.

---

## Slide 4: Kiến trúc hệ thống (How it Works)

**Tiêu đề:** Luồng xử lý dữ liệu (Data Pipeline)
**Hình ảnh minh họa (gợi ý):** Sơ đồ [PRD] -> [AI Extract] -> [JSON Schema] -> [Matrix Engine] -> [Test Cases].
**Nội dung:**

1.  **Input:** PRD (File Markdown) + UI Design (Ảnh/Screenshot).
2.  **Phase 1 - Architect:** AI phân tích nghiệp vụ, tách Business Rules và Validation Rules thành file `schema.json`.
3.  **Phase 2 - Matrix Engine:** Python Code tự động "bùng nổ" (explode) các yêu cầu:
    - 1 trường Email -> sinh ra nhiều test cases (Valid, Invalid format, Empty, SQL Injection, XSS...).
4.  **Output:** File Markdown Test Case hoàn chỉnh & File Excel báo cáo.

---

## Slide 5: Tính năng nổi bật

**Tiêu đề:** Không chỉ là viết Test Case
**Nội dung:**

- **Matrix Engine:** Tự động tổ hợp các kịch bản biên (Boundary Value Analysis).
- **Visual QA (Eagle Eye):** Tận dụng khả năng của AI Vision để hỗ trợ so sánh UI thực tế với Design System (Overview).
- **Hypothesis Integration:** Tích hợp thư viện _Hypothesis_ để sinh dữ liệu test ngẫu nhiên (Fuzzing).
- **Auto Validation:** Kiểm tra chéo với PRD để đảm bảo các yêu cầu quan trọng không bị bỏ sót.

---

## Slide 6: Hướng dẫn sử dụng (User Guide) - Phần 1

**Tiêu đề:** Quy trình kiểm thử cơ bản
**Nội dung:**
Từ việc lên kế hoạch đến tạo Test Case chi tiết:

- **Bước 1: Lập kế hoạch kiểm thử (Test Planning)**
  - Lệnh: `/testplan @input/PRD.md`
  - _AI Action:_ Đọc PRD, trích xuất Metadata (Scope, Roles, Schedule) và tự động điền vào mẫu _Master Test Plan_.
  - _Kết quả:_ File `output/TEST_PLAN.md` chuyên nghiệp.
- **Bước 2: Sinh Test Case (Test Generation)**
  - Lệnh: `/testcase @input/PRD.md`
  - _AI Action:_ Chạy _Matrix Engine_ để bùng nổ hàng trăm test case.
  - _Kết quả:_ File `output/tc_auto.md` sẵn sàng cho execution.

---

## Slide 7: Hướng dẫn sử dụng (User Guide) - Phần 2

**Tiêu đề:** Báo cáo & Cập nhật
**Nội dung:**
Tự động hóa các công việc giấy tờ sau khi test:

- **Bước 3: Cập nhật kết quả test**
  - Tester cập nhật trạng thái (Pass/Fail) trực tiếp vào file Markdown/Excel.
- **Bước 4: Sinh báo cáo (Test Reporting)**
  - Lệnh: `/test-report`
  - _AI Action:_ Tổng hợp kết quả, tính toán % Pass/Fail, vẽ biểu đồ (nếu có).
  - _Kết quả:_ File `output/TEST_REPORT.xlsx` và `output/SUMMARY_REPORT.md` để gửi khách hàng.
- **Bước 5: Cập nhật báo cáo (Update Report)**
  - Lệnh: `/update-tr`
  - _AI Action:_ Đồng bộ kết quả từ file Markdown (đã tick chọn Pass/Fail) ngược lại vào file Excel Report.
- **Bước 6: Bảo trì (Maintenance)**
  - Lệnh: `/update-tc`
  - _AI Action:_ Khi PRD thay đổi, tự động cập nhật lại Test Case mà không làm mất kết quả test cũ.

---

## Slide 8: Hệ sinh thái hỗ trợ - AWF

**Tiêu đề:** Antigravity Workflow Framework (AWF)
**Nội dung:**

- **Là gì:** Framework quản lý quy trình làm việc thông minh cho Developer/QC.
- **Tính năng:**
  - **Context Management:** Ghi nhớ ngữ cảnh dự án dài hạn (Project Brain).
  - **Workflow Automation:** Tự động hóa các tác vụ lặp lại (git, deploy, test generation) bằng các lệnh slash command (`/init`, `/plan`, `/test`).
  - **Lợi ích cho QC:** Giúp QC tập trung vào việc kiểm thử khó (exploratory testing) thay vì các tác vụ giấy tờ (documentation).

---

## Slide 9: Công cụ QC Nâng cao - Schemathesis

**Tiêu đề:** Automated API Testing với Schemathesis (Recommended)
**Nội dung:**

- **Vấn đề:** Test API thủ công thường tốn nhiều công sức để cover hết các edge cases.
- **Schemathesis là gì:** Công cụ test API mạnh mẽ dựa trên Swagger/OpenAPI spec (được đề xuất tích hợp).
- **Cách hoạt động:**
  - Đọc file Swagger.
  - Tự động sinh ra hàng nghìn request biên để kiểm thử độ bền của API.
  - Phát hiện các lỗi 500 Internal Server Error tiềm ẩn.
- **Tại sao nên dùng:** Bổ sung khả năng kiểm thử bảo mật và độ ổn định cho hệ thống.

---

## Slide 10: Tổng kết & Lợi ích

**Tiêu đề:** Giá trị mang lại (ROI)
**Nội dung:**

- **Tăng năng suất:** Giảm đáng kể thời gian viết tài liệu lặp lại.
- **Chất lượng cao:** Đảm bảo độ bao phủ yêu cầu (Requirements Coverage) ở mức cao.
- **Tiêu chuẩn hóa:** Mọi Test Case đều tuân theo chuẩn format của dự án.
- **Mở rộng:** Dễ dàng tích hợp vào quy trình CI/CD.

---

## Slide 11: Q&A

**Tiêu đề:** Hỏi đáp
**Nội dung:**

- Mời mọi người đặt câu hỏi về Workflow hoặc Demo.
- Thông tin liên hệ / Link Repository.

---

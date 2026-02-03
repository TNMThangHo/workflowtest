# 📋 KẾ HOẠCH WORKFLOW TỰ ĐỘNG HÓA KIỂM THỬ (BẢN PRODUCTION)

## 1. MỤC TIÊU HỆ THỐNG

Xây dựng quy trình khép kín, tự tối ưu và có khả năng tự phục hồi từ khâu tiếp nhận PRD (Markdown) đến khi xuất báo cáo, đảm bảo chất lượng AI đầu ra ở mức cao nhất.

## 2. CẤU TRÚC WORKFLOW NÂNG CAO

### Giai đoạn 1: Khởi tạo & Trích xuất (Input Layer)

- **Input:** File PRD (Markdown).
- **Command:** `/testcase [loại kiểm thử]` (Ví dụ: `/testcase smoke`).
- **Logic Xử lý:**
  - **`markdown_parser.py`** : Phân rã PRD thành các Feature Module dựa trên Heading ID.
  - **Context Extraction** : Trích xuất Technical Stack và Metadata.

### Giai đoạn 2: Thế hệ Test Case Đa Kỹ Thuật (Logic Layer)

- **Logic AI (Multi-Technique):** Tự động áp dụng BVA, EP, Decision Table, State Transition và Error Guessing dựa trên ngữ cảnh từng module.
- **`validator.py` (Chốt chặn):** AI tự rà soát lại (Chain-of-Verification) để loại bỏ case vô lý, trùng lặp hoặc sai `schema.py`.
- **Output:** Bảng Test Case chuẩn hóa (ID, Module, Title, Steps, Expected, Priority).

### Giai đoạn 3: Lập kế hoạch & Báo cáo (Output Layer)

- **Test Plan:** Tự động ước tính thời gian dựa trên số lượng và độ phức tạp của Test Case.
- **Test Report:** Tổng hợp kết quả thực thi, tính toán tỷ lệ Pass/Fail và phân tích rủi ro.

### Giai đoạn 4: Cập nhật & Phân tích Tác động (Sync Layer)

- **Command:** `/update`.
- **Impact Analysis:** AI không chỉ tìm "Delta" mà còn phân tích xem thay đổi ở Module này có ảnh hưởng đến Test Case của Module khác không (Regression Impact).
- **State Management:** Lưu trữ lịch sử tại thư mục `data/` để đối chiếu phiên bản.

---

## 3. CHỈ THỊ KỸ THUẬT & RÀNG BUỘC (STRICT RULES)

- **Lỗi Định dạng:** Nếu PRD thiếu Heading hoặc sai cấu trúc, `main.py` phải trả về thông báo lỗi cụ thể cho người dùng (Exception Handling).
- **Token Management:** Sử dụng chiến lược Chunking (chia nhỏ file) nếu PRD vượt quá giới hạn ngữ cảnh của AI.
- **Chất lượng:** Mọi Test Case sinh ra phải vượt qua bộ lọc của `validator.py`.

---

## 4. DANH SÁCH FILE TRIỂN KHAI TOÀN CẢNH

| **STT** | **File**             | **Chức năng chi tiết**                                                            |
| ------- | -------------------- | --------------------------------------------------------------------------------- |
| 1       | `main.py`            | **Orchestrator** : Tiếp nhận lệnh, điều phối luồng và xử lý lỗi toàn cục.         |
| 2       | `markdown_parser.py` | **Parser** : Chuyển đổi Markdown thành cấu trúc JSON tinh gọn.                    |
| 3       | `generator.py`       | **Core AI** : Thực thi các kỹ thuật viết testcase chuyên sâu từ `prompts.py`.     |
| 4       | **`validator.py`**   | **Quality Gate** : Kiểm tra logic và định dạng đầu ra của AI trước khi lưu.       |
| 5       | `prompts.py`         | **Prompt Library** : Lưu trữ các template Prompt và kỹ thuật kiểm thử.            |
| 6       | `updater.py`         | **Impact Tracker** : So sánh phiên bản và phân tích tác động thay đổi.            |
| 7       | `reporter.py`        | **Formatter** : Xuất bản `test_plan.md`và `test_report.md`.                       |
| 8       | `schema.py`          | **Data Model** : Định nghĩa cấu trúc dữ liệu nhất quán cho toàn hệ thống.         |
| 9       | `logger.py`          | **Monitor** : Ghi nhật ký vận hành để phục vụ debug và tối ưu Prompt.             |
| 10      | `data/`(Folder)      | **Vault** : Lưu trữ trạng thái (State) của các phiên bản kiểm thử dưới dạng JSON. |

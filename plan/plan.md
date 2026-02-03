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

- **Test Plan:** File Markdown `output/test_cases.md` chứa danh sách test case đã được định dạng bảng.
- **Test Report:** File Excel `output/TEST_REPORT.xlsx` chứa thống kê Pass/Fail và Breakdown theo Type/Priority. File `output/SUMMARY_REPORT.md` tóm tắt nhanh.

### Giai đoạn 4: Cập nhật & Phân tích Tác động (Sync Layer)

- **Command:** `/update` triggers `python -m test-gen.main --step sync`.
- **Impact Analysis:** Hệ thống so sánh ID và Title để xác định test case mới. (Roadmap: Phân tích Regression Impact dựa trên Dependency Graph).
- **State Management:** Lưu trữ snapshot tại thư mục `output/` để đối chiếu phiên bản.

---

## 3. CHỈ THỊ KỸ THUẬT & RÀNG BUỘC (STRICT RULES)

- **Lỗi Định dạng:** Nếu PRD thiếu Heading hoặc sai cấu trúc, `main.py` phải trả về thông báo lỗi cụ thể cho người dùng (Exception Handling).
- **Token Management:** Sử dụng chiến lược Chunking (chia nhỏ file) nếu PRD vượt quá giới hạn ngữ cảnh của AI.
- **Chất lượng:** Mọi Test Case sinh ra phải vượt qua bộ lọc của `validator.py`.

---

## 4. DANH SÁCH FILE TRIỂN KHAI TOÀN CẢNH

| **STT** | **File**             | **Chức năng chi tiết**                                                               |
| ------- | -------------------- | ------------------------------------------------------------------------------------ |
| 1       | `main.py`            | **Orchestrator** : Tiếp nhận lệnh, điều phối luồng và xử lý lỗi toàn cục.            |
| 2       | `markdown_parser.py` | **Parser** : Chuyển đổi Markdown thành cấu trúc JSON tinh gọn.                       |
| 3       | `generator.py`       | **Core AI** : Thực thi các kỹ thuật viết testcase chuyên sâu từ `prompts.py`.        |
| 4       | **`validator.py`**   | **Quality Gate** : Kiểm tra logic và định dạng đầu ra của AI trước khi lưu.          |
| 5       | `prompts.py`         | **Prompt Library** : Lưu trữ các template Prompt và kỹ thuật kiểm thử.               |
| 6       | `updater.py`         | **Sync Engine** : Đồng bộ test case mới vào file cũ, bảo toàn history (Append-only). |
| 7       | `reporter.py`        | **Reporter** : Sinh báo cáo Excel (`xlsx`) và Summary (`md`) từ kết quả test.        |
| 8       | `schema.py`          | **Data Model** : Định nghĩa cấu trúc `TestCase`, `TestSuite` chuẩn JSON.             |
| 9       | `logger.py`          | **Logger** : Ghi log màu ra console và file `logs/test_gen.log`.                     |
| 10      | `output/`(Folder)    | **Artifacts** : Chứa `raw_testcases.json`, `test_cases.md`, `run_context.json`.      |

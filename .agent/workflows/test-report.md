---
description: 📊 Sinh Test Report từ file kết quả Testcase
---

// turbo-all

# WORKFLOW: /test-report - AI Test Report Generator

Workflow này phân tích file Excel kết quả test và sinh báo cáo tổng hợp.

## 1. Input Collection

- [ ] Đường dẫn file Excel chứa kết quả test (vd: `output/test_cases.xlsx`).

## 2. Analysis & Report Generation

1.  **Chạy Orchestrator (Report Phase)**:
    - Dùng tool `run_command` để chạy script phân tích.
      // turbo
    - Lệnh: `python test-gen/main.py --step report`
    - Tool sẽ đọc `output/test_cases.md` và sinh `output/TEST_REPORT.xlsx`.

## 3. Review

- Thông báo cho user file báo cáo Excel đã xong: `output/TEST_REPORT.xlsx`.

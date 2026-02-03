---
description: Generate Test Report from Output (Zero-Click)
---

// turbo-all

# WORKFLOW: /test-report - Automated Test Report Generator

Workflow này **TỰ ĐỘNG HÓA HOÀN TOÀN** việc sinh Báo cáo Kiểm thử.

## 1. Input Collection

- [ ] Đường dẫn file Markdown kết quả test check (vd: `output/tc001.md` hoặc `output/test_cases.md`).

## 2. Report Generation (Automated)

1.  **Chạy Lệnh Sinh Báo Cáo**:
    // turbo
    - Lệnh: `python -m test-gen.main --step report --input <input_file_path>`
    - **Lưu ý**: Nếu User chạy lệnh /test-report mà không đưa tham số, hãy tự tìm file mới nhất trong `output/`.

## 3. Review

- Thông báo: "Báo cáo đã xong! Check `output/SUMMARY_REPORT.md` và `output/TEST_REPORT.xlsx`".

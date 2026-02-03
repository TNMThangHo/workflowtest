---
description: 🔄 Update test report với kết quả test mới
---

# WORKFLOW: /update-tr - Update Test Report (Zero-Click)

## 🎯 Mục đích

Update test report Excel với execution results từ test case markdown (status checkboxes).

## ✅ Input

- Test case markdown file với status checkboxes format: `[x] Pass / [ ] Fail / [ ] Skip / [ ] Blocked`
- Existing Excel report (default: `output/TEST_REPORT.xlsx`)

## 🚀 Execution (Automated)

// turbo-all

1. **Update report từ test case markdown**:

   ```powershell
   python -m test-gen.main --step update-report --input <testcase_file> [--report-file <report_path>]
   ```

   Script sẽ:
   - Parse markdown file để extract status từ checkbox format
   - Match TestCase IDs giữa markdown và Excel
   - Update Status column (Pass/Fail/Skip/Blocked)
   - Color-code cells (Green/Red/Yellow/Gray)
   - Update Execution Date
   - Create backup của report cũ
   - Save updated report: `output/updated_TEST_REPORT_<timestamp>.xlsx`
   - Print summary statistics

## 📊 Output

- ✅ Updated Excel report: `output/updated_TEST_REPORT_<timestamp>.xlsx`
- ✅ Backup file: `output/backup_TEST_REPORT_<timestamp>.xlsx`
- ✅ Summary statistics in console

## 📝 Example Usage

```powershell
# Update với file mặc định output/TEST_REPORT.xlsx
python -m test-gen.main --step update-report --input output/tc_auto.md

# Update với custom report file
python -m test-gen.main --step update-report --input output/tc_auto.md --report-file path/to/report.xlsx
```

## 🎯 Status Checkbox Format

Markdown phải có column **status** với format:

```
[x] Pass / [ ] Fail / [ ] Skip / [ ] Blocked  → Pass
[ ] Pass / [x] Fail / [ ] Skip / [ ] Blocked  → Fail
[ ] Pass / [ ] Fail / [x] Skip / [ ] Blocked  → Skip
[ ] Pass / [ ] Fail / [ ] Skip / [x] Blocked  → Blocked
```

## 📋 Prerequisites

- ✅ File test report Excel đã có
- ✅ File kết quả test mới (JSON/CSV/Excel format)

## 🚀 Execution Steps

### Phase 1: Gather Context & Inputs

1. **Hỏi user về file paths:**

   ```
   📁 File test report Excel cũ: [Nhập đường dẫn]
   📁 File kết quả test mới: [Nhập đường dẫn]
   ```

2. **Hỏi user về format của kết quả test:**

   ```
   📝 Format của file kết quả test:
   A) JSON - {"testcase_id": "TC001", "status": "Pass", "actual_result": "...", "evidence": "..."}
   B) CSV/Excel - Columns: TestCase ID, Status, Actual Result, Evidence

   → User chọn: [A/B]
   ```

3. **Validate files tồn tại:**
   - Check report Excel file exists
   - Check results file exists
   - Show file info to user

### Phase 2: Automated Update

// turbo-all 4. **Parse test results:**

```powershell
python -m test-gen.update_report --mode=parse --results <results_path> --format <json|csv|excel>
```

Script sẽ:

- Đọc file kết quả test
- Parse theo format
- Tạo mapping: TestCase ID → Results
- Save to: `output/parsed_results.json`

5. **Update report với kết quả mới:**

   ```powershell
   python -m test-gen.update_report --mode=update --report <report_path> --parsed-results output/parsed_results.json
   ```

   Script sẽ:
   - Load existing report Excel
   - Match TestCase IDs
   - Update ONLY these columns:
     - Status (Pass/Fail/Skip/Blocked)
     - Actual Result
     - Evidence (screenshot paths, logs)
     - Execution Date (TODAY)
   - PRESERVE these columns:
     - TestCase ID
     - Description
     - Expected Result
     - Test Steps
     - Priority
     - Category
   - Recalculate summary statistics
   - Save to: `output/updated_report_[timestamp].xlsx`
   - Create backup: `output/backup_report_[timestamp].xlsx`

### Phase 3: Summary & Statistics

6. **Show update summary:**

   ```
   ✅ Test Report Updated!

   📊 Statistics:
   - Total test cases: X
   - Updated: Y test cases
   - Not found in results: Z

   📈 Test Results:
   - Pass: XX (YY%)
   - Fail: XX (YY%)
   - Skip: XX (YY%)
   - Blocked: XX (YY%)

   🕐 Execution Date: YYYY-MM-DD

   📁 Output:
   - Updated report: output/updated_report_[timestamp].xlsx
   - Backup: output/backup_report_[timestamp].xlsx
   ```

7. **Ask user to verify:**
   ```
   🔍 Please review:
   - Status updated correctly?
   - Actual Results match your test execution?
   - Evidence paths correct?
   - Summary statistics look right?
   ```

## 📤 Output

- ✅ Updated test report Excel file
- ✅ Backup of original report
- ✅ Summary statistics (Markdown)

## ⚠️ Important Notes

- Only execution results are updated
- Test case descriptions are NEVER changed
- Original report is BACKED UP
- If TestCase ID not found in results → Status remains unchanged
- Summary sheet is auto-recalculated

## 📊 Test Results File Format

### Option A: JSON Format

```json
[
  {
    "testcase_id": "TC001",
    "status": "Pass",
    "actual_result": "User logged in successfully",
    "evidence": "screenshots/login_success.png"
  },
  {
    "testcase_id": "TC002",
    "status": "Fail",
    "actual_result": "Error 500 displayed",
    "evidence": "screenshots/error_500.png"
  }
]
```

### Option B: CSV/Excel Format

```
TestCase ID | Status | Actual Result | Evidence
TC001       | Pass   | User logged in successfully | screenshots/login_success.png
TC002       | Fail   | Error 500 displayed | screenshots/error_500.png
```

## 🔄 NEXT STEPS

```
1️⃣ Cần update testcase? → /update-tc
2️⃣ Share report với stakeholders? → Copy file Excel
3️⃣ Re-run tests? → /test
```

---

## 🛡️ Error Handling

### If report file not found:

```
❌ File test report không tìm thấy: <path>
→ Kiểm tra lại đường dẫn
→ Hoặc chạy /test-report để tạo report mới
```

### If results file not found:

```
❌ File kết quả test không tìm thấy: <path>
→ Kiểm tra lại đường dẫn
```

### If TestCase IDs mismatch:

```
⚠️ Warning: Một số TestCase IDs không match
   - Not found in report: [TC099, TC100]
   - Not found in results: [TC001, TC002]

→ Tiếp tục update cho các IDs match được?
```

### If invalid status value:

```
❌ Invalid status: <value>
→ Allowed values: Pass, Fail, Skip, Blocked
→ Please fix results file
```

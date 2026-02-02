---
description: 🔄 Update testcase Excel với requirements mới
---

# WORKFLOW: /update-tc - Incremental Testcase Update

// turbo-all

## 🎯 Mục đích

Thêm test cases mới vào file Excel đã có mà KHÔNG cần regenerate toàn bộ. Giữ nguyên test cases cũ + formatting.

## 📋 Prerequisites

- ✅ File testcase Excel đã có (từ lần chạy `/testcase` trước)
- ✅ File PRD mới hoặc đã update

## 🚀 Execution Steps

### Phase 1: Gather Context & Inputs

1. **Hỏi user về file paths:**

   ```
   📁 File testcase Excel cũ: [Nhập đường dẫn]
   📁 File PRD mới: [Nhập đường dẫn]
   ```

2. **Validate files tồn tại:**
   - Check Excel file exists
   - Check PRD file exists
   - Show file info to user

### Phase 2: Automated Context Preparation

3. **Prepare context cho AI:**

```powershell
python test-gen/update_testcase.py --mode=prepare --excel <excel_path> --prd <prd_path>
```

Script sẽ:

- Đọc Excel cũ → Extract all TestCase IDs
- Đọc PRD mới → Parse requirements
- Tạo context file: `output/update_context.json`

### Phase 3: AI Generation (Agent Task)

4. **Agent đọc context và generate:**
   - Đọc `output/update_context.json`
   - Đọc `docs/testRuleset.md` (strict quality rules)
   - Đọc `docs/references.md` (nếu có external refs)

5. **Call Gemini API để sinh test cases MỚI:**

   ```
   Prompt:
   "Based on the NEW requirements in PRD, generate comprehensive test cases.

   IMPORTANT:
   - ONLY generate test cases for NEW features/requirements
   - SKIP test cases that already exist in the following IDs: [existing_ids]
   - Follow strict quality rules in testRuleset.md
   - Include: Functional, UI/UX, Security, Performance tests

   Existing TestCase IDs to AVOID:
   {existing_ids}

   PRD Content:
   {prd_content}
   "
   ```

6. **Self-Correction Check:**
   - Review generated test cases against `testRuleset.md`
   - Check for duplicates with existing IDs
   - Verify coverage of new requirements

### Phase 4: Merge & Format

7. **Append new test cases vào Excel:**

```powershell
python test-gen/update_testcase.py --mode=merge --excel <excel_path> --new-cases <generated_json>
```

Script sẽ:

- Load existing Excel (preserve all data)
- Append new rows with `Created Date = TODAY`
- Copy formatting/theme from original
- Save to: `output/updated_testcase_[timestamp].xlsx`
- Create backup: `output/backup_[timestamp].xlsx`

### Phase 4.5: **VALIDATION** (MANDATORY)

8. **Validate ALL test cases against PRD:**

```powershell
python test-gen/validate_testcases.py --prd <prd_path> --testcases <updated_file>
```

⚠️ **CRITICAL**: Validation MUST pass before proceeding!

Script kiểm tra:

- ✅ Performance SLAs match PRD (API response time, email delivery)
- ✅ Browser compatibility coverage complete
- ✅ All requirements from PRD have corresponding tests
- ❌ **Exit code 1 = VALIDATION FAILED** → Must fix issues before continuing

**If validation fails:**

```
❌ VALIDATION FAILED - Issues found:
1. [HIGH] PERFORMANCE_MISMATCH
   - test_case: TC-SIGNUP-PERF-001
   - prd_requirement: < 3s (3000ms)
   - test_case_value: 1000ms

→ FIX the test cases manually or regenerate
→ Re-run validation until PASS
```

### Phase 5: Quality Review

10. **Show summary to user:**

```
✅ Update Complete!

📊 Statistics:
- Original test cases: X
- New test cases added: Y
- Total test cases: X + Y
- Created Date: YYYY-MM-DD

✅ Validation: PASSED

📁 Output:
- Updated file: output/updated_testcase_[timestamp].xlsx
- Backup file: output/backup_[timestamp].xlsx

🔍 Please review:
- Formatting preserved?
- Theme/colors intact?
- "Created Date" column visible?
```

11. **Ask user to open and verify Excel file**

## 📤 Output

- ✅ Updated testcase Excel file
- ✅ Backup of original file
- ✅ Summary report (Markdown)

## ⚠️ Important Notes

- Original file is BACKED UP before modification
- All existing test cases are PRESERVED
- Only NEW test cases are appended
- "Created Date" shows when each test was added

## 🔄 NEXT STEPS

```
1️⃣ Cần update test report? → /update-tr
2️⃣ Chạy test mới? → /test
3️⃣ Tạo test plan mới? → /test-plan
```

---

## 🛡️ Error Handling

### If Excel file not found:

```
❌ File Excel không tìm thấy: <path>
→ Bạn có chắc đường dẫn đúng không?
→ Hoặc chạy /testcase để tạo file mới
```

### If PRD file not found:

```
❌ File PRD không tìm thấy: <path>
→ Kiểm tra lại đường dẫn
```

### If no new requirements detected:

```
⚠️ Không phát hiện requirements mới trong PRD
→ PRD này có giống với lần trước không?
→ Nếu đúng thì không cần update testcase
```

### If API error:

```
❌ Gemini API error: <message>
→ Kiểm tra GEMINI_API_KEY
→ Retry sau vài giây
```

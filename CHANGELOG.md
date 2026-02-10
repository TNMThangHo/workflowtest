# Changelog

## [2026-02-10] - Matrix Engine v2 & Python Package Refactor

### Added

- **Matrix Engine v2 (Rule Explosion)**: Implemented logic to split single business rules into Happy Path, Negative Case, and Boundary/Transition checks.
- **Pairwise Filter Combinations**: Automatically generates test cases for combined filter scenarios (e.g., Region + Area).
- **Smart Actions**: Conditional logic verification (e.g., "Reject" action requires "Reason" field).
- **Visual Checks**: Added verifications for "Empty State", "Long Content", and "Tooltips".

### Changed

- **Package Structure**: Renamed `test-gen` directory to `test_gen` to support standard Python module execution (`python -m test_gen.main`).
- **Data Enrichment**: Replaced `hypothesis` library with standard `random` to improve stability and remove heavy dependencies.

### Fixed

- **Schema Model**: Added missing `description` field to `FieldType` in `schema_models.py`.
- **Import Errors**: Resolved relative import issues in `main.py` and `format_output.py`.

---

## [2026-02-05] - Super Explosion Strategy & Vision QA

### Added

- **Super Explosion Strategy (v4.0)**: Updated `prompts.py` to enforce Atomic Constraint Splitting, ensuring >30 test cases per feature.
- **Dashboard Verified**: Generated `tc0001.md` (25 TCs) covering Widget Logic and Visual QA.
- **Visual QA (Eagle Eye)**: Integrated Native Agent Vision for UI/UX testing without API keys.
- **Hypothesis Integration**: Added fuzz testing capabilities for robustness.

### Changed

- **Prompt Logic**: Switched from generic "Explosion" to specific "Atomic Splitting" protocol.
- **Environment**: Removed `.env` dependency, moved to fully local execution.

### Fixed

- **Low Test Coverage**: Resolved the issue where only basic happy paths were generated. Now detailed edge cases are mandatory.

---

## [2026-02-03] - Test Plan & Report Improvements

### Added

- **Metadata extraction** trong `/test-plan` workflow
  - Đọc tự động thông tin team từ PRD (QA Lead, Testers, Developer, BA/PO)
  - Không còn placeholder [TBD] trong Test Plan
- **Markdown test report generation** (`update_report.py`)
  - Parse checkbox status từ test case markdown
  - Generate formatted report với statistics
  - Output: `UPDATED_TEST_REPORT_<timestamp>.md`
- **--target argument** trong `main.py` để support `/update-tc` workflow

### Changed

- **Simplified Test Plan roles** để khớp với PRD structure:
  - Gộp QA Engineer 1/2/Automation → **Tester(s)**
  - Gộp Backend/Frontend Developer → **Supporting Developer**
- **Converted `/update-tr` workflow** từ Excel sang Markdown format
  - User preference cho .md files
  - Dễ version control hơn Excel
  - Template-based generation đơn giản hơn

### Fixed

- Import errors trong `update_report.py` (relative imports)
- Logger reference errors (dùng `log` instead of `logger`)
- Markdown parsing không nhận diện test case IDs (fixed regex pattern)
- Missing --target argument gây lỗi khi chạy sync step

### Technical Details

- Files changed: 3 files, 282 insertions(+), 299 deletions(-)
- Commits:
  - `f987a87`: Improve test plan workflow with metadata extraction
  - `a74f4f1`: Convert update-tr workflow to markdown format

---

# Changelog

All notable changes to the "WorkflowTest" project.

## [2026-02-02] - Strict Mode & Incremental Updates

### Added

- **Strict Mode Test Generation**: `/testcase` workflow now enforces mandatory reading of `testRuleset.md` and `best_practices.md`.
- **Incremental Updates**: Added `/update-tc` workflow to append new test cases without regenerating existing ones (`test-gen/update_testcase.py`).
- **Validation Pipeline**: Added `validate_testcases.py` to strictly check PRD compliance (SLAs, Browsers) before completion.
- **Ruleset**: Added `docs/test_generation_best_practices.md` and updated `docs/testRuleset.md`.

### Changed

- **Test Generation**: Switched from "loose interpretation" to "strict source-file trust". Values (> 500ms) are now extracted exactly from PRD.
- **Workflow**: Updated `.agent/workflows/testcase.md` to include validation steps.
- **Validation**: Strict SLA enforcement (e.g., < 1s vs < 5s) in generated tests.

### Fixed

- **Context Drift**: Fixed issue where AI would ignore `references.md` in previous runs.
- **Test Overwrite**: Prevented `/update-tc` from overwriting existing successful test cases.

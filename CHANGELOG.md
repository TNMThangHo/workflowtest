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

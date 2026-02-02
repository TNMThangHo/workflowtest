# 🤖 AI Test Case Generator (Test Gen v3)

Automate your QA workflow with AI using this "Smart Test Generator". It analyzes your Product Requirements (PRD), Swagger Specs, and Test Matrix to generate high-coverage test cases automatically.

## ✨ Features

- **Smart Analysis**: Reads PRD text, Swagger JSON, and Test Matrix.
- **Strict Mode**: Enforces security checks (XSS, SQLi), validation boundaries, and UX rules.
- **Workflow Automation**: 2-Step process (Prepare -> Generate -> Format).
- **Auto Reporting**: Generates Markdown test cases and Excel reports.

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+

### 2. Installation

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd <REPO_FOLDER>

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage

**Step 1: Prepare Inputs**

- Place your PRD (Markdown) in `input/`.
- (Optional) Place `swagger.json` and `matrix_factors.json` in `input/`.

**Step 2: Run Automation**

This project uses the AWF workflow system. If you don't have the AWF CLI, you can run the python scripts directly:

```bash
# Phase 1: Prepare Context (Reads inputs)
python test-gen/main.py --step prepare

# Phase 2: Generate Test Cases (Use your LLM Agent here to read `output/run_context.json`)
# ... (Or manually create output/raw_testcases.json)

# Phase 3: Format Output (Markdown & Excel)
python test-gen/main.py --step format
```

**Available Workflows:**

- **/testcase** - Generate comprehensive test cases from PRD
- **/test-plan** - Generate Test Plan from PRD (Scope, Strategy, Resources)
- **/test-report** - Generate test execution report
- **/release-note** - Generate Release Note from PRD (User-friendly, Feature highlights)
- **/update-tc** - Update existing testcase Excel with new requirements (appends new test cases)
- **/update-tr** - Update test report with new execution results (updates status, results, evidence)

**Update Workflows:**

The update workflows allow you to incrementally update existing test artifacts without regenerating from scratch:

```bash
# Update testcase Excel with new requirements
python test-gen/update_testcase.py --mode=prepare --excel <path> --prd <new_prd_path>
# ... (Agent generates new test cases)
python test-gen/update_testcase.py --mode=merge --excel <path> --new-cases <generated_json>

# Update test report with new execution results
python test-gen/update_report.py --mode=parse --results <results_path> --format json
python test-gen/update_report.py --mode=update --report <report_path> --parsed-results output/parsed_results.json
```

## 🔄 How to Reuse (Template Strategy)

**Important**: This tool runs **locally** within the project folder. It is NOT installed globally like typical CLI tools (npm/pip global).

To use this tool for a **new project**, treat this repository as a **Template**:

1. **Clone** this repository again (or fork it).
2. **Rename** the folder to your new project name.
3. **Clean up**:
   - Delete files in `input/` (keep `swagger.json` if needed).
   - Delete files in `output/`.
4. **Run**: Normal setup (`pip install -r requirements.txt`).

✅ This ensures every project has its own isolated PRDs, Test Cases, and Reports.

## 📂 Project Structure

- `input/`: Drop your input files here.
- `output/`: Generated results (Test Cases, Reports).
- `docs/`: Reference documentation (`references.md`, `testRuleset.md`).
- `test-gen/`: Core Python scripts.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

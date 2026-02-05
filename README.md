# 🤖 AI Test Case Generator (Test Gen v4.0)

Automate your QA workflow with AI using this "Smart Test Generator". It analyzes your Product Requirements (PRD) and UI Design (Images) to generate high-coverage test cases automatically.

> **v4.0 Update**: Now features **"Super Explosion Strategy"** (>30 TCs/feature) and **Native Visual QA** (Eagle Eye).

## ✨ Key Features

- **💥 Super Explosion Strategy**: Automatically splits validation rules into atomic test cases (Valid, Invalid, Boundary, Security). Guarantees >30 cases per standard form.
- **👁️ Eagle Eye Vision (Visual QA)**: Uses Native Agent Vision to critique UI/UX (Layout, Colors, Typography) without external API keys.
- **🛡️ Hypothesis Integration**: Smart data fuzzing (XSS payloads, Boundary values) injected directly into test steps.
- **🔒 Strict Mode**: Enforces security checks (XSS, SQLi, IDOR) and performance SLAs.
- **⚡ Zero-Click Workflow**: Two-step process (Init -> Finish) handles everything from parsing to formatting.

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- Git

### 2. Installation

```bash
# Clone the repository
git clone <YOUR_REPO_URL>
cd <REPO_FOLDER>

# Install dependencies (Minimal)
pip install -r requirements.txt
```

### 3. Usage (The AWF Workflow)

**Step 1: Input**

- Drop your PRD (Markdown) into `input/`.
- (Optional) Drop Figma screenshot `input/screen.png` for Visual QA.

**Step 2: Run Automation**

```bash
# 1. Initialize & Analyze (Atomic Splitting)
python -m test-gen.main --step init --prd input/signupPrd.md

# 2. Generate & Format (Super Explosion + Enrichment)
python -m test-gen.main --step finish --prd input/signupPrd.md --filename tc_auto
```

**Output**:

- `output/tc_auto.md`: The detailed Test Case Document (Markdown).
- `output/raw_testcases.json`: Traceable JSON source.

## 🧠 Core Strategies

### 1. Atomic Constraint Splitting

Instead of _"Verify Password"_, the tool generates:

- Verify Password Empty
- Verify Password < 8 Chars
- Verify Password Missing Uppercase
- Verify Password Missing Special Char

### 2. The "4-Scenario" Protocol

For every input field, we generate at least 4 variants:

1. **Happy Path** (Valid)
2. **Boundary** (Min/Max)
3. **Invalid Format** (Regex)
4. **Security** (XSS/SQLi)

## 📂 Project Structure

- `input/`: Drop PRDs and Images here.
- `output/`: Generated Artifacts.
- `test-gen/`: Core Logic (Prompts, Fuzzer, Parser).
- `docs/`: Rulesets and Best Practices.

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch
3. Commit your Changes
4. Push to the Branch
5. Open a Pull Request

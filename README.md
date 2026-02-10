# 🤖 AI Test Case Generator (Test Gen v5.0)

Automate your QA workflow with AI using this "Smart Test Generator". It analyzes your Product Requirements (PRD) and UI Design (Images) to generate high-coverage test cases automatically.

> **v5.0 Update (Feb 2026)**: Now features **"Smart Schema Architecture"** (Hybrid AI + Python) generating **60-100+ TCs per feature** with support for Forms, Dashboards, and Complex Business Logic.

## ✨ Key Features

- **🧠 Smart Schema v5.0**: Hybrid architecture where AI acts as "Architect" (extracting structured JSON schema) and Python acts as "Factory" (algorithmic expansion into 60-100+ test cases).
- **📊 Multi-Type Support**:
  - **Forms**: Text, Email, Password, Number, Select, Checkbox, Radio, Date, File
  - **Dashboards**: Charts, Lists, Tables, Labels, Widgets
  - **Business Logic**: Calculation rules (VAT, Discounts), State Machines, Payment flows
- **💥 Matrix Engine**: Automated test case explosion covering:
  - Validation (Min/Max, Required, Format)
  - Security (XSS, SQLi, HTML/Command/Null Byte Injection)
  - Compatibility (Chrome, Firefox, Safari, Edge, Mobile)
- **👁️ Eagle Eye Vision (Visual QA)**: Uses Native Agent Vision to critique UI/UX (Layout, Colors, Typography) without external API keys.
- **🛡️ Random Fuzzer**: Robust data fuzzing (XSS payloads, Boundary values) using standard Python libraries.
- **🔒 Strict Validation**: Enforces security checks, performance SLAs, and browser compatibility.
- **⚡ Zero-Click Workflow**: Two-step process (Init → Finish) handles everything from parsing to formatting.

## 🏗️ v5.0 Architecture (Smart Schema)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   PRD.md    │  ───► │  AI Agent    │  ───► │ Schema.json │
│ + Image     │       │ (Architect)  │       │ (Concise)   │
└─────────────┘       └──────────────┘       └─────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │ Matrix Engine│
                                              │  (Factory)   │
                                              └──────────────┘
                                                      │
                                                      ▼
                                              ┌──────────────┐
                                              │ 90-100+ TCs  │
                                              │  (Detailed)  │
                                              └──────────────┘
```

**Benefits:**

- **Token Efficient**: AI outputs ~100 lines of JSON instead of 1000+ lines of test cases
- **Predictable**: Python code ensures deterministic expansion (no hallucinations)
- **Scalable**: Complex features (Checkout, Payment) generate 100+ cases automatically
- **Maintainable**: Schema-first approach makes updates easier

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.8+
- Git

### 2. Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/workflowtest.git
cd workflowtest

# Install dependencies
pip install -r requirements.txt
```

### 3. Usage (The AWF Workflow)

**Step 1: Input**

- Drop your PRD (Markdown) into `input/`.
- (Optional) Drop UI screenshot `input/screen.png` for Visual QA.

**Step 2: Run Automation**

```bash
# 1. Initialize & Extract Schema
python -m test_gen.main --step init --prd input/yourFeature.md

# 2. Generate & Format (Smart Schema Expansion)
python -m test_gen.main --step finish --prd input/yourFeature.md --filename tc_auto

> **Crucial for v5.0**: To enable Smart Schema (90+ TCs), the AI Agent MUST first act as the "Architect" to generate `output/schema_*.json` from the PRD using `testRuleset.md` logic. The standard command above only runs the Python Matrix Engine if a schema exists.
```

**Or use AWF workflow:**

```bash
/testcase @input/yourFeature.md @input/screen.png
```

**Output**:

- `output/tc_auto.md`: The detailed Test Case Document (Markdown).
- `output/raw_testcases.json`: Traceable JSON source.
- `output/schema_*.json`: Extracted Smart Schema.

## 🧪 Proven Results

| Feature Type     | PRD Complexity                        | Generated TCs | Time |
| ---------------- | ------------------------------------- | ------------- | ---- |
| Signup Form      | Basic (6 fields)                      | ~60 TCs       | 15s  |
| Dashboard        | Medium (10 widgets)                   | ~80 TCs       | 18s  |
| Checkout/Payment | Complex (Business Logic + Validation) | **100 TCs**   | 22s  |
| Approval Flow    | Complex (Workflow + Permissions)      | **91 TCs**    | 20s  |

## 🧠 Core Strategies

### 1. Smart Schema Extraction

AI analyzes PRD and outputs structured JSON:

```json
{
  "feature_name": "User Registration",
  "sections": [
    {
      "name": "Personal Info",
      "fields": [
        {
          "name": "email",
          "type": "email",
          "required": true,
          "max_length": 100
        }
      ]
    }
  ],
  "business_rules": [...],
  "visual_rules": [...]
}
```

### 2. Matrix Engine Expansion

For each field, automatically generates:

1. **Validation**: Empty (if required), Min/Max Length/Value
2. **Format**: Invalid patterns, Edge cases (Unicode, Trim)
3. **Security**: XSS, SQLi, HTML/Command/Null Byte Injection
4. **Compatibility**: Chrome, Firefox, Safari, Edge, Mobile

**Example**: A single `email` field expands into **10+ test cases**.

### 3. Business Rule Conversion

Complex logic like "VAT = (Subtotal - Discount) \* 0.08" automatically becomes:

- Test with Discount = 0
- Test with Discount > Subtotal (edge case)
- Test rounding rules

## 📂 Project Structure

```
workflowtest/
├── input/              # Drop PRDs and Images here
├── output/             # Generated Test Cases & Schemas
├── test_gen/           # Core Engine
│   ├── main.py         # Orchestrator
│   ├── schema_models.py # Pydantic Models
│   ├── matrix_engine.py # Test Case Factory
│   ├── prompts.py      # AI Prompts
│   ├── validator.py    # Quality Gates
│   └── data_fuzzer.py  # Random Data Generation
├── docs/               # Rulesets and Best Practices
└── .agent/workflows/   # AWF Automation Scripts
```

## 🎯 Supported Field Types

### Input Fields (Forms)

- `text`, `password`, `textarea`, `email`, `number`
- `select`, `radio`, `checkbox`, `date`, `file`

### Display Elements (Dashboards)

- `chart` (Line, Bar, Donut)
- `table` (Data grids with sorting/pagination)
- `list` (Activity feeds, Notifications)
- `label` (Read-only text displays)

## 🛡️ Quality Gates

Every generated test suite is validated for:

- ✅ **Coverage**: 100% of PRD requirements mapped to test cases
- ✅ **Security**: XSS, SQLi, Injection vectors tested
- ✅ **Compatibility**: Browser/device coverage verified
- ✅ **Performance**: SLA checks included (if specified in PRD)

## 🤝 Contributing

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Built with [Antigravity AWF](https://deepmind.google/technologies/gemini/) (Advanced Agentic Workflow Framework)
- Test data generation powered by [Hypothesis](https://hypothesis.readthedocs.io/)
- Inspired by Pairwise Testing and BVA methodologies

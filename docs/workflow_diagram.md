# 🏗️ Test Generation Architecture (Smart Schema v5.0)

This document outlines the **Hybrid AI + Python** architecture used in the "Smart Schema" system. This approach combines the semantic understanding of Large Language Models (LLMs) with the deterministic precision of Python logic.

## 📐 Core Philosophy: "Architecht & Factory"

1.  **AI as the Architect (L1):**
    - **Role:** Analyzes unstructured input (PRD, Requirements).
    - **Goal:** Do _less_ generation, _more_ extraction.
    - **Output:** A strict `JSON Schema` defining variables, types, and constraints.
    - **Benefit:** Eliminates hallucinations by forcing structured output.

2.  **Python as the Factory (L2):**
    - **Role:** Takes the blueprint (Schema) and mass-produces test cases.
    - **Goal:** Apply rigorous testing algorithms (Boundary Value Analysis, Combinatorics).
    - **Output:** 100+ high-quality, executable test cases.
    - **Benefit:** Infinite scale, zero token cost for expansion.

---

## 🔄 System Data Flow

> [!NOTE]
> This diagram is written in **Mermaid.js**. If you cannot see the graph below, please install a Mermaid viewer (e.g., "Markdown Preview Mermaid Support" extension for VS Code).

```mermaid
graph TD
    %% Inputs
    User((User)) -->|PRD + Screen| Engine[Orchestrator]
    Engine -->|Input| Context{Context Builder}

    %% LAYER 1: The Brain (AI)
    subgraph "L1: KNOWLEDGE EXTRACTION (AI)"
        Context -->|Prompt: Extract Schema| AI_Arch{AI Architect}

        AI_Arch -->|JSON Schema| Schema("DATA SCHEMA\n{field: 'age', type: 'int', min:18}")

        style Schema fill:#ff9,stroke:#333
    end

    %% LAYER 2: The Factory (Python)
    subgraph "L2: MATRIX EXPANSION (Python)"
        Schema -->|Valid Models| Matrix[Matrix Engine]

        %% Expansion Logic
        Matrix -->|Rule: Integer| BVA[Boundary Value Analysis]
        Matrix -->|Rule: String| Sec[Security Payloads]
        Matrix -->|Rule: Enum|  Comb[Combinatorial]
        Matrix -->|Sanitize| Fuzz[Data Fuzzer]

        BVA & Sec & Comb & Fuzz --> GenCases[Generated Atomic Cases]
    end

    %% LAYER 3: Visual Intelligence
    subgraph "L3: VISUAL INTELLIGENCE"
        Engine -->|Image| EagleEye[Eagle Eye]
        EagleEye -->|UX Rules| VisualCases[Visual Test Cases]

        VisualCases --> Merger
        GenCases --> Merger
    end

    %% LAYER 4: Realization
    subgraph "L4: ASSEMBLY & VALIDATION"
        Merger{Merger} --> Builder[Markdown Builder]
        Builder --> FinalDoc[Final Doc]

        FinalDoc --> Validator{Quality Gate}
        Validator -->|Pass| Success((Done))
        Validator -->|Fail| Loop[Self-Correction]
    end

    %% Styles
    style AI_Arch fill:#f9f,stroke:#333
    style Matrix fill:#bbf,stroke:#333
```

## 📝 Workflow Execution Steps

### Phase 1: Knowledge Extraction (The Brain)

1.  **Input Analysis:** The **Orchestrator** reads the raw PRD (Markdown) and any UI screenshots.
2.  **Schema Extraction:** The **AI Architect** (Gemini) reads the PRD and extracts a strict JSON Schema.
    - _Example:_ Identifying that "User Age" is an integer between 18 and 100.
3.  **Validation:** `schema_models.py` validates the AI's output to ensure it matches the strict Pydantic models.

### Phase 2: Matrix Expansion (The Factory)

4.  **Mathematical Expansion:** The **Matrix Engine** takes the validated schema and applies testing algorithms:
    - **Boundary Analysis:** Generates tests for 17, 18, 19, 99, 100, 101.
    - **Combinatorics:** Generates all valid combinations of dropdowns/radio buttons.
    - **Security Injection:** Injects SQLi (`' OR 1=1`), XSS (`<script>`), and Overflow (1000+ chars) payloads.
5.  **Data Sanitization:** The **Data Fuzzer** ensures all generated test data is safe for Markdown tables (removes pipe characters, limits length).

### Phase 3: Visual Intelligence

6.  **Visual QA:** **Eagle Eye** analyzes the provided screenshot to generate UX/UI test cases (e.g., "Verify button color contrasts", "Check mobile responsiveness").

### Phase 4: Assembly & Validation

7.  **Merging:** Test cases from the Matrix Engine (Functional/Security) and Eagle Eye (Visual) are combined.
8.  **Formatting:** The **Markdown Builder** generates the final `tc_X.md` file.
9.  **Quality Gate:** The **Validator** checks the final output for formatting errors, duplicate IDs, or missing logic before presenting it to the user.

---

## 🛠 Component Map

| Component             | Responsibility                                                          | Status    |
| :-------------------- | :---------------------------------------------------------------------- | :-------- |
| `main.py`             | **Orchestrator**: Manages the flow between User, AI, and Matrix Engine. | ✅ Stable |
| `prompts.py`          | **Prompt Engineering**: Contains the `SCHEMA_EXTRACTION_PROMPT` for L1. | ✅ Stable |
| `schema_models.py`    | **Type Safety**: Pydantic models preventing invalid schemas.            | ✅ Stable |
| `matrix_engine.py`    | **Expansion Logic**: Implements BVA, pairwise, and security injection.  | ✅ Stable |
| `data_fuzzer.py`      | **Sanitization**: Hypothesis-based generator with markdown scrubbing.   | ✅ Stable |
| `visual_validator.py` | **Visual QA**: Eagle Eye module for UI/UX testing.                      | ✅ Stable |
| `validator.py`        | **Quality Gate**: Final check for formatting and consistency.           | ✅ Stable |

---

## 🚀 Key Advantages

| Feature         | Description                                                                   |
| :-------------- | :---------------------------------------------------------------------------- |
| **Determinism** | Python logic ensures that `Age > 18` _always_ generates 17, 18, 19.           |
| **Scalability** | Generating 1,000 test cases costs the same AI tokens as generating 10.        |
| **Security**    | Automatically injects SQLi, XSS, and Overflow payloads into every text field. |
| **Consistency** | Visual QA runs in parallel, ensuring UI/UX is not ignored.                    |

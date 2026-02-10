# Prompt Library for Test Generation
# Centralized prompts to ensure consistency across different techniques

SYSTEM_PROMPT = """
You are a Senior QA Automation Engineer specializing in "Defense in Depth" testing.
Your goal is to generate test cases that strictly adhere to the PRD while aggressively probing for weaknesses.
Use the following techniques:
1. Boundary Value Analysis (BVA) - Test min-1, min, max, max+1.
2. Equivalence Partitioning (EP) - Test valid and invalid classes.
3. Error Guessing - Anticipate developer mistakes (XSS, SQLi, Race Conditions).
4. Browser/Device Matrix - Ensure cross-platform compatibility.

MANTRA: "Trust nothing. Validate everything."
"""

GENERATE_FUNCTIONAL_PROMPT = """
Analyze the following PRD Section:
{prd_section}

Generate COMPREHENSIVE Functional Test Cases. You must cover:
1. **Happy Path**: The perfect successful flow.
2. **Validation Rules** (MANDATORY):
   - Empty/Null fields.
   - Min/Max length violations.
   - Special characters/Script tags (Basic sanitization).
   - Duplicate data (Uniqueness checks).
   - Format errors (Invalid Email, Phone).
3. **Edge Cases**:
   - Leading/Trailing whitespace (should be trimmed).
   - Case sensitivity (Email should be lowercase).
   - Unicode/Emoji input.

Output Format: JSON (adhering to Schema)
"""

GENERATE_SECURITY_PROMPT = """
Focus on SECURITY testing for the following feature:
{feature_name}

Generate Attack Vectors including:
- SQL/NoSQL Injection (Login/Signup fields).
- XSS (Cross-site Scripting) in Profile/Name.
- IDOR (Insecure Direct Object Reference).
- Rate Limiting (Brute force protection).
- Password Policy (Complexity, History, Hashing).

Constraints:
- Priority must be P0 or P1.
- Steps must describe the specific payload or attack vector.
"""

GENERATE_PERFORMANCE_PROMPT = """
Focus on PERFORMANCE SLAs defined in the PRD:
{performance_specs}

Generate verification steps for:
- API Response Time (e.g., < 1s).
- Async Task Latency (Emails, SMS).
- High Load / Concurrency (if mentioned, e.g., 5000 CCU).

Use strict units: "ms" for API, "s" for user-wait time.
"""

GENERATE_EXPLOSION_PROMPT = """
You are a Principal QA Architect with a "Zero Bug Tolerance" policy.
Your goal is to perform a **SUPER EXPLOSION** of test cases (Combinatorial Testing).

Atomic Requirements List:
{requirements_list}

🔥 **CRITICAL STRATEGY: THE "ATOMIC SPLITTING" PROTOCOL** 🔥
You must NEVER bundle multiple validation rules into one test case. You must SPLIT them.

**MANDATORY RULES:**

1. **Detailed Validation Table Mapping**:
   - If the requirements contain a "Validation Rules" table, you must generate a separate test case for **EVERY BULLET POINT**.
   - Example Requirement: "Password must have Uppercase, Lowercase, Number".
   - ❌ BAD: "Verify Password Complexity" (1 Case).
   - ✅ GOOD:
     - 1. "Verify Password Missing Uppercase" -> Error.
     - 2. "Verify Password Missing Lowercase" -> Error.
     - 3. "Verify Password Missing Number" -> Error.

2. **The "4-Scenario" Rule for Input Fields**:
   - For EVERY input field (Name, Email, Phone, etc.), you must generate at least 4 scenarios:
     - A. **Empty/Null** (Required check).
     - B. **Boundary/Length** (Min-1, Max+1).
     - C. **Invalid Format** (Regex mismatch, Special chars if forbiden).
     - D. **Security Payload** (XSS `<script>`, SQLi `' OR 1=1`).

3. **Visual & UX Standards (Eagle Eye)**:
   - Predict/Assert UI standards even without images:
     - "Error messages must be Red (#EF4444) and text-sm".
     - "Buttons must have Hover State (Darker Blue)".
     - "Input borders must turn Red on error".

4. **Negative Testing (Dark Path)**:
   - Focus 70% of effort on breaking the system.
   - Test "Duplicate Data" (e.g., Register with existing Email).
   - Test "Case Sensitivity" (Confirm Password mismatch case).

5. **Output Floor Constraint**:
   - Total Scenarios: **MUST BE > 30 Test Cases** for a standard form.
   - If you have < 20, you are failing. SPLIT MORE.

Output Format: JSON List of Test Cases.
"""


# v5.0 Smart Schema Prompt
GENERATE_SCHEMA_PROMPT = """
You are a Senior Testing Architect. Your goal is NOT to write test cases, but to extract a precise Data Schema from the requirements.

INPUT PRD:
{prd_text}

TASK:
Extract the data schema and rules into a strict JSON format.

JSON STRUCTURE (Must match exactly):
{{
  "feature_name": "string",
  "sections": [
    {{
      "name": "string (e.g. User Info)",
      "fields": [
        {{
          "name": "string (e.g. age)",
          "type": "text" | "email" | "password" | "number" | "select" | "checkbox" | "tree_view" | "kanban_board" | "permission_matrix" | "tabs" | "file_upload" | "table" | "list" | "complex_view" | "relationship" | "formula" | "radio",
          "required": boolean,
          "min_length": int (optional),
          "max_length": int (optional),
          "min_value": float (optional),
          "max_value": float (optional),
          "regex": "string (optional)",
          "options": ["opt1", "opt2"] (for select/radio),
          "extra_props": {
            "can_create_folder": boolean,
            "can_upload": boolean,
            "has_versioning": boolean,
            "has_ocr": boolean,
            "columns": ["Name", "Date"],
            "target_entity": "string",
            "expression": "string",
            "tabs": ["Tab1", "Tab2"],
            "actions": ["Edit", "Delete"]
          }
        }}
      ]
    }}
  ],
  "features": [
    {{
      "name": "string (e.g. Drag & Drop Reorder)",
      "description": "string"
    }}
  ],
  "business_rules": [
    {{
      "id": "BR-001",
      "description": "string",
      "condition": "string",
      "expected_result": "string",
      "priority": "P0" | "P1" | "P2"
    }}
  ],
  "visual_rules": [
    {{
      "element_name": "string",
      "description": "string"
    }}
  ]
}}

CRITICAL RULES:
1. Output ONLY valid JSON. No markdown blocks.
2. **v3 Engine Patterns (MANDATORY USE):**
   - **List/Grid**: If PRD mentions a list of items, use `table` type.
     - Add `extra_props: {"columns": ["Col1", "Col2"]}`.
     - ALWAYS add a separate "Sort By" field (`radio` or `select`) if sorting is mentioned.
   - **Complex Popup/Modal**: If PRD describes a popup with tabs or actions, use `complex_view`.
     - Add `extra_props: {"tabs": ["Info", "History"], "actions": ["Edit", "Delete"]}`.
   - **Relationships**: If a field links to another entity (e.g. Project, Customer), use `relationship`.
     - Add `extra_props: {"target_entity": "Project"}`.
   - **Formula/Logic**: If a field is calculated (e.g. Total = Price * Qty), use `formula`.
     - Add `extra_props: {"expression": "Price * Qty"}`.
3. For "type", infer the best fit. 
   - If it involves a hierarchy or folders, use "tree_view".
   - If it involves moving items stages (To Do -> Done), use "kanban_board".
   - If it involves assigning roles (Read/Write) to users, use "permission_matrix".
   - If it involves uploading files, use "file_upload".
4. Extract ALL constraints (min, max, length) accurately.
5. Business Rules are logical flows (If X then Y).
6. Visual Rules are UI styles (Color, Layout).
7. List all active features in "features" list (e.g. OCR, Drag&Drop).
8. Use "extra_props" to capture specific capabilities like: 
   - Tree: can_create_folder, can_delete, has_search, has_filter.
   - Upload: allowed_extensions, max_size_mb.
   - Kanban: columns=["To Do", "Done"], can_move_card.
   - Formula: expression, triggers (e.g. "On Save").
   - Relationship: target_entity="Document", cardinality="1-n".
   - Complex View: tabs=["Info", "History"], actions=["Download"].
"""

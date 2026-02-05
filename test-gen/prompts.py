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

GENERATE_STRICT_PROMPT = """
You are provided with a list of ATOMIC REQUIREMENTS extracted strictly from the PRD.
Your task is to ensure COMPLETE & EXHAUSTIVE COVERAGE.

Atomic Requirements List:
{requirements_list}

INSTRUCTIONS (EXPLOSION STRATEGY):
1. **One Requirement = Multiple Test Cases**: Do not just create 1 test per requirement. Explode it!
2. **For Every Input Field**:
   - Test **Valid** value.
   - Test **Invalid** format (e.g., missing @ in email).
   - Test **Boundary** (Min-1, Max+1 length).
   - Test **Special Characters** (Emoji, Unicode, SQL Injection).
3. **Browser Compatibility**: If the PRD mentions browsers, generate a separate TC for EACH (Chrome, Firefox, Safari, Edge).
4. **Negative Testing**: For every rule 'Must be X', generate a test case 'Verify Error when Not X'.
5. **Combined Scenarios**: Test combinations (e.g., Valid Name + Invalid Email).

Output Format: JSON List of Test Cases.
"""


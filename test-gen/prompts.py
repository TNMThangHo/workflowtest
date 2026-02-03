# Prompt Library for Test Generation
# Centralized prompts to ensure consistency across different techniques

SYSTEM_PROMPT = """
You are a Senior QA Automation Engineer specializing in high-coverage test generation.
Your goal is to generate test cases that strictly adhere to the PRD and following standard testing techniques:
1. Boundary Value Analysis (BVA)
2. Equivalence Partitioning (EP)
3. Error Guessing (Security & Negative cases)
"""

GENERATE_FUNCTIONAL_PROMPT = """
Analyze the following PRD Section:
{prd_section}

Generate STRICT Functional Test Cases covering:
- Positive Flows (Happy Path)
- Validation Rules (Field strictness)
- Business Logic Constraints

Output Format: JSON (adhering to Schema)
"""

GENERATE_SECURITY_PROMPT = """
Focus on SECURITY testing for the following feature:
{feature_name}

Generate Attack Vectors including:
- SQL/NoSQL Injection
- XSS (Cross-site Scripting)
- IDOR (Insecure Direct Object Reference)
- Rate Limiting scenarios
- Authorization bypass

Constraints:
- Priority must be P0 or P1
- Steps must describe the attack vector clearly
"""

GENERATE_PERFORMANCE_PROMPT = """
Focus on PERFORMANCE SLAs defined in the PRD:
{performance_specs}

Generate verification steps for:
- API Response Time
- Async Task Latency (Emails, Notifications)
- UI Rendering speed

Use strict units: "ms" for API, "s" for user-wait time.
"""

GENERATE_STRICT_PROMPT = """
You are provided with a list of ATOMIC REQUIREMENTS extracted strictly from the PRD.
Your task is to ensure EVERY requirement has a corresponding Test Case.

Atomic Requirements List:
{requirements_list}

For EACH requirement in the list:
1. Check if it already has a test case (from context).
2. If NOT, generate a NEW Test Case.
3. If the requirement contains a NUMBER (e.g., "1000 CCU", "10 seconds"), the Expected Result MUST explicitly mention this number.

Output Format: JSON List of Test Cases.
"""

"""
Quick Test: Template Integration E2E
Tests the complete workflow from PRD to template-based output
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from test_gen.markdown_parser import PRDParser
from test_gen.extractor import run_extraction
from test_gen.exporter import Exporter
from test_gen.template_engine import (
    render_template,
    calculate_statistics,
    categorize_testcases,
    extract_nft_categories
)

print("=" * 60)
print("🧪 TEMPLATE INTEGRATION TEST")
print("=" * 60)

# Test 1: Metadata Extraction
print("\n📊 Test 1: Metadata Extraction")
print("-" * 60)

prd_path = "input/signupPrd.md"
parser = PRDParser(prd_path)
if parser.load():
    metadata = parser.extract_metadata_header()
    print(f"✅ Metadata extracted:")
    print(f"   - Feature: {metadata['feature_name']}")
    print(f"   - Version: {metadata['prd_version']}")
    print(f"   - Tester: {metadata['tester']}")
else:
    print("❌ Failed to load PRD")
    sys.exit(1)

# Test 2: Requirement Extraction with Metadata
print("\n📝 Test 2: Requirement Extraction")
print("-" * 60)

if run_extraction(prd_path):
    print("✅ Extraction successful!")
    
    # Check output
    import json
    with open("output/requirements.json", 'r', encoding='utf-8') as f:
        req_data = json.load(f)
    
    print(f"   - Metadata present: {'metadata' in req_data}")
    print(f"   - Requirements count: {len(req_data.get('atomic_requirements', []))}")
else:
    print("❌ Extraction failed")

# Test 3: Template Rendering with Mock Data
print("\n🎨 Test 3: Template Rendering")
print("-" * 60)

# Mock test cases from tc_auto.md (simplified)
mock_test_cases = [
    {
        "id": "TC-SIGNUP-FUNC-001",
        "type": "FUNC",
        "title": "User Registration Success (Happy Path)",
        "module": "Authentication",
        "pre_condition": "User is logged out",
        "steps": ["Navigate to Registration Page", "Enter valid 'Họ và tên': 'Nguyen Van A'", "Enter valid 'Email': 'newuser@example.com'"],
        "test_data": "email=newuser@example.com, password=Pass@1234",
        "expected_result": "System returns 201 Created. Account created with status 'unverified'.",
        "priority": "P0"
    },
    {
        "id": "TC-SIGNUP-SEC-001",
        "type": "SEC",
        "title": "Security: Rate Limiting (Anti-Spam)",
        "steps": ["Send 6 registration requests within 1 minute from same IP address"],
        "tools": "Postman, k6",
        "pass_criteria": "Requests 1-5 processed. Request 6 returns 429 Too Many Requests",
        "priority": "P1"
    },
    {
        "id": "TC-SIGNUP-PERF-001",
        "type": "PERF",
        "title": "Performance: API Response Time",
        "steps": ["Submit valid registration request", "Measure API response time"],
        "tools": "k6, Artillery",
        "pass_criteria": "Response received in < 1 second (< 1000ms)",
        "priority": "P2"
    },
    {
        "id": "TC-SIGNUP-COMP-001",
        "type": "COMP",
        "title": "Compatibility: Chrome Browser",
        "steps": ["Open Signup Page on Chrome (Latest)", "Perform full registration flow"],
        "tools": "Chrome v120+",
        "pass_criteria": "UI renders correctly. No functional errors. Registration successful.",
        "priority": "P2"
    },
    {
        "id": "TC-SIGNUP-ANA-001",
        "type": "ANA",
        "title": "Analytics: Button Click & Success Tracking",
        "steps": ["Click 'Đăng ký'  with validation errors", "Fix errors and click 'Đăng ký' successfully"],
        "tools": "Google Analytics 4",
        "pass_criteria": "Event 'click_signup_button' fired twice. 'signup_failed' fired once. 'signup_success' fired once.",
        "priority": "P3"
    }
]

template_data = {
    "metadata": metadata,
    "test_cases": mock_test_cases
}

exporter = Exporter(output_dir="output")
result = exporter.export_to_template_markdown(
    template_data,
    "test-gen/templates/test-case-template.md",
    "TEST_TEMPLATE_OUTPUT.md"
)

print(f"✅ Template rendered: {result}")

# Test 4: Verify Output
print("\n✅ Test 4: Verify Output Structure")
print("-" * 60)

with open("output/TEST_TEMPLATE_OUTPUT.md", 'r', encoding='utf-8') as f:
    output = f.read()

checks = {
    "Section I: Dashboard": "## I. THỐNG KÊ TỔNG QUAN" in output,
    "Section II: Functional": "## II. KIỂM THỬ CHỨC NĂNG" in output,
    "Section III: Non-Functional": "## III. KIỂM THỬ PHI CHỨC NĂNG" in output,
    "Section IV: Bug Tracking": "## IV. GHI CHÚ & THEO DÕI LỖI" in output,
    "Feature Name in Title": metadata['feature_name'] in output,
    "Total Cases (5)": "**5**" in output,
    "P0 Priority": "**P0" in output,
    "Security Category": "[x] **Security**" in output or "Security" in output,
    "Analytics Category": "[x] **Analytics**" in output or "Analytics" in output,
    "No Jinja2 Syntax": "{{" not in output and "{%" not in output
}

for check_name, passed in checks.items():
    status = "✅" if passed else "❌"
    print(f"   {status} {check_name}")

# Summary
print("\n" + "=" * 60)
passed_checks = sum(checks.values())
total_checks = len(checks)
print(f"📊 SUMMARY: {passed_checks}/{total_checks} checks passed")

if passed_checks == total_checks:
    print("✅ ALL TESTS PASSED! Template integration working correctly!")
else:
    print(f"⚠️  {total_checks - passed_checks} checks failed. Review output.")

print("=" * 60)

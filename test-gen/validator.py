import re
import sys
import json
from typing import Dict, List, Set, Optional
from .logger import log
from .schema import TestSuite, TestCase

class TestCaseValidator:
    def __init__(self, prd_content: str, test_suite: TestSuite):
        self.prd_content = prd_content
        self.test_suite = test_suite
        self.issues: List[Dict] = []
        self.warnings: List[Dict] = []

    def extract_performance_requirements(self) -> Dict:
        """Extract performance SLAs from PRD"""
        requirements = {}
        # API check
        api_match = re.search(r'API.*?đăng ký.*?[<\u003c]\s*(\d+)\s*(giây|s|second)', self.prd_content, re.IGNORECASE)
        if api_match:
            requirements['api_response_seconds'] = int(api_match.group(1))
        
        # Email check
        email_match = re.search(r'Email.*?trong vòng\s*(\d+)\s*giây', self.prd_content, re.IGNORECASE)
        if email_match:
            requirements['email_delivery_seconds'] = int(email_match.group(1))
            
        return requirements

    def extract_browser_requirements(self) -> Set[str]:
        """Extract browser compatibility requirements from PRD"""
        browsers = set()
        # Simple extraction based on keywords found near "trình duyệt" or "browser"
        match = re.search(r'(trình duyệt|browser).*?:(.*?)[\n\r]', self.prd_content, re.IGNORECASE)
        if match:
            text = match.group(2).lower()
            for b in ['chrome', 'firefox', 'safari', 'edge', 'opera']:
                if b in text:
                    browsers.add(b.capitalize())
        return browsers

    def validate_structure(self):
        """Check if IDs and fields follow rules"""
        for tc in self.test_suite.test_cases:
            if not tc.id.startswith("TC-"):
                self.issues.append({"type": "INVALID_ID", "id": tc.id, "msg": "ID must start with TC-"})
            if not tc.priority in ["P0", "P1", "P2", "P3"]:
                self.warnings.append({"type": "INVALID_PRIORITY", "id": tc.id, "msg": f"Priority {tc.priority} is unusual"})

    def validate_performance(self):
        """Validate Performance Limit matches"""
        reqs = self.extract_performance_requirements()
        
        # Check API
        if 'api_response_seconds' in reqs:
            expected_ms = reqs['api_response_seconds'] * 1000
            found = False
            for tc in self.test_suite.test_cases:
                if tc.type == "Performance" and "API" in tc.title:
                    found = True
                    # Check for "1000ms" or "1s"
                    match = re.search(r'(\d+)\s*(ms|s)', tc.expected_result)
                    if match:
                        val = int(match.group(1))
                        unit = match.group(2)
                        actual_ms = val if unit == 'ms' else val * 1000
                        if actual_ms != expected_ms:
                             self.issues.append({
                                "type": "PERFORMANCE_MISMATCH",
                                "id": tc.id,
                                "expected": f"{expected_ms}ms",
                                "actual": f"{actual_ms}ms"
                            })
            if not found:
                 self.warnings.append({"type": "MISSING_TEST", "msg": "No API Performance test found"})

    def validate_browsers(self):
        """Review Browser Coverage"""
        required_browsers = self.extract_browser_requirements()
        covered_browsers = set()
        
        for tc in self.test_suite.test_cases:
            # Check title for browser name
            for b in required_browsers:
                if b in tc.title:
                    covered_browsers.add(b)
        
        missing = required_browsers - covered_browsers
        if missing:
             self.issues.append({
                "type": "MISSING_BROWSER",
                "browsers": list(missing)
            })

    def validate(self):
        log.info("🔍 Running Validations...")
        self.validate_structure()
        self.validate_performance()
        self.validate_browsers()
        
        if self.issues:
            log.error(f"❌ Found {len(self.issues)} issues.")
            for i in self.issues:
                log.error(f"  - {i}")
            return False
        
        if self.warnings:
            log.warning(f"⚠️ Found {len(self.warnings)} warnings.")
            for w in self.warnings:
                log.warning(f"  - {w}")
        
        log.info("✅ All Validations Passed.")
        return True

def run_validate(prd_path, testcases_path):
    # Load PRD
    try:
        with open(prd_path, 'r', encoding='utf-8') as f:
            prd_text = f.read()
    except Exception as e:
        log.error(f"Could not read PRD: {e}")
        return False

    # Load Test Cases
    try:
        # Try JSON first (intermediate)
        if testcases_path.endswith('.json'):
            suite = TestSuite.from_json_file(testcases_path)
        else:
             # Markdown parsing not fully implemented in schema yet, assuming JSON input for validation for now
             # Or we need a partial parser for MD. 
             # Given the flow -> raw_testcases.json is key.
             log.warning("Validator currently prefers JSON input for strict checking.")
             return False
    except Exception as e:
        log.error(f"Could not load Test Cases: {e}")
        return False

    validator = TestCaseValidator(prd_text, suite)
    return validator.validate()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--prd', required=True)
    parser.add_argument('--testcases', required=True)
    args = parser.parse_args()
    
    success = run_validate(args.prd, args.testcases)
    sys.exit(0 if success else 1)

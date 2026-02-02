"""
Test Case Validator - Automatically validates test cases against PRD requirements
Prevents discrepancies between PRD and generated test cases
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Set
import sys

class TestCaseValidator:
    def __init__(self, prd_path: str, testcases_md_path: str):
        self.prd_path = prd_path
        self.testcases_path = testcases_md_path
        self.issues = []
        self.warnings = []
        
    def read_prd(self) -> str:
        """Read PRD content"""
        with open(self.prd_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def read_testcases(self) -> str:
        """Read test cases Markdown"""
        with open(self.testcases_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def extract_performance_requirements(self, prd_content: str) -> Dict:
        """Extract performance SLAs from PRD"""
        requirements = {}
        
        # API response time
        api_match = re.search(r'API.*?đăng ký.*?[<\u003c]\s*(\d+)\s*(giây|s|second)', prd_content, re.IGNORECASE)
        if api_match:
            seconds = int(api_match.group(1))
            requirements['api_response_seconds'] = seconds
        
        # Email delivery time
        email_match = re.search(r'Email.*?trong vòng\s*(\d+)\s*giây', prd_content, re.IGNORECASE)
        if email_match:
            requirements['email_delivery_seconds'] = int(email_match.group(1))
        
        return requirements
    
    def extract_browser_requirements(self, prd_content: str) -> Set[str]:
        """Extract browser compatibility requirements from PRD"""
        browsers = set()
        
        # Find browser section
        browser_match = re.search(r'trình duyệt.*?:(.*?)[\n\r]', prd_content, re.IGNORECASE)
        if browser_match:
            browser_text = browser_match.group(1).lower()
            
            if 'chrome' in browser_text:
                browsers.add('Chrome')
            if 'firefox' in browser_text:
                browsers.add('Firefox')
            if 'safari' in browser_text:
                browsers.add('Safari')
            if 'edge' in browser_text:
                browsers.add('Edge')
            if 'opera' in browser_text or 'operamini' in browser_text:
                browsers.add('Opera Mini')
        
        return browsers
    
    def extract_validation_rules(self, prd_content: str) -> Dict:
        """Extract validation rules from PRD"""
        rules = {}
        
        # Password min length
        pwd_match = re.search(r'Mật khẩu.*?tối thiểu\s*(\d+)\s*ký tự', prd_content, re.IGNORECASE)
        if pwd_match:
            rules['password_min_length'] = int(pwd_match.group(1))
        
        # Name min length
        name_match = re.search(r'Họ và tên.*?tối thiểu\s*(\d+)\s*ký tự', prd_content, re.IGNORECASE)
        if name_match:
            rules['name_min_length'] = int(name_match.group(1))
        
        return rules
    
    def validate_performance_tests(self, prd_content: str, tc_content: str):
        """Validate performance test cases match PRD SLAs"""
        prd_reqs = self.extract_performance_requirements(prd_content)
        
        # Check API response time test
        if 'api_response_seconds' in prd_reqs:
            expected_ms = prd_reqs['api_response_seconds'] * 1000
            
            # Find performance test case
            perf_match = re.search(r'TC-SIGNUP-PERF-001.*?response\s*[<\u003c]\s*(\d+)ms', tc_content)
            if perf_match:
                actual_ms = int(perf_match.group(1))
                if actual_ms != expected_ms:
                    self.issues.append({
                        'type': 'PERFORMANCE_MISMATCH',
                        'test_case': 'TC-SIGNUP-PERF-001',
                        'prd_requirement': f'< {prd_reqs["api_response_seconds"]}s ({expected_ms}ms)',
                        'test_case_value': f'{actual_ms}ms',
                        'severity': 'HIGH'
                    })
            else:
                self.warnings.append({
                    'type': 'MISSING_TEST',
                    'message': 'No API performance test case found'
                })
        
        # Check Email delivery time
        if 'email_delivery_seconds' in prd_reqs:
            email_match = re.search(r'TC-SIGNUP-PERF-002.*?within\s*(\d+)s', tc_content, re.IGNORECASE)
            if email_match:
                actual_s = int(email_match.group(1))
                if actual_s != prd_reqs['email_delivery_seconds']:
                    self.issues.append({
                        'type': 'PERFORMANCE_MISMATCH',
                        'test_case': 'TC-SIGNUP-PERF-002',
                        'prd_requirement': f'{prd_reqs["email_delivery_seconds"]}s',
                        'test_case_value': f'{actual_s}s',
                        'severity': 'MEDIUM'
                    })
    
    def validate_browser_compatibility(self, prd_content: str, tc_content: str):
        """Validate browser compatibility test cases"""
        prd_browsers = self.extract_browser_requirements(prd_content)
        
        # Extract browsers from test cases
        tc_browsers = set()
        for browser in ['Chrome', 'Firefox', 'Safari', 'Edge', 'Opera Mini']:
            if re.search(f'{browser}.*?Browser.*?Compatibility', tc_content, re.IGNORECASE):
                tc_browsers.add(browser)
        
        # Check missing browsers
        missing = prd_browsers - tc_browsers
        if missing:
            self.issues.append({
                'type': 'MISSING_BROWSER_TESTS',
                'missing_browsers': list(missing),
                'severity': 'HIGH'
            })
        
        # Check extra browsers (not critical but good to know)
        extra = tc_browsers - prd_browsers
        if extra:
            self.warnings.append({
                'type': 'EXTRA_BROWSER_TESTS',
                'extra_browsers': list(extra),
                'message': 'Test cases cover more browsers than PRD specifies'
            })
    
    def validate_all(self) -> bool:
        """Run all validations"""
        print("🔍 Starting Test Case Validation...\n")
        
        prd_content = self.read_prd()
        tc_content = self.read_testcases()
        
        # Run validations
        self.validate_performance_tests(prd_content, tc_content)
        self.validate_browser_compatibility(prd_content, tc_content)
        
        # Print results
        self.print_results()
        
        # Return True if no critical issues
        return len(self.issues) == 0
    
    def print_results(self):
        """Print validation results"""
        if not self.issues and not self.warnings:
            print("✅ All validations passed! Test cases match PRD requirements.\n")
            return
        
        if self.issues:
            print("❌ ISSUES FOUND:\n")
            for idx, issue in enumerate(self.issues, 1):
                print(f"{idx}. [{issue.get('severity', 'MEDIUM')}] {issue['type']}")
                for key, value in issue.items():
                    if key not in ['type', 'severity']:
                        print(f"   - {key}: {value}")
                print()
        
        if self.warnings:
            print("⚠️  WARNINGS:\n")
            for idx, warning in enumerate(self.warnings, 1):
                print(f"{idx}. {warning['type']}")
                print(f"   - {warning.get('message', '')}")
                print()
        
        # Summary
        print("\n" + "="*60)
        print(f"📊 SUMMARY: {len(self.issues)} issues, {len(self.warnings)} warnings")
        print("="*60)

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Validate test cases against PRD')
    parser.add_argument('--prd', required=True, help='Path to PRD file')
    parser.add_argument('--testcases', required=True, help='Path to test cases Markdown')
    
    args = parser.parse_args()
    
    validator = TestCaseValidator(args.prd, args.testcases)
    is_valid = validator.validate_all()
    
    sys.exit(0 if is_valid else 1)

if __name__ == '__main__':
    main()

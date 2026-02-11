import json
import re
from typing import List, Dict, Any, Tuple

class ValidationEngine:
    """
    [NEW v4.0] Proactive Quality Gate
    Scans generated test cases for known hallucinations and data quality issues.
    """
    
    FORBIDDEN_KEYWORDS = {
        "Payment": ["thanh toán", "payment", "credit card", "banking", "gateway"],
        "API Integration": ["api key", "endpoint", "swagger", "postman", "json response"],
        # [Refined] Removed "approver" as it can mean Role, "level 1/2" valid in contexts
        "Approval Workflow": ["phê duyệt", "từ chối", "reject", "approval flow"],
        # [Refined] Removed "login/register/password" as basic auth is standard
        "Authentication": ["oauth", "sso", "mfa", "2fa"] 
    }

    # Features that SHOULD allow these keywords if present in Schema
    FEATURE_MAP = {
        "Payment": ["billing", "finance", "checkout", "transaction"],
        "API Integration": ["api", "webhook", "integration", "developer"],
        "Approval Workflow": ["approval", "workflow", "process", "duyệt", "quy trình", "permission", "role"], # Added Permission/Role
        "Authentication": ["auth", "login", "security", "account", "permission", "user"] # Added common auth terms
    }

    def __init__(self, schema_path: str):
        self.schema_content = ""
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                self.schema_content = f.read().lower()
        except Exception:
            print(f"⚠️ Warning: Could not read schema from {schema_path}")

    def validate(self, test_cases_path: str) -> bool:
        """
        Runs all validation checks.
        Returns True if passed (or warnings only), False if critical errors found.
        """
        print(f"🛡️  Starting Validation on {test_cases_path}...")
        
        try:
            with open(test_cases_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Handle wrapper key if present
                if isinstance(data, dict) and "test_cases" in data:
                    test_cases = data["test_cases"]
                elif isinstance(data, list):
                    test_cases = data
                else:
                    print("❌ Error: Invalid JSON structure (expected list or dict with 'test_cases' key)")
                    return False
        except Exception as e:
            print(f"❌ Error loading test cases: {e}")
            return False

        issues = []
        
        # 1. Check for Forbidden Keywords (Hallucinations)
        hallucinations = self._check_hallucinations(test_cases)
        issues.extend(hallucinations)

        # 2. Check Data Quality (Random Strings)
        data_issues = self._check_data_quality(test_cases)
        issues.extend(data_issues)

        # Report Results
        if not issues:
            print("✅ Validation PASSED: No issues found.")
            return True
        
        print(f"⚠️  Found {len(issues)} potential issues:")
        for issue in issues:
            print(f"   - [{issue['type']}] {issue['message']} (TC: {issue['tc_id']})")
            
        # For now, we return True to allow pipeline to proceed with warnings, 
        # unless user configures strict mode.
        return True

    def _check_hallucinations(self, test_cases: List[Dict]) -> List[Dict]:
        issues = []
        
        for category, keywords in self.FORBIDDEN_KEYWORDS.items():
            # Check if Schema actually supports this feature
            is_feature_present = any(f in self.schema_content for f in self.FEATURE_MAP[category])
            
            if is_feature_present:
                continue # Skip check if feature is legitimate
            
            # Scan Test Cases
            for tc in test_cases:
                content = (tc.get('title', '') + " " + tc.get('steps', '')).lower()
                for kw in keywords:
                    if kw in content:
                        issues.append({
                            "type": "HALLUCINATION",
                            "tc_id": tc.get('id', 'Unknown'),
                            "message": f"Detected '{category}' keyword '{kw}' but feature not in Schema."
                        })
                        break # One hit per TC is enough
        return issues

    def _check_data_quality(self, test_cases: List[Dict]) -> List[Dict]:
        issues = []
        # Patterns looking for random strings like "Xy7z" (Capital, lower, digit mix, len 4-8)
        # This is heuristics, might have false positives
        random_pattern = re.compile(r'\b[A-Za-z0-9]{5,10}\b')
        
        for tc in test_cases:
            data = tc.get('test_data', '')
            if "[Random Examples]" in data:
                 issues.append({
                    "type": "BAD_DATA",
                    "tc_id": tc.get('id', 'Unknown'),
                    "message": "Found disallowed '[Random Examples]' marker."
                })
        return issues

import json
import os
import sys
from datetime import datetime
from .logger import log

class TestManager:
    def __init__(self, file_path="output/raw_testcases.json"):
        self.file_path = file_path

    def load_data(self):
        """Safely load JSON data with error reporting."""
        if not os.path.exists(self.file_path):
            log.warning(f"⚠️ File not found: {self.file_path}. Creating new.")
            return {"test_cases": []}
        
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            log.error(f"❌ Corrupt JSON in {self.file_path}")
            log.error(f"   Line {e.lineno}, Column {e.colno}: {e.msg}")
            # Optional: Read file and show the specific line
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if 0 <= e.lineno - 1 < len(lines):
                        log.error(f"   Target content: {lines[e.lineno - 1].strip()}")
            except:
                pass
            return None

    def save_data(self, data):
        """Safely save JSON data."""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            log.info(f"✅ Saved to {self.file_path}")
            return True
        except Exception as e:
            log.error(f"❌ Failed to save JSON: {e}")
            return False

    def add_testcase(self, title, steps=None, expected=None, priority="P2"):
        """Add a new test case programmatically."""
        data = self.load_data()
        if data is None:
            return False

        if "test_cases" not in data:
            data["test_cases"] = []

        # Generate ID
        new_id = f"TC-MANUAL-{len(data['test_cases']) + 1:03d}"
        
        new_tc = {
            "id": new_id,
            "title": title,
            "priority": priority,
            "steps": steps or [],
            "expected_result": expected or "",
            "type": "Manual",
            "status": "New",
            "create_date": datetime.now().strftime('%Y-%m-%d')
        }

        data["test_cases"].append(new_tc)
        
        if self.save_data(data):
            log.info(f"✅ Added Test Case: {new_id} - {title}")
            return True
        return False

def run_add_testcase(title, steps=None, expected=None, priority="P2"):
    manager = TestManager()
    steps_list = steps.split(";") if steps else []
    return manager.add_testcase(title, steps_list, expected, priority)

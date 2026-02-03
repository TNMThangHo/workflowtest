import re
from typing import List, Dict, Optional
from pathlib import Path
from .logger import log

class PRDParser:
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.content = ""
        self.metadata = {}
        self.sections = {}

    def load(self):
        """Load file content"""
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                self.content = f.read()
            return True
        except Exception as e:
            log.error(f"Failed to load PRD file: {e}")
            return False

    def parse_metadata(self):
        """Extract metadata table often found at the beginning"""
        # Metadata often in | Key | Value | format
        meta_pattern = r'\|\s*\*\*?(.*?)\*\*?\s*\|\s*(.*?)\s*\|'
        matches = re.findall(meta_pattern, self.content)
        for key, value in matches:
            clean_key = key.strip().replace("**", "").lower()
            clean_val = value.strip()
            # Ignore table headers
            if "---" in clean_key or "chi tiết" in clean_key:
                continue
            self.metadata[clean_key] = clean_val
        
        log.info(f"Parsed {len(self.metadata)} metadata items.")

    def extract_regex_requirements(self) -> Dict[str, str]:
        """Attempt to find regex or format rules"""
        rules = {}
        # Example: Email ... regex standard
        if "email" in self.content.lower():
             rules["email"] = "standard_email_regex"
        return rules

    def get_full_content(self) -> str:
        return self.content

    def run(self):
        if self.load():
            self.parse_metadata()
            return True
        return False

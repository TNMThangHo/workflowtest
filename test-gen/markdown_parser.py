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

    def extract_metadata_header(self) -> dict:
        """
        Extract metadata from PRD header (first 15-20 lines)
        
        Expected format:
        **Feature:** User Signup
        **Phiên bản:** 1.0.0
        **Người thực hiện:** Nguyễn Văn A
        
        Or variation:
        - **Feature:** ...
        - **Version:** ...
        - **Tester:** ...
        
        Returns:
            Dictionary with feature_name, prd_version, tester
        """
        metadata = {
            'feature_name': 'Test Cases',  # Default
            'prd_version': '1.0.0',
            'tester': 'QA Team'
        }
        
        if not self.content:
            return metadata
        
        # Read first 20 lines
        lines = self.content.split('\n')[:20]
        
        for line in lines:
            line_lower = line.lower()
            
            # Feature/Tính năng
            if '**feature:**' in line_lower or '**tính năng:**' in line_lower:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    metadata['feature_name'] = parts[1].strip().replace('**', '')
            
            # Version/Phiên bản
            elif '**phiên bản:**' in line_lower or '**version:**' in line_lower:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    metadata['prd_version'] = parts[1].strip().replace('**', '')
            
            # Tester/Người thực hiện
            elif '**người thực hiện:**' in line_lower or '**tester:**' in line_lower or '**qa:**' in line_lower:
                parts = line.split(':', 1)
                if len(parts) > 1:
                    metadata['tester'] = parts[1].strip().replace('**', '')
        
        log.info(f"Extracted metadata: feature='{metadata['feature_name']}', version='{metadata['prd_version']}', tester='{metadata['tester']}'")
        return metadata

    def get_full_content(self) -> str:
        return self.content

    def run(self):
        if self.load():
            self.parse_metadata()
            return True
        return False

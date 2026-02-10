import re
import json
from .logger import log

class RequirementExtractor:
    def __init__(self, content):
        self.content = content
        self.requirements = []

    def extract_atomic(self):
        """
        Break down PRD content into atomic requirements.
        Focuses on sentences containing:
        - Numbers (SLAs, limits)
        - Start keywords (Must, Shall, Required, Tuyệt đối, Bắt buộc)
        """
        log.info("🔍 Starting Atomic Requirement Extraction...")
        
        # Split by lines first, then by punctuation if needed
        lines = self.content.split('\n')
        
        req_id_counter = 1
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith(('#', '|', '---')): 
                continue # Skip headers and tables for now (tables handled by parser)
            
            # Remove Markdown list markers
            clean_text = re.sub(r'^[-*]\s+', '', line)
            
            # 1. Detection: Numbers (potential SLAs/Limits)
            # Look for digits that are NOT just item numbers (like "1.")
            has_number = re.search(r'\b\d+(?!\.)\b', clean_text)
            
            # 2. Detection: Keywords
            keywords = ["must", "shall", "required", "bắt buộc", "tuyệt đối", "không được", "only", "duy nhất"]
            has_keyword = any(k in clean_text.lower() for k in keywords)
            
            if has_number or has_keyword:
                req_id = f"REQ-AUTO-{req_id_counter:03d}"
                category = "Performance/Limit" if has_number else "Functional/Constraint"
                
                self.requirements.append({
                    "id": req_id,
                    "text": clean_text,
                    "type": category,
                    "criticality": "High" if "tuyệt đối" in clean_text.lower() or "must" in clean_text.lower() else "Medium"
                })
                req_id_counter += 1
                log.info(f"   👉 Detected: [{req_id}] {clean_text[:50]}...")

        return self.requirements

    def save_to_json(self, output_path="output/requirements.json"):
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump({"atomic_requirements": self.requirements}, f, indent=2, ensure_ascii=False)
            log.info(f"✅ Extracted {len(self.requirements)} atomic requirements to {output_path}")
            return True
        except Exception as e:
            log.error(f"❌ Failed to save requirements: {e}")
            return False

def run_extraction(prd_path):
    try:
        # Use PRDParser to extract metadata
        from .markdown_parser import PRDParser
        
        parser = PRDParser(prd_path)
        if not parser.load():
            return False
        
        # Extract metadata from header
        metadata = parser.extract_metadata_header()
        log.info(f"📊 Metadata extracted: {metadata}")
        
        # Extract atomic requirements
        content = parser.get_full_content()
        extractor = RequirementExtractor(content)
        extractor.extract_atomic()
        
        # Save requirements with metadata
        output_data = {
            "metadata": metadata,
            "atomic_requirements": extractor.requirements
        }
        
        output_path = "output/requirements.json"
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        log.info(f"✅ Extracted {len(extractor.requirements)} atomic requirements with metadata to {output_path}")
        return True
    except Exception as e:
        log.error(f"Error in extraction: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False

import pandas as pd
import json
import os
import sys
from .logger import log
from .exporter import Exporter

class Reporter:
    def __init__(self, input_path: str):
        self.input_path = input_path
        self.exporter = Exporter(output_dir="output")

    def load_data(self) -> pd.DataFrame:
        """Load data from Markdown, JSON or Excel into DataFrame"""
        if not os.path.exists(self.input_path):
            log.error(f"Input file not found: {self.input_path}")
            return pd.DataFrame()

        try:
            if self.input_path.endswith('.md'):
                return self._parse_markdown()
            elif self.input_path.endswith('.json'):
                return self._parse_json()
            elif self.input_path.endswith('.xlsx'):
                return pd.read_excel(self.input_path)
            else:
                log.error("Unsupported format")
                return pd.DataFrame()
        except Exception as e:
            log.error(f"Failed to load data: {e}")
            return pd.DataFrame()

    def _parse_json(self):
        with open(self.input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if "test_cases" in data:
            return pd.DataFrame(data["test_cases"])
        return pd.DataFrame(data)

    def _parse_markdown(self) -> pd.DataFrame:
        """Parse Markdown Pipe Table"""
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            data = []
            for line in lines:
                line = line.strip()
                if line.startswith("| TC-"): # Robust check for Test Case Row
                    parts = [p.strip() for p in line.split("|")]
                    # parts[0] is empty str before first |
                    # Standard: | id | priority | title | steps | expected | status | notes |
                    if len(parts) >= 8:
                        data.append({
                            "id": parts[1],
                            "priority": parts[2],
                            "title": parts[3],
                            "steps": parts[4],
                            "expected_result": parts[5],
                            "status": parts[6],
                            "notes": parts[7] if len(parts) > 7 else ""
                        })
            
            # Infer Type if missing
            for item in data:
                item["type"] = self._infer_type(item["id"])
                
            return pd.DataFrame(data)
        except Exception as e:
            log.error(f"Markdown parse error: {e}")
            return pd.DataFrame()

    def _infer_type(self, tc_id):
        if "SEC" in tc_id: return "Security"
        if "PERF" in tc_id: return "Performance"
        if "ANA" in tc_id: return "Analytics"
        if "VAL" in tc_id: return "Validation"
        if "UI" in tc_id or "COMP" in tc_id: return "UI/UX"
        return "Functional"

    def generate_excel(self, output_path: str):
        df = self.load_data()
        if df.empty:
            log.warning("No data to report.")
            return

        # Use Exporter for layout
        # Convert DataFrame back to list of dicts for Exporter compat, or use pandas directly
        # Here we use pandas directly but with Stats
        
        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Test Cases', index=False)
                
                # Stats
                stats = {
                    "Total": len(df),
                    "Passed": len(df[df['status'].str.contains('Pass', case=False, na=False)]),
                    "Failed": len(df[df['status'].str.contains('Fail', case=False, na=False)]),
                    "Untested": len(df[df['status'].str.contains('\[ \]', na=False)]) # Check for empty check
                }
                
                pd.DataFrame([stats]).to_excel(writer, sheet_name='Summary', index=False)
                
            log.info(f"✅ Excel Report Generated: {output_path}")
        except Exception as e:
            log.error(f"Excel generation failed: {e}")

    def generate_summary_md(self, output_path="output/SUMMARY_REPORT.md"):
        df = self.load_data()
        if df.empty: return

        # Simple Stats
        total = len(df)
        by_type = df['type'].value_counts() if 'type' in df.columns else pd.Series()
        by_prio = df['priority'].value_counts() if 'priority' in df.columns else pd.Series()

        md = f"# Test Execution Summary\n\n**Total Cases**: {total}\n\n"
        md += "## By Type\n" + by_type.to_markdown() + "\n\n"
        md += "## By Priority\n" + by_prio.to_markdown() + "\n"
        
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(md)
        log.info(f"✅ Summary MD Generated: {output_path}")

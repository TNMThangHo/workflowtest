import pandas as pd
from collections import Counter
import re
import sys
from .logger import log
from .schema import TestSuite

class Reporter:
    def __init__(self, input_path: str):
        self.input_path = input_path

    def parse_markdown_to_df(self) -> pd.DataFrame:
        """Parse the generated Markdown file into a DataFrame for reporting"""
        try:
            with open(self.input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception as e:
            log.error(f"Failed to read report input: {e}")
            return pd.DataFrame()

        data = []
        for line in lines:
            line = line.strip()
            # Check for table row with TC ID
            if line.startswith("| TC-"):
                parts = [p.strip() for p in line.split("|")]
                # Structure: | id | priority | title | steps | expected | status | notes |
                # Indices:   0   1    2        3       4       5          6        7      8
                if len(parts) >= 6:
                    data.append({
                        "ID": parts[1],
                        "Priority": parts[2],
                        "Title": parts[3],
                        "Steps": parts[4],
                        "Expected Result": parts[5],
                        "Type": "Functional", # Default, or infer from somewhere else if needed
                        # Note: Type is not in table explicitly, but Priority is. 
                        # We can try to infer from ID e.g. TC-SIGNUP-SEC-001 -> Security
                    })
        
        # Post-processing to infer Type from ID
        for item in data:
            if "SEC" in item["ID"]: item["Type"] = "Security"
            elif "PERF" in item["ID"]: item["Type"] = "Performance"
            elif "VAL" in item["ID"]: item["Type"] = "Validation"
            elif "UI" in item["ID"] or "COMP" in item["ID"]: item["Type"] = "UI/UX" 
            elif "ANA" in item["ID"]: item["Type"] = "Analytics"

        log.info(f"Parsed {len(data)} test cases from Markdown Table.")
        return pd.DataFrame(data)

    def generate_excel(self, output_path: str):
        log.info(f"Generating Excel Report at: {output_path}")
        df = self.parse_markdown_to_df()
        if df.empty:
            log.warning("No data to report.")
            return

        try:
            with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Test Cases', index=False)
                
                # Stats Sheet
                stats = {
                    "Total Cases": len(df),
                    "By Priority": df['Priority'].value_counts().to_dict(),
                    "By Type": df['Type'].value_counts().to_dict()
                }
                pd.DataFrame([stats]).to_excel(writer, sheet_name='Summary')
                
            log.info("✅ Excel Report Generated Successfully.")
        except Exception as e:
            log.error(f"Failed to write Excel: {e}")

    def generate_summary_md(self, output_path="output/SUMMARY_REPORT.md"):
        df = self.parse_markdown_to_df()
        if df.empty:
            return

        stats = f"""# Test Execution Summary
        
**Total Test Cases**: {len(df)}

## Breakdown by Priority
{df['Priority'].value_counts().to_markdown()}

## Breakdown by Type
{df['Type'].value_counts().to_markdown()}
"""
        with open(output_path, "w", encoding='utf-8') as f:
            f.write(stats)
        log.info(f"✅ Markdown Summary Generated at {output_path}")

if __name__ == "__main__":
    rep = Reporter("output/test_cases.md")
    rep.generate_excel("output/TEST_REPORT.xlsx")

import pandas as pd
import os
from typing import List, Dict, Any
from datetime import datetime

class Exporter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def export_to_excel(self, test_cases: List[Dict[str, Any]], filename: str = "test_cases.xlsx") -> str:
        """
        Exports test cases to an Excel file.
        """
        filepath = os.path.join(self.output_dir, filename)
        
        # Flatten steps if necessary or join them
        for tc in test_cases:
            if isinstance(tc.get('steps'), list):
                tc['steps'] = "\n".join(tc['steps'])
        
        df = pd.DataFrame(test_cases)
        
        # Ensure standard columns exist
        standard_columns = [
            "id", "module", "type", "priority", "pre_condition", 
            "description", "steps", "expected_result", "actual_result", "status", "notes", "create_date"
        ]
        
        # Add missing columns with empty values
        for col in standard_columns:
            if col not in df.columns:
                if col == "create_date":
                    df[col] = datetime.now().strftime('%Y-%m-%d')
                else:
                    df[col] = "" # Leave empty for manual entry

        # Filter/Order columns
        cols_to_use = [c for c in standard_columns if c in df.columns]
        
        try:
            df[cols_to_use].to_excel(filepath, index=False)
            return filepath
        except Exception as e:
            return f"Error exporting to Excel: {e}"

    def export_dict_to_excel(self, data: Dict[str, Any], filename: str = "report.xlsx") -> str:
        """
        Exports a flat dictionary to an Excel file (Key-Value pairs).
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            df = pd.DataFrame(list(data.items()), columns=["Metric", "Value"])
            df.to_excel(filepath, index=False)
            return filepath
        except Exception as e:
            return f"Error exporting Dict to Excel: {e}"

    def export_to_markdown(self, content: str, filename: str = "TEST_PLAN.md") -> str:
        """
        Exports text content to a Markdown file.
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception as e:
            return f"Error exporting to Markdown: {e}"

    def export_to_markdown_readable_table(self, data: List[Dict[str, Any]], filename: str = "test_cases.md") -> str:
        """
        Exports list of dicts to a *Compact* Markdown Pipe Table.
        Multi-line content is flattened with ' • ' bullets to avoid <br> tags.
        Status is pre-filled with checkable boxes [ ].
        """
        if not data:
            return "No data to export"
            
        filepath = os.path.join(self.output_dir, filename)
        
        try:
            processed_data = []
            for item in data:
                row = item.copy()
                
                # 1. Status: Clean Checkbox (4 options)
                row['status'] = "[ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked"
                
                # 2. Steps: Flatten to bulleted line
                if isinstance(row.get('steps'), list):
                    # "1. Step A • 2. Step B"
                    row['steps'] = " • ".join(str(s) for s in row['steps'])
                elif isinstance(row.get('steps'), str):
                    row['steps'] = row['steps'].replace('\n', ' • ')

                # 3. Expected Result: Flatten
                if isinstance(row.get('expected_result'), str):
                     row['expected_result'] = row['expected_result'].replace('\n', ' • ')
                elif isinstance(row.get('expected_result'), list):
                     row['expected_result'] = " • ".join(str(s) for s in row['expected_result'])
                
                processed_data.append(row)

            df = pd.DataFrame(processed_data)
            
            # Ensure standard columns exist & Order specific for readability
            standard_columns = [
                "id", "priority", "title", "steps", "expected_result", "status", "notes", "create_date"
            ]
            
            # Add missing columns
            for col in standard_columns:
                if col not in df.columns:
                    if col == "create_date":
                        df[col] = datetime.now().strftime('%Y-%m-%d')
                    else:
                        df[col] = "" 

            # Filter columns
            cols_to_use = [c for c in standard_columns if c in df.columns]
            
            # Generate Standard Markdown Table (Pipe)
            markdown_table = df[cols_to_use].to_markdown(index=False)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# Test Cases\n\n{markdown_table}")
            return filepath
        except Exception as e:
            import traceback
            return f"Error exporting to Readable Markdown Table: {e} {traceback.format_exc()}"

if __name__ == "__main__":
    print("Exporter Initialized")

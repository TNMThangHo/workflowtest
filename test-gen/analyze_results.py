import pandas as pd
import argparse
import sys
import os
import json
# Make sure we can import exporter
sys.path.append(os.path.dirname(__file__))
from exporter import Exporter

def analyze_file(filepath):
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}
    
    try:
        df = None
        # Determine file type
        if filepath.endswith('.xlsx'):
            df = pd.read_excel(filepath)
        elif filepath.endswith('.json'):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # Flatten if it's the raw_testcases wrapper
            if "test_cases" in data:
                df = pd.DataFrame(data["test_cases"])
            else:
                 return {"error": "JSON structure not recognized (missing 'test_cases')"}
        elif filepath.endswith('.md'):
            # Parse Markdown Pipe Table
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Simple parser for Pipe Table
            data = []
            headers = []
            for line in lines:
                line = line.strip()
                if not line.startswith('|'): continue
                if '---' in line: continue # Separator line
                
                # Split by pipe, ignore first/last empty splits
                cols = [c.strip() for c in line.split('|')]
                if len(cols) > 2:
                    # Remove empty start/end if pipe surrounded
                    if cols[0] == '': cols.pop(0)
                    if cols[-1] == '': cols.pop()
                    
                    if not headers:
                        headers = [h.lower() for h in cols]
                    else:
                        # Map to header
                        if len(cols) == len(headers):
                            data.append(dict(zip(headers, cols)))
            
            df = pd.DataFrame(data)

        else:
            return {"error": "Unsupported file format. Use .xlsx, .json or .md"}

        # Normailze column names
        df.columns = [str(c).lower().strip() for c in df.columns]
        
        # Check for status/result column
        status_col = None
        for col in ['status', 'result', 'pass/fail', 'actual result']:
            if col in df.columns:
                status_col = col
                break
        
        stats = {
            "Total Test Cases": len(df),
            "Passed": 0,
            "Failed": 0,
            "Blocked": 0,
            "Skip": 0,
            "Untested": 0
        }
        
        if status_col:
            import re
            # Parse stats manual check marks
            for val in df[status_col]:
                s_raw = str(val).lower()
                
                # Regex looks for [x] with optional spaces: \[ \s* [xX] \s* \]
                # Groups: 
                #   pass_match checks if "pass" follows a checked box
                #   fail_match checks if "fail" follows a checked box, etc.
                
                found_status = None
                
                # Check patterns: "[x] pass", "[ x] pass", "[x ] pass"
                if re.search(r'\[\s*[xX]\s*\]\s*pass', s_raw):
                    found_status = "Passed"
                elif re.search(r'\[\s*[xX]\s*\]\s*fail', s_raw):
                    found_status = "Failed"
                elif re.search(r'\[\s*[xX]\s*\]\s*skip', s_raw):
                    found_status = "Skip"
                elif re.search(r'\[\s*[xX]\s*\]\s*block', s_raw):
                    found_status = "Blocked"
                
                if found_status:
                    stats[found_status] += 1
                else:
                    stats["Untested"] += 1
        else:
             # If no status column, assume untest/new
             stats["Untested"] = len(df)
             # stats["warning"] = "Could not find a 'Status' or 'Result' column."

        return stats
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Path to test cases file (.xlsx or .json)")
    parser.add_argument("--output-excel", help="Path to save Excel Report")
    args = parser.parse_args()
    
    result = analyze_file(args.input)
    
    if args.output_excel and "error" not in result:
        exporter = Exporter(output_dir=os.path.dirname(args.output_excel) or "output")
        filename = os.path.basename(args.output_excel)
        path = exporter.export_dict_to_excel(result, filename=filename)
        result["excel_path"] = path

    print(json.dumps(result, indent=2))

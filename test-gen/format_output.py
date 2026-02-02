import argparse
import json
import os
import pandas as pd
import sys
# Make sure we can import exporter if running from different location
sys.path.append(os.path.dirname(__file__))
from exporter import Exporter

def validate_json(data):
    required_keys = ["test_cases", "test_plan", "release_note"]
    for key in required_keys:
        if key not in data:
            # Silent check for granular workflows
            pass

def main():
    parser = argparse.ArgumentParser(description="Formatter for AI Generated Test Artifacts")
    parser.add_argument("--input", required=True, help="Path to raw JSON output from Agent")
    parser.add_argument("--output", default="output", help="Output directory")
    parser.add_argument("--filename", default=None, help="Custom filename for output")
    
    args = parser.parse_args()
    
    print(f"🚀 Starting Formatting...")
    print(f"📂 Input JSON: {args.input}")
    
    if not os.path.exists(args.input):
        print(f"❌ Error: Input file not found: {args.input}")
        return

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error decoding JSON: {e}")
        return

    validate_json(data)
    
    # Initialize Exporter
    exporter = Exporter(output_dir=args.output)
    
    # 1. Export Test Cases (Markdown)
    test_cases = data.get("test_cases", [])
    if test_cases:
        print(f"\nTest Cases Export: Found {len(test_cases)} test cases.")
        fname = "test_cases.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        
        # Use 'Readable' Markdown Table exporter (Compact, Editable Status)
        md_path = exporter.export_to_markdown_readable_table(test_cases, filename=fname)
        print(f"   -> Saved to: {md_path}")
    else:
        print("\nTest Cases Export: No test cases found.")

    # 2. Export Test Plan (Markdown)
    test_plan = data.get("test_plan", "")
    if test_plan:
        print(f"\nTest Plan Export:")
        fname = "TEST_PLAN.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        plan_path = exporter.export_to_markdown(test_plan, filename=fname)
        print(f"   -> Saved to: {plan_path}")
    
    # 3. Export Release Note (Markdown)
    release_note = data.get("release_note", "")
    if release_note:
        print(f"\nRelease Note Export:")
        fname = "RELEASE_NOTE.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        rn_path = exporter.export_to_markdown(release_note, filename=fname)
        print(f"   -> Saved to: {rn_path}")

    # 4. Generate Summary Report
    summary = f"""# Test Generation Summary
- **Input File**: {args.input}
- **Test Cases**: {len(test_cases)}
- **Artifacts Generated**:
  - Test Cases (Excel)
  - Test Plan (Markdown)
  - Release Note (Markdown)
"""
    exporter.export_to_markdown(summary, "SUMMARY_REPORT.md")
    print("\n✅ Formatting Complete!")

if __name__ == "__main__":
    main()

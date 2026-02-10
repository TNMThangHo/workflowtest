import argparse
import json
import os
import pandas as pd
import sys
from .logger import log
sys.path.append(os.path.dirname(__file__))
from exporter import Exporter
from markdown_generator import generate_markdown_report

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
    
    log.info(f"🚀 Starting Formatting...")
    log.info(f"📂 Input JSON: {args.input}")
    
    if not os.path.exists(args.input):
        log.error(f"❌ Error: Input file not found: {args.input}")
        return

    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        log.error(f"❌ Critical Error: Invalid JSON in {args.input}")
        log.error(f"   📍 Location: Line {e.lineno}, Column {e.colno}")
        log.error(f"   📝 Message: {e.msg}")
        try:
            with open(args.input, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                if 0 <= e.lineno - 1 < len(lines):
                    log.error(f"   🔎 Defective Line: {lines[e.lineno - 1].strip()}")
        except:
            pass
        return

    validate_json(data)
    
    # Initialize Exporter
    exporter = Exporter(output_dir=args.output)
    
    # 1. Export Test Cases (Template-based Markdown)
    test_cases = data.get("test_cases", [])
    if not test_cases:
        test_cases = data.get("functional_testcases", []) + data.get("non_functional_testcases", [])

    if test_cases:
        log.info(f"Test Cases Export: Found {len(test_cases)} test cases.")
        fname = "test_cases.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        
        # Prepare data using exporter's logic (reusing existing robust preparation)
        prepared_data = exporter.prepare_data_for_template(data)
        
        # Generate Markdown using Python Generator (No Jinja2)
        md_content = generate_markdown_report(prepared_data)
        
        # Save output
        out_path = os.path.join(args.output, fname)
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
            
        log.info(f"   -> Saved to: {out_path}")
    else:
        log.warning("Test Cases Export: No test cases found.")

    # 2. Export Test Plan (Markdown)
    test_plan = data.get("test_plan", "")
    if test_plan:
        log.info(f"Test Plan Export:")
        fname = "TEST_PLAN.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        plan_path = exporter.export_to_markdown(test_plan, filename=fname)
        log.info(f"   -> Saved to: {plan_path}")
    
    # 3. Export Release Note (Markdown)
    release_note = data.get("release_note", "")
    if release_note:
        log.info(f"Release Note Export:")
        fname = "RELEASE_NOTE.md"
        if args.filename:
            fname = args.filename if args.filename.endswith('.md') else f"{args.filename}.md"
        rn_path = exporter.export_to_markdown(release_note, filename=fname)
        log.info(f"   -> Saved to: {rn_path}")

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
    log.info("✅ Formatting Complete!")

if __name__ == "__main__":
    main()

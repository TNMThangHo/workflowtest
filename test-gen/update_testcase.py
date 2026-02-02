"""
Update Testcase Script - Incremental testcase updates for MARKDOWN format
Appends new test cases to existing Markdown file without regenerating everything
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import sys
import re

def read_existing_testcases_md(md_path: str) -> tuple[str, set]:
    """
    Read existing testcase Markdown file
    Returns: (full content, set of existing TestCase IDs)
    """
    print(f"📖 Reading existing testcases from: {md_path}")
    
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract TestCase IDs from markdown table
        # Pattern: | TC-XXX-XXX-XXX | ... |
        id_pattern = r'\|\s*([A-Z]+-[A-Z0-9-]+)\s*\|'
        existing_ids = set(re.findall(id_pattern, content))
        
        print(f"✅ Found {len(existing_ids)} existing test cases")
        print(f"   Existing IDs: {len(existing_ids)}")
        
        return content, existing_ids
    except Exception as e:
        print(f"❌ Error reading Markdown: {e}")
        sys.exit(1)

def read_prd(prd_path: str) -> str:
    """Read PRD file content"""
    print(f"📖 Reading PRD from: {prd_path}")
    
    try:
        with open(prd_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        print(f"✅ PRD loaded ({len(content)} characters)")
        return content
    except Exception as e:
        print(f"❌ Error reading PRD: {e}")
        sys.exit(1)

def create_update_context(md_path: str, prd_path: str, output_path: str):
    """
    Prepare context for AI generation
    Creates a JSON file with existing IDs and PRD content
    """
    print("\n📝 Preparing update context...")
    
    # Read existing testcases
    content, existing_ids = read_existing_testcases_md(md_path)
    
    # Read PRD
    prd_content = read_prd(prd_path)
    
    # Create context
    context = {
        "markdown_file": md_path,
        "prd_file": prd_path,
        "existing_testcase_ids": list(existing_ids),
        "existing_count": len(existing_ids),
        "prd_content": prd_content,
        "timestamp": datetime.now().isoformat()
    }
    
    # Save context
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(context, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Context saved to: {output_path}")
    print(f"\n📊 Summary:")
    print(f"   - Existing test cases: {len(existing_ids)}")
    print(f"   - Existing IDs to skip: {len(existing_ids)}")
    print(f"   - PRD size: {len(prd_content)} chars")
    
    return context

def append_testcases_to_markdown(md_path: str, new_cases_json: str, output_dir: str):
    """
    Append new test cases to existing Markdown file
    Adds new rows to the table with Created Date
    """
    print("\n🔄 Merging new test cases with existing Markdown file...")
    
    # Read existing Markdown
    with open(md_path, 'r', encoding='utf-8') as f:
        existing_content = f.read()
    
    print(f"📖 Existing Markdown file loaded")
    
    # Read new test cases from JSON
    with open(new_cases_json, 'r', encoding='utf-8') as f:
        new_cases = json.load(f)
    
    if isinstance(new_cases, dict) and 'testcases' in new_cases:
        new_cases = new_cases['testcases']
    
    print(f"📥 New test cases to add: {len(new_cases)}")
    
    # Create backup
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = Path(output_dir) / f"backup_{timestamp}.md"
    with open(backup_path, 'w', encoding='utf-8') as f:
        f.write(existing_content)
    print(f"💾 Backup created: {backup_path}")
    
    # Generate new rows for Markdown table
    today = datetime.now().strftime('%Y-%m-%d')
    new_rows = []
    
    for tc in new_cases:
        # Escape pipe characters in content
        def escape_pipes(text):
            return str(text).replace('|', '\\|') if text else ''
        
        # Create Markdown table row
        # Format: | id | priority | title | steps | expected_result | status | notes | created_date |
        row = f"| {escape_pipes(tc.get('TestCase ID', ''))} " \
              f"| {escape_pipes(tc.get('Priority', ''))} " \
              f"| {escape_pipes(tc.get('Title', ''))} " \
              f"| {escape_pipes(tc.get('Test Steps', ''))} " \
              f"| {escape_pipes(tc.get('Expected Result', ''))} " \
              f"| [ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked " \
              f"| {escape_pipes(tc.get('Notes', ''))} " \
              f"| {today} |"
        
        new_rows.append(row)
    
    # Append new rows to the end of the file
    updated_content = existing_content.rstrip() + '\n' + '\n'.join(new_rows) + '\n'
    
    # Save updated Markdown
    output_path = Path(output_dir) / f"updated_testcases_{timestamp}.md"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"✅ Updated Markdown saved: {output_path}")
    
    # Count existing test cases (rough count by counting rows starting with |)
    existing_count = len([line for line in existing_content.split('\n') if line.strip().startswith('| TC-')])
    
    # Print summary
    print("\n" + "="*60)
    print("📊 UPDATE SUMMARY")
    print("="*60)
    print(f"Original test cases: ~{existing_count}")
    print(f"New test cases added: {len(new_cases)}")
    print(f"Total test cases: ~{existing_count + len(new_cases)}")
    print(f"Created Date: {today}")
    print(f"\n📁 Files:")
    print(f"   - Updated: {output_path}")
    print(f"   - Backup: {backup_path}")
    print("="*60)
    
    return str(output_path)

def main():
    parser = argparse.ArgumentParser(description='Update testcase Markdown with new test cases')
    parser.add_argument('--mode', choices=['prepare', 'merge'], required=True,
                       help='Mode: prepare (create context) or merge (append test cases)')
    parser.add_argument('--markdown', required=True, help='Path to existing testcase Markdown file')
    parser.add_argument('--prd', help='Path to PRD file (required for prepare mode)')
    parser.add_argument('--new-cases', help='Path to new test cases JSON (required for merge mode)')
    parser.add_argument('--output-dir', default='output', help='Output directory')
    
    args = parser.parse_args()
    
    if args.mode == 'prepare':
        if not args.prd:
            print("❌ Error: --prd is required for prepare mode")
            sys.exit(1)
        
        context_path = Path(args.output_dir) / 'update_context.json'
        create_update_context(args.markdown, args.prd, str(context_path))
        
    elif args.mode == 'merge':
        if not args.new_cases:
            print("❌ Error: --new-cases is required for merge mode")
            sys.exit(1)
        
        append_testcases_to_markdown(args.markdown, args.new_cases, args.output_dir)

if __name__ == '__main__':
    main()

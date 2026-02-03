"""
Update Test Report Module
Automatically generate markdown report from test case results
"""

import re
import sys
from pathlib import Path
from datetime import datetime
from .logger import log


def parse_markdown_status(md_content: str) -> list[dict]:
    """
    Parse test case markdown to extract status and details
    
    Format: [x] Pass / [ ] Fail / [ ] Skip / [ ] Blocked
    """
    results = []
    
    # Pattern to match table rows
    rows = md_content.split('\n')
    
    for row in rows:
        if '|' not in row or row.startswith('|---') or row.startswith('| :--'):
            continue
            
        # Extract columns
        cols = [c.strip() for c in row.split('|')]
        if len(cols) < 3:
            continue
            
        # Find TestCase ID
        tc_id = None
        priority = ""
        title = ""
        
        for i, col in enumerate(cols):
            match = re.search(r'TC-[\w]+-[\w]+-\d+|TC\d{3}', col)
            if match:
                tc_id = match.group()
                # Get priority and title from adjacent columns
                if i + 1 < len(cols):
                    priority = cols[i + 1]
                if i + 2 < len(cols):
                    title = cols[i + 2]
                break
        
        if not tc_id:
            continue
            
        # Extract status from checkbox format
        status_col = next((c for c in cols if '[x]' in c.lower() or '[ ]' in c), None)
        if not status_col:
            continue
            
        # Determine status
        status_lower = status_col.lower()
        if '[x] pass' in status_lower:
            status = 'Pass'
        elif '[x] fail' in status_lower:
            status = 'Fail'
        elif '[x] skip' in status_lower:
            status = 'Skip'
        elif '[x] blocked' in status_lower:
            status = 'Blocked'
        else:
            status = 'Not Run'
            
        results.append({
            'testcase_id': tc_id,
            'priority': priority,
            'title': title,
            'status': status,
            'execution_date': datetime.now().strftime('%Y-%m-%d')
        })
    
    log.info(f"Parsed {len(results)} test results from markdown")
    return results


def generate_markdown_report(results: list[dict], template_path: str = "test-gen/templates/test-report-template.md") -> str:
    """
    Generate markdown report from test results using template
    
    Args:
        results: List of test results with testcase_id, status, etc.
        template_path: Path to template file
        
    Returns:
        Markdown report content
    """
    # Read template
    template_file = Path(template_path)
    if not template_file.exists():
        log.warning(f"Template not found: {template_path}, using default structure")
        # Use template structure
        template_content = template_file.read_text(encoding='utf-8') if template_file.exists() else ""
    
    # Calculate statistics
    total = len(results)
    pass_count = sum(1 for r in results if r['status'] == 'Pass')
    fail_count = sum(1 for r in results if r['status'] == 'Fail')
    skip_count = sum(1 for r in results if r['status'] == 'Skip')
    blocked_count = sum(1 for r in results if r['status'] == 'Blocked')
    
    pass_rate = (pass_count / total * 100) if total > 0 else 0
    
    # Build report using template structure
    report = f"""# Test Report

## 1. Summary

- Feature tested: User Registration
- Test cycle: Cycle 1
- Date: {datetime.now().strftime('%Y-%m-%d')}

## 2. Test Execution Result

| Total TC | Passed | Failed | Blocked | Skip |
| -------- | ------ | ------ | ------- | ---- |
| {total}  | {pass_count} | {fail_count} | {blocked_count} | {skip_count} |

**Pass Rate:** {pass_rate:.1f}%

## 3. Detailed Test Results

| TestCase ID | Title | Priority | Status | Notes |
| :---------- | :---- | :------- | :----- | :---- |
"""
    
    # Add test results
    for r in results:
        status_emoji = {
            'Pass': '✅',
            'Fail': '❌',
            'Skip': '⏭️',
            'Blocked': '🚫',
            'Not Run': '⚪'
        }.get(r['status'], '⚪')
        
        report += f"| {r['testcase_id']} | {r.get('title', '')} | {r.get('priority', '')} | {status_emoji} {r['status']} | |\n"
    
    report += f"""
## 4. Defect Summary

| Bug ID | Severity | Status | Description |
| ------ | -------- | ------ | ----------- |
| TBD    | -        | -      | No bugs reported yet |

## 5. Key Findings

- {pass_count} test cases passed successfully
- {fail_count} test cases failed
- {blocked_count} test cases blocked
- {skip_count} test cases skipped

## 6. Risks & Recommendations

- Review failed test cases and create bug tickets
- Re-test blocked cases after dependencies resolved
"""
    
    return report


def run_update_report(testcase_file: str, report_file: str = None):
    """
    Main function to generate markdown report from test case markdown
    
    Args:
        testcase_file: Path to test case markdown with status
        report_file: Output path for markdown report (default: output/UPDATED_TEST_REPORT.md)
    """
    log.info("Starting test report generation...")
    
    # Read markdown file
    tc_path = Path(testcase_file)
    if not tc_path.exists():
        log.error(f"Test case file not found: {testcase_file}")
        print(f"❌ File not found: {testcase_file}")
        return False
    
    md_content = tc_path.read_text(encoding='utf-8')
    
    # Parse status
    results = parse_markdown_status(md_content)
    
    if not results:
        log.warning("No test results found in markdown")
        print("⚠️ No test results found in markdown file")
        return False
    
    # Generate report
    try:
        report_content = generate_markdown_report(results)
        
        # Determine output path
        if not report_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_file = f"output/UPDATED_TEST_REPORT_{timestamp}.md"
        
        output_path = Path(report_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write report
        output_path.write_text(report_content, encoding='utf-8')
        log.info(f"Report generated: {output_path}")
        
        # Calculate and print statistics
        total = len(results)
        stats = {
            'Pass': sum(1 for r in results if r['status'] == 'Pass'),
            'Fail': sum(1 for r in results if r['status'] == 'Fail'),
            'Skip': sum(1 for r in results if r['status'] == 'Skip'),
            'Blocked': sum(1 for r in results if r['status'] == 'Blocked'),
        }
        
        print(f"\n✅ Test Report Generated!")
        print(f"\n📊 Statistics:")
        print(f"   - Total test cases: {total}")
        print(f"\n📈 Test Results:")
        for status, count in stats.items():
            pct = (count / total * 100) if total > 0 else 0
            print(f"   - {status}: {count} ({pct:.1f}%)")
        
        pass_rate = (stats['Pass'] / total * 100) if total > 0 else 0
        print(f"\n🎯 Pass Rate: {pass_rate:.1f}%")
        print(f"\n📁 Output: {output_path}")
        
        return True
        
    except Exception as e:
        log.error(f"Error generating report: {e}", exc_info=True)
        print(f"❌ Error: {e}")
        return False

from typing import List, Dict, Any
import datetime

def generate_markdown_report(data: Dict[str, Any]) -> str:
    """
    Generate the test case markdown report directly using Python string manipulation.
    This avoids Jinja2 template issues entirely.
    """
    lines = []
    
    # --- HEADER ---
    lines.append("# 📘 TÀI LIỆU TEST CASE - Test Cases")
    lines.append("")
    lines.append("---")
    lines.append("")
    lines.append("**Thông tin chung:**")
    lines.append("")
    lines.append(f"- **Feature:** {data.get('feature_name', 'Test Cases')}")
    lines.append(f"- **Phiên bản PRD:** {data.get('prd_version', '1.0.0')}")
    lines.append(f"- **Ngày tạo:** {datetime.datetime.now().strftime('%Y-%m-%d')}")
    lines.append("- **Người thực hiện:** QA Team")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- DASHBOARD ---
    lines.append("## I. THỐNG KÊ TỔNG QUAN (DASHBOARD)")
    lines.append("")
    lines.append("### 1. Tổng hợp số lượng")
    lines.append("")
    lines.append("| Chỉ số | Giá trị |")
    lines.append("| :--- | :--- |")
    
    total_tc = len(data.get('functional_testcases', [])) + len(data.get('non_functional_testcases', []))
    lines.append(f"| **Tổng số Test Case** | **{total_tc}** |")
    lines.append(f"| Functional (Chức năng) | {len(data.get('functional_testcases', []))} |")
    lines.append(f"| Non-Functional (Phi chức năng) | {len(data.get('non_functional_testcases', []))} |")
    lines.append("")

    # Additional dashboard logic (Priority distribution) can be calculated here...
    
    lines.append("### 2. Phân bố mức độ ưu tiên")
    lines.append("")
    # Calculate Stats
    p0 = p1 = p2 = p3 = 0
    all_tcs = data.get('functional_testcases', []) + data.get('non_functional_testcases', [])
    for tc in all_tcs:
        p = str(tc.get('priority', '')).upper()
        if 'P0' in p: p0 += 1
        elif 'P1' in p: p1 += 1
        elif 'P2' in p: p2 += 1
        elif 'P3' in p: p3 += 1
            
    def _pct(val, total): 
        return f"{(val/total)*100:.1f}%" if total > 0 else "0.0%"
        
    lines.append("| Mức độ | Số lượng | Tỷ lệ (%) |")
    lines.append("| :--- | :--- | :--- |")
    lines.append(f"| **P0 (Critical - Blocker)** | {p0} | {_pct(p0, total_tc)} |")
    lines.append(f"| **P1 (Cao - High)** | {p1} | {_pct(p1, total_tc)} |")
    lines.append(f"| **P2 (Trung bình - Medium)** | {p2} | {_pct(p2, total_tc)} |")
    lines.append(f"| **P3 (Thấp - Low)** | {p3} | {_pct(p3, total_tc)} |")
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- FUNCTIONAL TABLE ---
    lines.append("## II. KIỂM THỬ CHỨC NĂNG (FUNCTIONAL TESTING)")
    lines.append("")
    lines.append("Dưới đây là danh sách chi tiết các kịch bản kiểm thử nghiệp vụ.")
    lines.append("")
    
    # Table Header - 11 Columns
    headers = [
        "ID", "Module", "Title", "Pre-condition", "Step", 
        "Test Data", "Expected Result", "Status", "Priority", 
        "Create Date", "Execute Date"
    ]
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("| " + " | ".join([":---"] * len(headers)) + " |")

    for tc in data.get('functional_testcases', []):
        # Format status for execution context
        status_raw = tc.get('status', '')
        status_display = status_raw
        if status_raw in ['New', '[ ]', '']:
             status_display = '[ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked'

        row = [
            tc.get('id', ''),
            tc.get('module', ''),
            tc.get('title', ''),
            tc.get('pre_condition', '-'),
            tc.get('steps_short', ''),
            tc.get('test_data', '-'),
            tc.get('expected_result', ''),
            status_display,
            tc.get('priority', ''),
            tc.get('created_date', ''),
            tc.get('execute_date', '')
        ]
        # Escape pipes in content just in case
        row = [str(col).replace('|', '&#124;').replace('\n', '<br>') for col in row]
        lines.append("| " + " | ".join(row) + " |")
    
    lines.append("")
    lines.append("---")
    lines.append("")

    # --- NON-FUNCTIONAL TABLE ---
    lines.append("## III. KIỂM THỬ PHI CHỨC NĂNG (NON-FUNCTIONAL TESTING)")
    lines.append("")
    lines.append("### 1. Phạm vi kiểm thử")
    lines.append("")
    categories = data.get('nft_categories', [])
    all_cats = ["Functional", "Performance", "Security", "Visual", "Availability", "Reliability", "Usability", "Accessibility", "Compatibility", "Analytics"]
    for cat in all_cats:
        mark = "x" if cat in categories else " "
        lines.append(f"- [{mark}] **{cat}**")
    lines.append("")
    
    lines.append("### 2. Danh sách Test Case chi tiết")
    lines.append("")
    
    # Table Header - 10 Columns for NF to match Functional style where applicable
    headers_nf = [
        "ID", "Category", "Title", "Tools/Env", "Step", 
        "Pass Criteria", "Status", "Priority", 
        "Create Date", "Execute Date"
    ]
    
    lines.append("| " + " | ".join(headers_nf) + " |")
    lines.append("| " + " | ".join([":---"] * len(headers_nf)) + " |")

    for tc in data.get('non_functional_testcases', []):
        # Format status for execution context
        status_raw = tc.get('status', '')
        status_display = status_raw
        if status_raw in ['New', '[ ]', '']:
             status_display = '[ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked'
             
        row = [
            tc.get('id', ''),
            tc.get('category', ''),
            tc.get('title', ''),
            tc.get('tools', '-') or tc.get('pre_condition', '-'),
            tc.get('steps_short', ''),
            tc.get('pass_criteria', '') or tc.get('expected_result', ''),
            status_display,
            tc.get('priority', ''),
            tc.get('created_date', ''),
            tc.get('execute_date', '')
        ]
        row = [str(col).replace('|', '&#124;').replace('\n', '<br>') for col in row]
        lines.append("| " + " | ".join(row) + " |")

    lines.append("")
    lines.append("---")
    lines.append("")
    
    # --- BUG TRACKING ---
    lines.append("## IV. GHI CHÚ & THEO DÕI LỖI (BUG TRACKING)")
    lines.append("")
    lines.append("_(Phần này dành cho Tester ghi chú thủ công khi chạy test)_")
    lines.append("")
    lines.append("### Danh sách Bug phát hiện:")
    lines.append("")
    lines.append("| Bug ID | Liên kết (Jira/Issue) | Mức độ nghiêm trọng | Trạng thái |")
    lines.append("| :--- | :--- | :--- | :--- |")
    lines.append("| | | | |")
    lines.append("| | | | |")

    return "\n".join(lines)

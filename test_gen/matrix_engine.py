from typing import List, Dict, Any
try:
    from .schema_models import SmartSchema, FieldType, BusinessRule, VisualRule
except ImportError:
    from schema_models import SmartSchema, FieldType, BusinessRule, VisualRule

class MatrixEngine:
    """
    The Factory: Converts a concise SmartSchema into a massive list of Test Cases.
    Applies BVA (Boundary Value Analysis), Equivalence Partitioning, and Security Baselines.
    """
    
    def __init__(self, schema: SmartSchema):
        self.schema = schema
        self.test_cases = []

    def _expand_filter_combinations(self, section):
        """
        [NEW] Generates combinatorial test cases for filters.
        Detects optional list/text fields and creates combined scenarios.
        """
        filter_fields = [f for f in section.fields if not f.required and f.type in ["select", "radio", "date", "text"]]
        
        if len(filter_fields) >= 2:
            # 1. Verify All Filters Applied
            names = [f.name for f in filter_fields[:3]] # Limit to 3 to avoid explosion
            self._add_tc("Business Logic", f"Verify {section.name} - Combined Filter: {', '.join(names)}", 
                         f"1. Enter/Select valid values for: {', '.join(names)}.\n2. Apply Filter.", 
                         "List shows only records matching ALL criteria.", "P1")
            
            # 2. Verify Clear All
            self._add_tc("Functional", f"Verify {section.name} - Clear All Filters", 
                         "1. Apply multiple filters.\n2. Click 'Clear' or 'Reset'.", 
                         "All filters reset to default. List shows all records.", "P2")

            # 3. [NEW] Pairwise Combinations (up to 10 pairs to avoid explosion)
            import itertools
            start_idx = 0
            for pair in itertools.combinations([f.name for f in filter_fields], 2):
                if start_idx >= 10: break
                self._add_tc("Business Logic", f"Verify {section.name} - Combined Filter: {pair[0]} + {pair[1]}",
                             f"1. Select {pair[0]}.\n2. Select {pair[1]}.\n3. Apply Filter.",
                             "List shows records matching BOTH criteria.", "P2")
                start_idx += 1

    def _get_rule_summary(self, text: str) -> str:
        """ Helper: Extracts a short summary from rule description (e.g. before the first colon). """
        if ":" in text:
            return text.split(":")[0].strip()
        return " ".join(text.split()[:7]) + "..."

    # Vietnamese Translation Mappings
    TITLE_TRANSLATIONS = {
        # Actions
        "Verify": "Kiểm tra",
        "Check": "Kiểm tra",
        "Test": "Test",
        "Validate": "Xác thực",
        "Enter": "Nhập",
        "Select": "Chọn",
        "Click": "Bấm",
        "Upload": "Tải lên",
        "Download": "Tải xuống",
        "Delete": "Xóa",
        "Edit": "Sửa",
        "View": "Xem",
        "Create": "Tạo",
        "Update": "Cập nhật",
        "Submit": "Gửi",
        "Cancel": "Hủy",
        "Save": "Lưu",
        "Search": "Tìm kiếm",
        "Filter": "Lọc",
        "Sort": "Sắp xếp",
        "Open": "Mở",
        "Close": "Đóng",
        "Login": "Đăng nhập",
        "Logout": "Đăng xuất",
        "Approve": "Duyệt",
        "Reject": "Từ chối",
        
        # Fields & Components
        "Button": "Nút",
        "Field": "Trường",
        "Input": "Ô nhập",
        "Dropdown": "Danh sách chọn",
        "Checkbox": "Hộp kiểm",
        "Radio": "Nút chọn",
        "Table": "Bảng",
        "List": "Danh sách",
        "Form": "Biểu mẫu",
        "Dialog": "Hộp thoại",
        "Modal": "Cửa sổ",
        "Popup": "Cửa sổ bật lên",
        "Menu": "Menu",
        "Tab": "Tab",
        "Panel": "Bảng điều khiển",
        "Card": "Thẻ",
        "Row": "Dòng",
        "Column": "Cột",
        "Header": "Tiêu đề",
        "Footer": "Chân trang",
        "Sidebar": "Thanh bên",
        "Toolbar": "Thanh công cụ",
        "Icon": "Biểu tượng",
        "Image": "Hình ảnh",
        "Link": "Liên kết",
        "Page": "Trang",
        "Screen": "Màn hình",
        
        # Validation & States
        "Empty": "Trống",
        "Required": "Bắt buộc",
        "Optional": "Tùy chọn",
        "Valid": "Hợp lệ",
        "Invalid": "Không hợp lệ",
        "Error": "Lỗi",
        "Success": "Thành công",
        "Warning": "Cảnh báo",
        "Disabled": "Vô hiệu hóa",
        "Enabled": "Kích hoạt",
        "Hidden": "Ẩn",
        "Visible": "Hiển thị",
        "Loading": "Đang tải",
        "Pending": "Chờ xử lý",
        "Completed": "Hoàn thành",
        "Failed": "Thất bại",
        
        # Scenarios
        "Happy Path": "Trường hợp chuẩn",
        "Edge Case": "Trường hợp biên",
        "Negative Case": "Trường hợp âm",
        "Boundary": "Biên",
        "Min Length": "Độ dài tối thiểu",
        "Max Length": "Độ dài tối đa",
        "Min Value": "Giá trị tối thiểu",
        "Max Value": "Giá trị tối đa",
        
        # Security
        "XSS Injection": "Tấn công XSS",
        "SQL Injection": "Tấn công SQL",
        "HTML Injection": "Tấn công HTML",
        "Command Injection": "Tấn công Command",
        "Null Byte Injection": "Tấn công Null Byte",
        "Param Tampering": "Giả mạo tham số",
        "Unauthorized Access": "Truy cập trái phép",
        "Permission Check": "Kiểm tra quyền",
        
        # UI/UX
        "Tooltip": "Chú thích",
        "Help Text": "Văn bản trợ giúp",
        "Visibility": "Hiển thị",
        "Layout": "Bố cục",
        "Responsiveness": "Responsive",
        "Visual Cues": "Gợi ý trực quan",
        "Empty State": "Trạng thái trống",
        "Long Content": "Nội dung dài",
        "Hover": "Di chuột",
        
        # Performance & Compatibility
        "Large Dataset": "Dữ liệu lớn",
        "Performance": "Hiệu suất",
        "Load Time": "Thời gian tải",
        "Browser": "Trình duyệt",
        "Mobile": "Di động",
        "Desktop": "Máy tính",
        
        # Pagination & Actions
        "Pagination": "Phân trang",
        "Next": "Tiếp theo",
        "Previous": "Trước đó",
        "First": "Đầu tiên",
        "Last": "Cuối cùng",
        "Bulk": "Hàng loạt",
        "Select All": "Chọn tất cả",
        
        # Common Terms
        "on": "trên",
        "for": "cho",
        "with": "với",
        "without": "không có",
        "and": "và",
        "or": "hoặc",
    }

    def _translate_title_to_vietnamese(self, english_title: str) -> str:
        """
        Auto-translate test case title from English to Vietnamese.
        Uses keyword mapping for common test case patterns.
        """
        import re
        
        # Keep BR-XXX prefix intact
        if english_title.startswith(("BR-", "LOGIN-", "CHECKOUT-")):
            return english_title  # Already Vietnamese from _generate_positive_title
        
        # Translate piece by piece
        vietnamese_title = english_title
        
        # Sort by length (longer first to match phrases before words)
        sorted_translations = sorted(self.TITLE_TRANSLATIONS.items(), key=lambda x: len(x[0]), reverse=True)
        
        for english, vietnamese in sorted_translations:
            # Use word boundary regex to prevent mid-word replacements
            # e.g., 'on' should match ' on ' but not 'Option'
            pattern = r'\b' + re.escape(english) + r'\b'
            vietnamese_title = re.sub(pattern, vietnamese, vietnamese_title, flags=re.IGNORECASE)
        
        return vietnamese_title

    def _generate_positive_title(self, rule: BusinessRule) -> str:
        """
        Generate unique Vietnamese title for each BR based on its specific purpose.
        CRITICAL: Must handle all 13 BRs uniquely to avoid confusion for non-technical QC.
        """
        rid = rule.id.upper() if rule.id else ""
        desc = rule.description.lower()
        
        # === FILTER & UI RULES ===
        if "BR-001" in rid:  # Regional filter dependency
            return f"{rid}: Chưa chọn Region → Combobox Area bị vô hiệu hóa (grayed out)"
        
        if "BR-002" in rid:  # Area filter data filtering
            return f"{rid}: Chọn Region A → Area Filter chỉ hiển thị các area thuộc Region A"
        
        if "BR-011" in rid:  # Empty data handling
            return f"{rid}: Filter không match kết quả nào → Hiển thị 'No data available'"
        
        if "BR-012" in rid:  # Real-time search
            return f"{rid}: Gõ từ khóa vào Search Box → Danh sách cập nhật real-time (không cần bấm Search)"
        
        if "BR-013" in rid:  # Default sorting
            return f"{rid}: Load trang lần đầu → Request sắp xếp theo ngày tạo (mới nhất trước)"
        
        # === PERMISSION & ROLE RULES ===
        if "BR-003" in rid:  # Multi-role aggregation
            return f"{rid}: User có 2 vai trò (PM + Approver) → Thấy request từ cả 2 vai trò"
        
        if "BR-009" in rid:  # Role-based button visibility
            return f"{rid}: User không phải Approver hiện tại → Nút Duyệt/Từ chối bị disable/ẩn"
        
        if "BR-010" in rid:  # Permission error handling
            return f"{rid}: User bị thu hồi quyền Approver → Bấm Approve hiển thị lỗi 'Không được phép thao tác'"
        
        # === APPROVAL WORKFLOW RULES ===
        if "BR-004" in rid:  # Rejection workflow
            return f"{rid}: Người duyệt từ chối ở bất kỳ cấp nào → Request chuyển 'Rejected', Legal chuyển 'In Progress'"
        
        if "BR-005" in rid:  # Mandatory reject reason
            return f"{rid}: Nhập đủ lý do từ chối (≥10 ký tự) → Được phép Submit Reject"
        
        if "BR-006" in rid:  # Single-level approval
            return f"{rid}: Workflow 1 cấp + Approve → Request 'Approved', Legal 'Completed'"
        
        if "BR-007" in rid:  # Multi-level sequence
            return f"{rid}: Workflow nhiều cấp → Phải duyệt theo thứ tự Level 1 → Level 2 → Level N"
        
        if "BR-008" in rid:  # Same-level approver logic
            return f"{rid}: Cùng cấp có 2 approver (A, B) → A duyệt xong, B không cần thao tác anymore"
        
        # Fallback for any new rules
        return f"{rid}: {self._get_rule_summary(rule.description)} - Trường hợp chuẩn"

    def _generate_violation_title(self, rule: BusinessRule) -> str:
        """
        Generate violation scenario title for negative test cases.
        """
        rid = rule.id.upper() if rule.id else ""
        
        if "BR-001" in rid:
            return f"{rid}: Đã chọn Region nhưng modify DOM để enable Area → Bị chặn hoặc validate lỗi"
        
        if "BR-005" in rid:
            return f"{rid}: Bấm Reject nhưng không nhập lý do → Hiển thị lỗi 'Rejection reason is required'"
        
        if "BR-007" in rid:
            return f"{rid}: Level 1 chưa duyệt mà Level 2 cố bypass → Nút bị disabled/API reject"
        
        return f"{rid}: Vi phạm điều kiện → Bị chặn/Hiển thị lỗi"

    def _convert_rule_v2(self, rule: BusinessRule):
        """
        [UPGRADED v2.2] Convert Business Rule → Multiple Test Cases
        Generates:
          1. Happy Path (Positive Scenario)
          2. Negative Scenario (Violation)
          3. State Transition (if status-related)
        """
        # Generate Vietnamese title WITHOUT BR-XXX prefix
        positive_title = self._generate_positive_title(rule)
        # Remove BR-XXX prefix for final output (QC doesn't need technical codes)
        if ':' in positive_title and positive_title.split(':')[0].startswith('BR-'):
            positive_title = positive_title.split(':', 1)[1].strip()
        
        violation_title = self._generate_violation_title(rule)
        if ':' in violation_title and violation_title.split(':')[0].startswith('BR-'):
            violation_title = violation_title.split(':', 1)[1].strip()
        
        # Scenario 1: Happy Path
        self._add_tc("Business Logic", positive_title,
                    f"Condition: {rule.condition} (Satisfied)",
                    f"Result: {rule.expected_result}",
                    "P0")
        
        # Scenario 2: Negative Case
        keywords = ["not", "cannot", "invalid", "blocked", "disabled", "prohibited", "error", "fail"]
        if any(keyword in rule.description.lower() for keyword in keywords):
            self._add_tc("Business Logic", violation_title, 
                     f"Condition: Violate '{rule.condition}'", 
                     "Result: Action blocked / Error message displayed.", 
                     priority="P2")

        # Scenario 3: State Transition (if detected)
        if "status" in rule.expected_result.lower() or "trạng thái" in rule.expected_result.lower():
            # Generate state-specific title
            rid = rule.id.upper() if rule.id else ""
            result_lower = rule.expected_result.lower()
            
            if "rejected" in result_lower:
                state_title = f"{rid}: Verify trạng thái chuyển sang 'Rejected'"
            elif "approved" in result_lower:
                state_title = f"{rid}: Verify trạng thái chuyển sang 'Approved'"
            elif "completed" in result_lower:
                state_title = f"{rid}: Verify Legal Category chuyển sang 'Completed'"
            else:
                state_title = f"{rid}: Verify cập nhật trạng thái: {rule.expected_result}"
            
            self._add_tc("Business Logic", state_title, 
                     f"Trigger: {rule.condition}", 
                     f"Verify Status changes to: {rule.expected_result}", 
                     priority="P1")

    def _expand_smart_actions(self, field: FieldType, prefix: str):
        """ [NEW] Generates conditional action tests (e.g., Reject requires Reason) """
        if field.type == "radio" and "Action" in field.name:
            # Detect Approve/Reject pattern
            has_reject = any("reason" in opt.lower() or "reject" in opt.lower() for opt in field.options or [])
            if has_reject:
                 self._add_tc("Business Logic", f"{prefix} - Reject without Reason", 
                     "1. Select 'Reject'.\n2. Leave Reason empty.\n3. Submit.", 
                     "Error: Reason is required.", "P1")

    def _expand_roles_permissions(self, rule: BusinessRule):
        """ [NEW] Generates Role-Based Access Control (RBAC) tests """
        roles = ["Manager", "Creator", "Approver", "Admin", "User", "Quản lý", "Người tạo", "Người duyệt", "Phụ trách"]
        found_roles = [r for r in roles if r.lower() in rule.description.lower()]
        
        if found_roles:
            for role in found_roles:
                 self._add_tc("Security", f"Kiểm tra quyền: Đăng nhập với vai trò '{role}' → Hệ thống cho phép/từ chối hành động", 
                     f"1. Login as '{role}'.\n2. Perform action defined in rule.", 
                     f"System respects '{role}' privileges (Allow/Deny).", "P1")
            
            # Dual Role High Value Case
            if len(found_roles) >= 2:
                 self._add_tc("Security", f"User có 2 vai trò ({found_roles[0]} + {found_roles[1]}) → Quyền tổng hợp từ cả 2 role", 
                     f"1. Login as User with BOTH '{found_roles[0]}' and '{found_roles[1]}'.", 
                     "System grants combined privileges (Union of permissions).", "P1")

    def _expand_approval_flows(self, rule: BusinessRule):
        """
        [UPGRADED v3.0] Generates Approval Flow test cases ONLY for rules explicitly about approval flows.
        Uses rule-specific Vietnamese titles to avoid duplication.
        CRITICAL: Only BR-004, BR-006, BR-007 should trigger flow generation.
        BR-008 and BR-009 are NOT about flows, so they skip this function.
        """
        rid = rule.id or ""
        desc = rule.description.lower()
        
        # ONLY expand flows for rules that are SPECIFICALLY about multi-level workflows
        # BR-008 (same-level approver logic) and BR-009 (role-based visibility) are NOT flow rules!
        if rid not in ["BR-004", "BR-006", "BR-007"]:
            return  # Skip - not a flow rule
        
        # Generate flow-specific test cases with descriptive Vietnamese titles (NO BR-XXX)
        if rid == "BR-004":  # Rejection workflow
            self._add_tc("Business Logic", "Quy trình từ chối: Level 2 từ chối → Request 'Rejected', Legal quay về 'In Progress'",
                        "1. Level 1 Approve.\n2. Level 2 REJECT.",
                        "Status reverts to In Progress/Rejected.",
                        "P1")
        
        elif rid == "BR-006":  # Single-level approval
            self._add_tc("Business Logic", "Workflow 1 cấp duy nhất: Approve xong → Legal chuyển 'Completed' ngay",
                        "1. Request is Single Level.\n2. Approver Approves.",
                        "Status changes quickly to 'Completed'.",
                        "P1")
        
        elif rid == "BR-007":  # Sequential approval
            self._add_tc("Business Logic", "Quy trình tuần tự: Level 1 chưa duyệt → Nút Level 2 bị disabled",
                        "1. Level 1 Pending.\n2. Try to Approve as Level 2.",
                        "Action Blocked / Button Disabled.",
                        "P2")
            self._add_tc("Business Logic", "Quy trình tuần tự: Level 1 duyệt xong → Level 2 được phép duyệt tiếp",
                        "1. Level 1 Approves.\n2. Level 2 Approves.",
                        "Status changes to 'Pending Level 2', then 'Approved/Completed'.",
                        "P1")

    def _expand_concurrency(self, rule: BusinessRule):
        """ [NEW] Generates Concurrency/Group Logic """
        rid = rule.id.upper() if rule.id else ""
        desc = rule.description.lower()
        
        # BR-003: Multi-role aggregation OR BR-008/010: Same-level approver logic
        if any(k in desc for k in ["any", "all", "đồng thuận", "nhóm", "group", "cùng 1 cấp", "same-level"]):
             self._add_tc("Business Logic", "Cùng cấp có nhiều approver: User A duyệt trước → User B không cần thao tác nữa", 
                     "1. User A (Group 1) approves.\n2. User B (Group 1) views request.", 
                     "User B sees request as 'Approved' (No action needed).", "P1")
             self._add_tc("Business Logic", "Cùng cấp: 2 user bấm Approve đồng thời → Hệ thống xử lý không conflict", 
                     "1. User A and User B click 'Approve' at exact same time.", 
                     "System handles race condition (Single success or Idempotent).", "P2")

    def _expand_search_advanced(self, section):
        """ [NEW v2.2] Explodes Search Scenarios (Multi-select, Dropdown Search, Advanced Keyword) """
        for field in section.fields:
            desc_lower = (field.description or "").lower()
            name_lower = field.name.lower()
            
            # 1. Multi-select Support (Forced for all Filter Selects)
            # [FIXED v2.3] Removed strict "multi/nhiều" check to ensure coverage for Area/Region/Status
            if field.type in ["select", "param"]:
                 self._add_tc("Business Logic", f"Verify {field.name} - Multi-select Filter", 
                     f"1. Select Value A.\n2. Select Value B.\n3. Apply Filter.", 
                     "List shows records matching A OR B (based on logic).", "P1")

            # 2. Dropdown Search
            if field.type in ["select", "param"] and ("tìm kiếm" in desc_lower or "search" in desc_lower):
                 self._add_tc("Functional", f"Verify {field.name} - Dropdown Search", 
                     f"1. Click dropdown.\n2. Type partial text.", 
                     "Dropdown filters options matching text.", "P2")

            # 3. Advanced Keyword Search
            if "keyword" in name_lower or "tìm kiếm" in name_lower:
                self._add_tc("Business Logic", f"Verify {field.name} - Advanced Search (Combinations)", 
                     "1. Enter text matching 'Content'.\n2. Enter text matching 'Doc Name'.\n3. Enter text matching 'Description'.", 
                     "Results match any of the fields (OR logic).", "P1")

    def _expand_detail_popup(self, field: FieldType, prefix: str):
        """ [NEW v2.3] Explicitly Covers Detail Popup Fields """
        if field.type == "complex_view" or "popup" in field.name.lower():
            # 1. Verify All Fields Displayed
            required_fields = ["Nội dung", "Trạng thái", "Người yêu cầu", "Tên dự án", "Vùng - khu vực", "Đường dẫn"]
            self._add_tc("Visual", f"{prefix} - Verify Popup displays all required fields", 
                         "1. Open Popup.", 
                         f"Displays: {', '.join(required_fields)}.", "P2")

    def _expand_ui_ux_gaps(self, section):
        """ [NEW v2.2] Covers Link Navigation, Notifications, Colors """
        for field in section.fields:
            desc_lower = (field.description or "").lower()
            extra = field.extra_props or {}
            
            # 1. Link Navigation (Chuyển đến)
            if "link" in field.type or "chuyển đến" in desc_lower or "chi tiết" in desc_lower:
                target = "Detail Screen"
                if "công việc" in desc_lower: target = "Task Detail"
                self._add_tc("Functional", f"Verify {field.name} - Link Navigation", 
                     f"1. Click on '{field.name}' link/button.", 
                     f"Navigates to {target} successfully.", "P1")

            # 2. Notification (Implicit in Actions)
            if "action" in field.name.lower() or "hành động" in field.name.lower():
                 self._add_tc("Functional", f"Verify {field.name} - Notification Alert", 
                     "1. Perform Action (Approve/Reject).", 
                     "Notification 'Yêu cầu phê duyệt' appears in 'Activity Log'/'Nhận xét'.", "P2")

    def _expand_security_implicit(self, rule: BusinessRule):
         """ [NEW v2.2] Implicit Negative Security cases """
         desc = rule.description.lower()
         if "permission" in desc or "quyền" in desc:
             # Add explicit Unauthorized checks for non-approvers
             self._add_tc("Security", "Truy cập trái phép: Project Lead (không phải Approver) cố duyệt → Bị chặn", 
                     "1. Login as 'Project Lead' (Non-Approver).\n2. Try to Approve/Reject.", 
                     "Action Blocked / Buttons Hidden / Error 'Không được phép thao tác'.", "P1")
             self._add_tc("Security", "Truy cập trái phép: Task Lead (không phải Approver) cố duyệt → Bị chặn", 
                     "1. Login as 'Task Lead' (Non-Approver).\n2. Try to Approve/Reject.", 
                     "Action Blocked / Buttons Hidden / Error 'Không được phép thao tác'.", "P1")

    def _expand_approval_flows(self, rule: BusinessRule):
        """ [NEW] Smart Workflow-Aware Expansions """
        rid = rule.id.upper() if rule.id else ""
        desc = rule.description.lower()
        
        # Single vs Multi-Level Detection
        if "single" in desc or "1 level" in desc or "1 cấp" in desc:
             self._add_tc("Business Logic", "Workflow 1 cấp duy nhất: Approver duyệt xong → Trạng thái chuyển 'Completed' ngay",
                     "1. Request is Single Level.\n2. Approver Approves.",
                     "Status changes quickly to 'Completed' (Hoàn thành).", "P1")
        elif "multi" in desc or "nhiều cấp" in desc or "level" in desc:
             self._add_tc("Business Logic", "Workflow nhiều cấp: Level 1 duyệt xong → Chuyển Level 2 (chưa Completed)",
                     "1. Level 1 Approves.",
                     "Status changes to 'Pending Level 2' (Not Completed yet).", "P1")

             # Multi-level Continuation
             self._add_tc("Business Logic", "Workflow nhiều cấp: Tất cả level duyệt tuần tự → Trạng thái cuối 'Approved/Completed'",
                     "1. Level 1 Approve.\n2. Level 2 Approve.\n3. ... Level N Approve.",
                     "Final Status: Approved/Completed.", "P1")
             self._add_tc("Business Logic", "Workflow nhiều cấp: Level 2 từ chối giữa chừng → Quay về 'Rejected', quyết định Level 1 bị ghi đè",
                     "1. Level 1 Approve.\n2. Level 2 REJECT.",
                     "Status reverts to In Progress/Rejected. Level 1 decision overridden.", "P1")
             self._add_tc("Business Logic", "Workflow nhiều cấp: Level 1 chưa duyệt → Nút Level 2 bị disabled (ràng buộc thứ tự)",
                     "1. Level 1 Pending.\n2. Try to Approve as Level 2.",
                     "Action Blocked / Button Disabled.", "P2")
            
             # Visual Cues for Levels
             self._add_tc("Visual", "Gợi ý trực quan: Level 1 vs Level 2 Approver → Màu sắc/nhãn khác biệt rõ ràng",
                     "1. View Request as Level 1 and Level 2 Approvers.", 
                     "Check distinct colors/labels for different levels.", "P2")

    def _expand_concurrency(self, rule: BusinessRule):
        """ [NEW] Generates Concurrency/Group Logic """
        # [FIXED v2.3] Removed duplicate approval flow generation
        desc = rule.description.lower()
        if any(k in desc for k in ["any", "all", "đồng thuận", "nhóm", "group", "cùng 1 cấp"]):
             self._add_tc("Business Logic", "Cùng cấp có nhiều approver: User A duyệt trước → User B không cần thao tác nữa", 
                     "1. User A (Group 1) approves.\n2. User B (Group 1) views request.", 
                     "User B sees request as 'Approved' (No action needed).", "P1")
             self._add_tc("Business Logic", "Cùng cấp: 2 user bấm Approve đồng thời → Hệ thống xử lý không conflict", 
                     "1. User A and User B click 'Approve' at exact same time.", 
                     "System handles race condition (Single success or Idempotent).", "P2")

    def _expand_dependency_logic(self, section):
        """ [NEW] Scans fields for 'dependent' logic """
        for field in section.fields:
            if field.description and any(k in field.description.lower() for k in ["depend", "phụ thuộc", "theo"]):
                # Attempt to find parent field from description
                # Heuristic: verify if any other field name is in this description
                parent = next((f.name for f in section.fields if f.name in field.description and f.name != field.name), "Parent Field")
                
                self._add_tc("Business Logic", f"Verify {field.name} - Dependency on {parent} (Empty)", 
                     f"1. Leave '{parent}' empty/unselected.", 
                     f"'{field.name}' is Disabled or Empty.", "P1")
                self._add_tc("Business Logic", f"Verify {field.name} - Dependency on {parent} (Selected)", 
                     f"1. Select value in '{parent}'.", 
                     f"'{field.name}' becomes Enabled/Populated.", "P1")
                self._add_tc("Business Logic", f"Verify {field.name} - Dependency on {parent} (Changed)", 
                     f"1. Change value in '{parent}'.", 
                     f"'{field.name}' resets or updates options.", "P2")

    def deduplicate_test_cases(self, test_cases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        [NEW v3.0] Remove duplicate test cases based on semantic similarity.
        Merges duplicate rules into a single test case.
        """
        unique_cases = {}
        
        for tc in test_cases:
            # Create semantic key: Title + Steps (normalized) + Expected Result
            # Normalize steps to ignore minor formatting differences
            norm_steps = " ".join(tc['steps'].split()).lower()
            norm_expected = " ".join(tc['expected'].split()).lower()
            
            # Key focuses on the CORE LOGIC, not the random ID
            key = f"{tc['title']}|{norm_steps}|{norm_expected}"
            
            if key not in unique_cases:
                unique_cases[key] = tc
            else:
                # If duplicate found, we can merge metadata if needed
                # For now, we just keep the first one as it's likely from the most specific rule
                pass
                
        # Re-index IDs to be sequential after filtering
        final_list = list(unique_cases.values())
        for idx, tc in enumerate(final_list):
            tc['id'] = f"TC-{tc['category'][:4].upper()}-{idx + 1:03d}"
            
        return final_list

    class TestDataManager:
        """ [NEW v3.0] Manages realistic test data for Test Case generation """
        DATA_POOL = {
            "requester": ["Nguyễn Văn A", "Trần Thị B", "Lê Văn C", "Phạm Minh D"],
            "project": ["Dự án Pháp lý Q1 2026", "Tuân thủ GDPR", "Hệ thống CRM v2", "Migration AWS"],
            "region": ["Miền Bắc", "Miền Trung", "Miền Nam"],
            "area": ["Hà Nội", "Đà Nẵng", "TP.HCM", "Cần Thơ"],
            "content": ["Phê duyệt ngân sách Marketing", "Tuyển dụng nhân sự IT", "Mua sắm thiết bị văn phòng"],
            "description": ["Cần phê duyệt gấp trước ngày 15/02", "Dự án trọng điểm Q1", "Bổ sung tai nghe cho team Sales"],
            "status": ["Pending", "Approved", "Rejected", "Draft", "Cancelled"]
        }

        @staticmethod
        def get_example(field_name: str) -> str:
            name_lower = field_name.lower()
            if "requester" in name_lower or "người yêu cầu" in name_lower:
                return MatrixEngine.TestDataManager.DATA_POOL["requester"][0]
            if "project" in name_lower or "dự án" in name_lower:
                return MatrixEngine.TestDataManager.DATA_POOL["project"][0]
            if "region" in name_lower or "vùng" in name_lower:
                return MatrixEngine.TestDataManager.DATA_POOL["region"][0]
            if "area" in name_lower or "khu vực" in name_lower:
                return MatrixEngine.TestDataManager.DATA_POOL["area"][0]
            if "content" in name_lower or "nội dung" in name_lower:
                return MatrixEngine.TestDataManager.DATA_POOL["content"][0]
            return "Valid Value"

    def generate_all(self) -> List[Dict[str, Any]]:
        self.test_cases = []
        
        # 1. Expand Field Validations
        for section in self.schema.sections:
            # [NEW] Filter Combinations
            if "filter" in section.name.lower() or "search" in section.name.lower():
                self._expand_filter_combinations(section)
                self._expand_search_advanced(section) # [NEW v2.2]
            
            # [NEW] Dependency Logic
            self._expand_dependency_logic(section)
            self._expand_ui_ux_gaps(section) # [NEW v2.2]

            for field in section.fields:
                self._expand_field(field, section.name)
                # [NEW] Smart Actions Check
                self._expand_smart_actions(field, f"Verify {field.name}")
                # [NEW v2.3] Detail Popup Check
                self._expand_detail_popup(field, f"Verify {field.name}")
                
        # 2. Convert Business Rules (Upgraded)
        for rule in self.schema.business_rules:
            self._convert_rule_v2(rule)
            # [NEW] Semantic Explosion
            self._expand_roles_permissions(rule)
            self._expand_security_implicit(rule) # [NEW v2.2]
            self._expand_approval_flows(rule)    # [UPDATED v2.2]
            self._expand_concurrency(rule)
            
        # 3. Convert Visual Rules
        for vis in self.schema.visual_rules:
            self._convert_visual(vis)
            
        # 4. Add E2E Flows
        self._add_e2e_flows()
        
        # 5. Add Global Compatibility
        self._add_global_compatibility()
        
        # [NEW v3.0] Deduplicate
        self.test_cases = self.deduplicate_test_cases(self.test_cases)
            
        return self.test_cases

    def _add_e2e_flows(self):
        """
        Heuristic-based E2E flow generation.
        Detects "Create" and "List" sections to generate Happy Path TCs.
        """
        for section in self.schema.sections:
            s_name = section.name.lower()
            
            # --- Detect Create/Add Flow ---
            if any(k in s_name for k in ["create", "add", "new", "register"]):
                steps = [f"1. Open '{section.name}' screen."]
                step_count = 2
                
                # Fill required fields
                for field in section.fields:
                    if field.required:
                        action = "Select" if field.type in ["select", "radio"] else "Enter"
                        steps.append(f"{step_count}. {action} valid '{field.name}'.")
                        step_count += 1
                
                steps.append(f"{step_count}. Click 'Save' or 'Submit'.")
                
                self._add_tc("E2E", f"Verify {section.name} - Success (Happy Path)", 
                             "\n".join(steps), 
                             "Action successful. New record created/displayed.", "P0")

            # --- Detect List/Search Flow ---
            elif any(k in s_name for k in ["list", "search", "index", "filter"]):
                steps = [
                    f"1. Open '{section.name}' screen.",
                    "2. Enter valid Search Key.",
                    "3. Apply available Filters.",
                    "4. Verify results."
                ]
                self._add_tc("E2E", f"Verify {section.name} - Search & Filter Flow", 
                             "\n".join(steps), 
                             "Results match search criteria. UI is responsive.", "P1")

    def _add_global_compatibility(self):
        browsers = ["Chrome", "Firefox", "Safari", "Edge"]
        for browser in browsers:
            self._add_tc("Compatibility", f"Verify Layout on {browser}", 
                         f"1. Open feature on {browser}.\n2. Perform main flow.", 
                         "Layout matches design. No console errors.", "P1")
                         
        devices = ["iPhone 14 (Mobile)", "Samsung Galaxy S22", "Desktop 1920x1080"]
        for device in devices:
            self._add_tc("Compatibility", f"Verify Responsiveness: {device}", 
                         f"1. Emulate {device} viewport.", 
                         "UI adjusts correctly (Stacked/Grid).", "P2")

    def _generate_test_data_from_context(self, title: str, steps: str) -> str:
        """ [NEW v3.0] Smart Test Data Injection """
        context = (title + " " + steps).lower()
        data = []
        
        tm = self.TestDataManager
        
        if "requester" in context or "người yêu cầu" in context:
            data.append(f"Requester: {tm.get_example('requester')}")
            
        if "project" in context or "dự án" in context:
             data.append(f"Project: {tm.get_example('project')}")

        if "region" in context or "vùng" in context:
             data.append(f"Region: {tm.get_example('region')}")
             
        if "area" in context or "khu vực" in context:
             data.append(f"Area: {tm.get_example('area')}")
             
        if "content" in context or "nội dung" in context:
             data.append(f"Content: {tm.get_example('content')}")
             
        if "reason" in context or "lý do" in context:
             data.append(f"Reason: {tm.get_example('description')}")
             
        return "\n".join(data) if data else "-"

    def _add_tc(self, category: str, title: str, steps: str, expected: str, priority: str = "P2", test_data: str = None):
        # Auto-translate title to Vietnamese
        vietnamese_title = self._translate_title_to_vietnamese(title)
        
        # [NEW v3.0] Auto-generate test data if not provided
        if not test_data:
            test_data = self._generate_test_data_from_context(title, steps)
        
        tc_id = f"TC-{category[:4].upper()}-{len(self.test_cases) + 1:03d}"
        self.test_cases.append({
            "id": tc_id,
            "category": category,
            "title": vietnamese_title,  # Use Vietnamese title
            "steps": steps,
            "test_data": test_data,     # [NEW]
            "expected": expected,
            "priority": priority
        })

    def _expand_field(self, field: FieldType, section: str):
        prefix = f"Verify {field.name}"
        
        # --- Common Checks ---
        if field.required:
            self._add_tc("Validation", f"{prefix} - Empty (Required)", 
                         f"1. Leave '{field.name}' empty.\n2. Submit.",
                         "Error: Field is required.", "P1")

        # [NEW] Visual Check (Description/Tooltip)
        if field.description:
             self._add_tc("Visual", f"{prefix} - Tooltip/Help Text", 
                         f"1. Hover over info icon or check below field.",
                         f"Displays: '{field.description}'", "P3")
        
        # --- Type Specific Expansion ---
        if field.type in ["text", "password", "textarea"]:
            self._expand_text(field, prefix)
        elif field.type == "email":
            self._expand_email(field, prefix)
        elif field.type == "number":
            self._expand_number(field, prefix)
        elif field.type in ["select", "radio"]:
            self._expand_enum(field, prefix)
        elif field.type in ["chart", "list", "table", "label", "text_display"]:
            self._expand_display(field, prefix)
        elif field.type == "tree_view":
            self._expand_tree_view(field, prefix)
        elif field.type == "kanban_board":
            self._expand_kanban(field, prefix)
        elif field.type == "permission_matrix":
            self._expand_permission_matrix(field, prefix)
        elif field.type == "tabs":
            self._expand_tabs(field, prefix)
        elif field.type == "file_upload":
            self._expand_file_upload(field, prefix)
        elif field.type == "formula":
            self._expand_formula(field, prefix)
        elif field.type == "relationship":
            self._expand_relationship(field, prefix)
        elif field.type == "complex_view":
            self._expand_complex_view(field, prefix)

    def _expand_display(self, field: FieldType, prefix: str):
        if field.type == "table":
            self._expand_table(field, prefix)
        else:
            self._add_tc("Visual", f"{prefix} - Visibility", 
                         f"1. Check if '{field.name}' is visible.", 
                         "Element is displayed correctly.", "P2")

    def _expand_table(self, field: FieldType, prefix: str):
        # 1. Columns & Visibility
        self._add_tc("Visual", f"{prefix} - Verify Columns", 
                     "1. Check table headers.", 
                     f"Columns match PRD: {field.extra_props.get('columns', 'See PRD')}.", "P2")
        
        # 2. Sorting
        if field.extra_props.get("sortable", True):
            self._add_tc("Functional", f"{prefix} - Sort by Default", 
                         "1. Check default sort order.", 
                         "Sorted by Date (Newest) or PRD default.", "P2")
            self._add_tc("Functional", f"{prefix} - Sort by Name (A-Z)", 
                         "1. Click 'Name' header.", 
                         "List sorted alphabetically.", "P2")

        # 3. Pagination
        if field.extra_props.get("pagination", True):
            self._add_tc("Functional", f"{prefix} - Pagination Next/Prev", 
                         "1. Click Next page.", 
                         "Next set of records loaded.", "P2")
            self._add_tc("Performance", f"{prefix} - Large Dataset", 
                         "1. Load 1000+ records.", 
                         "Pagination handles data gracefully. No lag.", "P2")

        # 4. Filter Integration
        filters = field.extra_props.get("filters", [])
        for fil in filters:
            self._add_tc("Functional", f"{prefix} - Filter by {fil}", 
                         f"1. Apply filter '{fil}'.", 
                         "Table updates to show matching records.", "P1")
            
        # 5. Row Actions
        actions = field.extra_props.get("row_actions", ["View", "Edit", "Delete"])
        for action in actions:
            self._add_tc("Functional", f"{prefix} - Row Action: {action}", 
                         f"1. Click '{action}' on a row.", 
                         f"'{action}' triggered successfully.", "P1")

        # 6. Bulk Actions (Selection)
        if field.extra_props.get("bulk_actions", True):
            self._add_tc("Functional", f"{prefix} - Bulk Select All", 
                         "1. Click 'Select All' checkbox in header.", 
                         "All visible rows selected. Bulk Action menu appears.", "P2")
            self._add_tc("Functional", f"{prefix} - Bulk Delete (if applicable)", 
                         "1. Select multiple rows.\n2. Click 'Delete'.", 
                         "Selected rows deleted. List refreshes.", "P2")

        # 7. [NEW] Edge Cases
        self._add_tc("Visual", f"{prefix} - Empty State (No Data)",
                     "1. Apply filter that returns 0 results.",
                     "Show 'No Data' message/image. Table not broken.", "P2")
        self._add_tc("Visual", f"{prefix} - Long Content Handling",
                     "1. Create record with max length text.",
                     "Text truncated with ellipsis (...) or wrapped inside cell.", "P2")

    def _expand_text(self, field: FieldType, prefix: str):
        # Min Length
        if field.min_length:
            val_len = field.min_length
            self._add_tc("Validation", f"{prefix} - Min Length (-1)", 
                         f"1. Enter {val_len - 1} chars.", 
                         f"Error: Min {val_len} chars.")
            self._add_tc("Functional", f"{prefix} - Min Length (Valid)", 
                         f"1. Enter {val_len} chars.", 
                         "Accepted.")

        # Max Length (Buffer Overflow Check)
        if field.max_length:
            val_len = field.max_length
            self._add_tc("Functional", f"{prefix} - Max Length (Valid)", 
                         f"1. Enter {val_len} chars.", 
                         "Accepted.")
            self._add_tc("Validation", f"{prefix} - Max Length (+1)", 
                         f"1. Enter {val_len + 1} chars.", 
                         "Truncated or Error.")
            
        # --- Expanded Edge Cases ---
        self._add_tc("Functional", f"{prefix} - Trim Whitespace", 
                     f"1. Enter '  {field.name}  ' (spaces).", 
                     "Spaces trimmed. Accepted.")
        
        self._add_tc("Validation", f"{prefix} - Unicode/Emoji", 
                     f"1. Enter 'Name 🤡' or Chinese chars.", 
                     "Accepted (if UTF8) or Error (if strict ASCII).")

        # Security: XSS & Injection
        self._add_tc("Security", f"{prefix} - XSS Injection (<script>)", 
                     f"1. Enter '<script>alert(1)</script>'.", 
                     "Input sanitized/encoded. No popup.")
        
        self._add_tc("Security", f"{prefix} - HTML Injection", 
                     f"1. Enter '<b>Bold</b>' in '{field.name}'.", 
                     "Rendered as text, not HTML.")

        self._add_tc("Security", f"{prefix} - Null Byte Injection", 
                     f"1. Enter 'value%00' in '{field.name}'.", 
                     "Rejected or Sanitzed.")

        self._add_tc("Security", f"{prefix} - Command Injection", 
                     f"1. Enter '; cat /etc/passwd' or '| dir'.", 
                     "Rejected safe.")
        
        self._add_tc("Security", f"{prefix} - SQL Injection (Generic)", 
                     f"1. Enter ' OR 1=1;--.", 
                     "Handled safely.")

    def _expand_email(self, field: FieldType, prefix: str):
        # Standard Email Patterns
        patterns = [
            ("Missing @", "userdomain.com", "Error: Invalid format"),
            ("Missing Domain", "user@", "Error: Invalid format"),
            ("Missing TLD", "user@domain", "Error: Invalid format"),
            ("Special Chars", "us#er@domain.com", "Error: Invalid format if strict"),
            ("Double Dot", "user@domain..com", "Error: Invalid format"),
            ("Leading Dot", ".user@domain.com", "Error: Invalid format"),
            ("IP Domain", "user@[192.168.1.1]", "Accepted or Error (policy depending)"),
            ("Localhost", "user@localhost", "Accepted (internal) or Error (public)"),
        ]
        for name, payload, exp in patterns:
            self._add_tc("Validation", f"{prefix} - {name}", 
                         f"1. Enter '{payload}'.", exp)
                         
        self._add_tc("Security", f"{prefix} - SQL Injection", 
                     f"1. Enter \"' OR '1'='1\" in email.", 
                     "Handled safely.")

    def _expand_number(self, field: FieldType, prefix: str):
        if field.min_value is not None:
            self._add_tc("Validation", f"{prefix} - Min Value (-1)", 
                         f"1. Enter '{field.min_value - 1}'.", "Error: Value too low.")
            self._add_tc("Functional", f"{prefix} - Min Value (Valid)", 
                         f"1. Enter '{field.min_value}'.", "Accepted.")
                         
        if field.max_value is not None:
            self._add_tc("Functional", f"{prefix} - Max Value (Valid)", 
                         f"1. Enter '{field.max_value}'.", "Accepted.")
            self._add_tc("Validation", f"{prefix} - Max Value (+1)", 
                         f"1. Enter '{field.max_value + 1}'.", "Error: Value too high.")
            
        self._add_tc("Validation", f"{prefix} - Invalid Type (Text)", 
                     f"1. Enter 'abc'.", "Should not accept text.")
        
        self._add_tc("Validation", f"{prefix} - Negative Value", 
                     f"1. Enter '-10' (if unsigned).", "Error or converted.")

    def _expand_enum(self, field: FieldType, prefix: str):
        if field.options:
            for opt in field.options:
                self._add_tc("Functional", f"{prefix} - Select '{opt}'", 
                             f"1. Select option '{opt}'.", "Value selected.")
                             
        self._add_tc("Security", f"{prefix} - Invalid Option (Param Tampering)", 
                     f"1. Intercept request.\n2. Send value 'INVALID_OPT'.", 
                     "400 Bad Request or Error.")

 




    def _expand_tree_view(self, field: FieldType, prefix: str):
        # 1. Structure Navigation
        self._add_tc("Functional", f"{prefix} - Expand/Collapse Node", 
                     "1. Click expand icon (+).\n2. Click collapse icon (-).", 
                     "Tree expands/collapses correctly. Lazy loading works if applicable.", "P2")
        self._add_tc("Functional", f"{prefix} - Multi-level Hierarchy", 
                     "1. Create deep structure (Root -> L1 -> L2 -> Leaf).", 
                     "Hierarchy displayed correctly with indentation.", "P2")

        # 2. Search & Filter
        if field.extra_props.get("has_search", True):
            self._add_tc("Functional", f"{prefix} - Search by Name", 
                         "1. Enter valid node name in search box.", 
                         "Tree expands and highlights matching nodes.", "P1")
            self._add_tc("Functional", f"{prefix} - Search by Code/ID", 
                         "1. Enter valid node code.", 
                         "Tree auto-expands to result.", "P2")
            
        if field.extra_props.get("has_filter", True):
             self._add_tc("Functional", f"{prefix} - Filter by Status", 
                         "1. Apply filter 'Approved'.", 
                         "Only approved nodes shown. Structure preserved.", "P2")

        # 3. CRUD Operations (Folders/Docs)
        if field.extra_props.get("can_create_folder", True):
            self._add_tc("Functional", f"{prefix} - Create Folder", 
                         "1. Right-click Parent -> New Folder.\n2. Enter Name, Security Level.", 
                         "Folder created. Appears in tree.", "P0")
            self._add_tc("Functional", f"{prefix} - Rename Folder", 
                         "1. Right-click Folder -> Rename.\n2. Enter New Name.", 
                         "Name updated successfully.", "P2")
            self._add_tc("Validation", f"{prefix} - Create Folder - Duplicate Name", 
                         "1. Create folder with existing name in same parent.", 
                         "Error: Name already exists.", "P2")

        if field.extra_props.get("can_create_doc", True):
            self._add_tc("Functional", f"{prefix} - Create Document", 
                         "1. Right-click Folder -> New Document.\n2. Enter Code, Name.", 
                         "Document created.", "P0")

        if field.extra_props.get("can_delete", True):
            self._add_tc("Functional", f"{prefix} - Delete Folder (Empty)", 
                         "1. Select empty folder.\n2. Delete.", 
                         "Folder removed.", "P1")
            self._add_tc("Validation", f"{prefix} - Delete Folder (With Children)", 
                         "1. Select folder with children.\n2. Delete.", 
                         "Warning: Folder not empty OR Cascade delete prompt.", "P2")

        # 4. Organization
        if field.extra_props.get("can_drag_drop", True):
             self._add_tc("Functional", f"{prefix} - Drag & Drop Reorder", 
                         "1. Drag node A to new position within same parent.", 
                         "Order updated.", "P2")
             self._add_tc("Functional", f"{prefix} - Drag & Drop Move", 
                         "1. Drag node A into Folder B.", 
                         "Node A moves to Folder B.", "P2")

    def _expand_file_upload(self, field: FieldType, prefix: str):
        # 1. Functional Uploads
        exts = field.allowed_extensions or ["PDF", "DOCX", "JPG"]
        for ext in exts:
            self._add_tc("Functional", f"{prefix} - Upload {ext} File", 
                         f"1. Select valid .{ext} file.\n2. Upload.", 
                         "Upload success. Progress bar 100%.", "P1")

        # 2. Constraints
        if field.max_size_mb:
            self._add_tc("Validation", f"{prefix} - Max Size Exceeded", 
                         f"1. Select file > {field.max_size_mb}MB.", 
                         f"Error: File too large.", "P2")
            self._add_tc("Validation", f"{prefix} - Zero Byte File", 
                         "1. Select 0KB file.", 
                         "Error: File is empty.", "P2")
        
        # 3. Security (Critical)
        self._add_tc("Security", f"{prefix} - Malicious File (Shell)", 
                     "1. Upload 'shell.php' or 'exec.sh'.", 
                     "Server rejects file or quarantine.", "P1")
        self._add_tc("Security", f"{prefix} - Double Extension", 
                     "1. Upload 'image.jpg.exe'.", 
                     "Server checks final extension and rejects.", "P1")
        
        # 4. Advanced Features
        if field.extra_props.get("has_ocr", False):
            self._add_tc("Business Logic", f"{prefix} - OCR Processing", 
                         "1. Upload scan PDF.\n2. Wait for processing.", 
                         "Status changes to 'Processing' (Yellow) -> 'Done'. Text extracted.", "P2")
            
        if field.extra_props.get("has_versioning", False):
            self._add_tc("Functional", f"{prefix} - Upload New Version", 
                         "1. Upload file with same name/code as existing.", 
                         "System creates v2. History log updated.", "P1")

    def _expand_permission_matrix(self, field: FieldType, prefix: str):
        # 1. Role Capabilities (Enforcement)
        roles = field.extra_props.get("roles", ["Manage", "View", "Input", "Download"])
        for role in roles:
            self._add_tc("Security", f"{prefix} - Verify Role '{role}' Capabilities", 
                         f"1. Login as User with '{role}'.\n2. Attempt authorized actions.", 
                         "Success.", "P1")
            self._add_tc("Security", f"{prefix} - Verify Role '{role}' Restrictions", 
                         f"1. Login as User with '{role}'.\n2. Attempt UNAUTHORIZED actions (e.g. Delete).", 
                         "Access Denied / Button Hidden.", "P1")

        # 2. Assignment Logic
        self._add_tc("Functional", f"{prefix} - specific_user_assignment", 
                     "1. Select User -> Assign Role.", 
                     "User added to list with correct role.", "P1")
        self._add_tc("Functional", f"{prefix} - specific_unit_assignment", 
                     "1. Select Unit -> Assign Role.", 
                     "All members of Unit inherit role.", "P1")

        # 3. Inheritance & Conflict
        self._add_tc("Business Logic", f"{prefix} - Conflict Resolution", 
                     "1. User has 'View' (Direct) and 'Manage' (via Unit).", 
                     "System grants highest privilege (Manage).", "P1")

        # 4. Remove/Revoke
        self._add_tc("Functional", f"{prefix} - Remove Permission", 
                     "1. Remove User/Unit.", 
                     "Access revoked immediately.", "P1")
        self._add_tc("Business Logic", f"{prefix} - ManageBy Protection", 
                     "1. Try to remove Owner/Manager.", 
                     "Error: Cannot remove project owner.", "P2")

    def _expand_tabs(self, field: FieldType, prefix: str):
        # ... (Same as before)
        self._add_tc("Functional", f"{prefix} - Switch Tabs", 
                     "1. Click on different tab headers.", 
                     "Content switches instantly. No page reload.", "P2")
        self._add_tc("Visual", f"{prefix} - Active State", 
                     "1. Inspect active tab.", 
                     "Active tab highlighted/underlined.", "P2")

    def _expand_kanban(self, field: FieldType, prefix: str):
        cols = field.extra_props.get("columns", ["To Do", "In Progress", "Done"])
        
        # 1. Transitions
        for i in range(len(cols)-1):
            self._add_tc("Functional", f"{prefix} - Move Card {cols[i]} -> {cols[i+1]}", 
                         f"1. Drag card from '{cols[i]}' to '{cols[i+1]}'.", 
                         f"Card moved. Status updated to '{cols[i+1]}'.", "P1")

        # 2. Rules
        self._add_tc("Validation", f"{prefix} - Invalid Move", 
                     "1. Try to skip required step (if configured).", 
                     "Move rejected.", "P2")
                     
        # 3. Card Actions
        self._add_tc("Functional", f"{prefix} - View Card Detail", 
                     "1. Click on card.", 
                     "Popup details appear.", "P2")

    def _expand_formula(self, field: FieldType, prefix: str):
        # 1. Calculation Correctness
        expression = field.extra_props.get("expression", "Values")
        self._add_tc("Business Logic", f"{prefix} - Verify Calculation", 
                     f"1. Update dependent fields.\n2. Observe '{field.name}'.", 
                     f"Value calculated correctly using formula: {expression}", "P1")
        
        # 2. Trigger Events
        triggers = field.extra_props.get("triggers", ["On Save", "On Load"])
        for trig in triggers:
            self._add_tc("Functional", f"{prefix} - Trigger: {trig}", 
                         f"1. Perform action '{trig}'.", 
                         "Formula re-calculates automatically.", "P2")

        # 3. Edge Cases
        self._add_tc("Validation", f"{prefix} - Divide by Zero / Null", 
                     "1. Set dependent values to 0 or Null.", 
                     "Handled gracefully (No crash, shows 0 or Error).", "P2")

    def _expand_relationship(self, field: FieldType, prefix: str):
        target = field.extra_props.get("target_entity", "Item")
        cardinality = field.extra_props.get("cardinality", "1-n")
        
        # 1. Linking
        self._add_tc("Functional", f"{prefix} - Link {target}", 
                     f"1. Search for existing {target}.\n2. Select and Link.", 
                     f"{target} linked successfully. Appears in list.", "P1")
        
        # 2. Unlinking
        self._add_tc("Functional", f"{prefix} - Unlink {target}", 
                     f"1. Select linked {target}.\n2. Click Unlink/Remove.", 
                     "Link removed (Entity not deleted).", "P1")
        
        # 3. Cardinality Rules
        if "1" in cardinality: # 1-1 or n-1
             self._add_tc("Validation", f"{prefix} - Max Links Enforced", 
                          f"1. Try to link 2nd {target}.", 
                          "Error: Single connection only.", "P2")

        # 4. Navigation
        self._add_tc("Functional", f"{prefix} - Navigate to {target}", 
                     f"1. Click on linked {target} name.", 
                     f"Redirects to {target} details.", "P2")

    def _expand_complex_view(self, field: FieldType, prefix: str):
        tabs = field.extra_props.get("tabs", ["Info", "History"])
        
        # 1. Tab Visibility & Navigation
        for tab in tabs:
            self._add_tc("Visual", f"{prefix} - Tab Visibility: {tab}", 
                         f"1. Open Popup/View.\n2. Switch to '{tab}'.", 
                         f"Tab '{tab}' content displayed.", "P2")

        # 2. Actions
        actions = field.extra_props.get("actions", ["Download", "Print"])
        for action in actions:
            self._add_tc("Functional", f"{prefix} - Action: {action}", 
                         f"1. Click '{action}' button.", 
                         f"Action '{action}' executed successfully.", "P2")
                         
        # 3. Data Consistency
        self._add_tc("Data Integrity", f"{prefix} - Verify Data matches Source", 
                     "1. Compare Popup data with Grid/Source data.", 
                     "Data is identical.", "P1")

    def _convert_rule(self, rule: BusinessRule):
        self._add_tc("Business Logic", f"Verify Rule: {rule.description}", 
                     f"Condition: {rule.condition}", 
                     f"Result: {rule.expected_result}", 
                     priority=rule.priority)

    def _convert_visual(self, rule: VisualRule):
        self._add_tc("Visual", f"Verify Visual: {rule.element_name}", 
                     f"Inspect {rule.element_name}", 
                     rule.description, 
                     priority="P2")

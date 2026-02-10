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

    def _convert_rule_v2(self, rule: BusinessRule):
        """
        [NEW] Explodes 1 Business Rule into 3 scenarios (Positive, Negative, Boundary).
        """
        # Scenario 1: Happy Path (Positive)
        self._add_tc("Business Logic", f"Verify Rule {rule.id or ''}: {rule.description[:50]}... - Happy Path", 
                     f"Condition: {rule.condition} (Satisfied)", 
                     f"Result: {rule.expected_result}", 
                     priority=rule.priority)

        # Scenario 2: Negative Case (if applicable)
        keywords = ["if", "must", "only", "required", "restrict", 
                   "nếu", "chỉ", "bắt buộc", "không được", "phải"]
        if any(keyword in rule.description.lower() for keyword in keywords):
             self._add_tc("Business Logic", f"Verify Rule {rule.id or ''}: {rule.description[:50]}... - Negative Case", 
                     f"Condition: Violate '{rule.condition}'", 
                     "Result: Action blocked / Error message displayed.", 
                     priority="P2")

        # Scenario 3: State Transition (if detected)
        if "status" in rule.expected_result.lower() or "trạng thái" in rule.expected_result.lower():
             self._add_tc("Business Logic", f"Verify Rule {rule.id or ''}: State Transition Check", 
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

    def generate_all(self) -> List[Dict[str, Any]]:
        self.test_cases = []
        
        # 1. Expand Field Validations
        for section in self.schema.sections:
            # [NEW] Filter Combinations
            if "filter" in section.name.lower() or "search" in section.name.lower():
                self._expand_filter_combinations(section)

            for field in section.fields:
                self._expand_field(field, section.name)
                # [NEW] Smart Actions Check
                self._expand_smart_actions(field, f"Verify {field.name}")
                
        # 2. Convert Business Rules (Upgraded)
        for rule in self.schema.business_rules:
            self._convert_rule_v2(rule)
            
        # 3. Convert Visual Rules
        for vis in self.schema.visual_rules:
            self._convert_visual(vis)
            
        # 4. Add E2E Flows
        self._add_e2e_flows()

        # 5. Add Global Compatibility
        self._add_global_compatibility()
            
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

    def _add_tc(self, category: str, title: str, steps: str, expected: str, priority: str = "P2"):
        tc_id = f"TC-{category[:4].upper()}-{len(self.test_cases) + 1:03d}"
        self.test_cases.append({
            "id": tc_id,
            "category": category,
            "title": title,
            "steps": steps,
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

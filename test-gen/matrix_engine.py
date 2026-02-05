from typing import List, Dict, Any
from .schema_models import SmartSchema, FieldType, BusinessRule, VisualRule

class MatrixEngine:
    """
    The Factory: Converts a concise SmartSchema into a massive list of Test Cases.
    Applies BVA (Boundary Value Analysis), Equivalence Partitioning, and Security Baselines.
    """
    
    def __init__(self, schema: SmartSchema):
        self.schema = schema
        self.test_cases = []

    def generate_all(self) -> List[Dict[str, Any]]:
        self.test_cases = []
        
        # 1. Expand Field Validations (The "Explosion" source)
        for section in self.schema.sections:
            for field in section.fields:
                self._expand_field(field, section.name)
                
        # 2. Convert Business Rules to Functional TCs
        for rule in self.schema.business_rules:
            self._convert_rule(rule)
            
        # 3. Convert Visual Rules to Visual TCs
        for vis in self.schema.visual_rules:
            self._convert_visual(vis)
            
        # 4. Add Global Compatibility Checks (Mandatory for Validator)
        self._add_global_compatibility()
            
        return self.test_cases

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

    def _expand_display(self, field: FieldType, prefix: str):
        """
        New handler for Read-Only / Dashboard Elements (Charts, Lists, Labels)
        """
        # 1. Visibility Check
        self._add_tc("Visual", f"{prefix} - Visibility", 
                     f"1. Inspect '{field.name}'.", 
                     "Element is visible and aligned.", "P1")
        
        # 2. Data Accuracy (Dynamic Data)
        if field.type == "chart":
            self._add_tc("Functional", f"{prefix} - Data Rendering", 
                         f"1. Hover over chart points.", 
                         "Tooltip displays correct values.", "P2")
            self._add_tc("Functional", f"{prefix} - Empty State", 
                         f"1. Simulate 0 data.", 
                         "Chart shows 'No Data' or empty state.", "P2")
        
        elif field.type == "list" or field.type == "table":
             self._add_tc("Functional", f"{prefix} - List Check", 
                          f"1. Verify items in '{field.name}'.", 
                          "List items render correctly.", "P2")
             self._add_tc("Functional", f"{prefix} - Pagination/Load", 
                          f"1. Check if list has > 10 items.", 
                          "Pagination or Scroll works.", "P2")

        elif field.type == "label" or field.type == "text_display":
            self._add_tc("Functional", f"{prefix} - Content Check", 
                         f"1. Read text of '{field.name}'.", 
                         "Matches expected format/value.", "P2")

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

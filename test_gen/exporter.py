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

    def prepare_data_for_template(self, data: dict) -> dict:
        """
        Prepare dictionary with all variables needed for report generation
        """
        import sys
        sys.path.append(os.path.dirname(__file__))
        from template_engine import (
            calculate_statistics,
            categorize_testcases,
            extract_nft_categories
        )
        from datetime import datetime
        
        # Extract data
        if 'test_cases' in data and isinstance(data['test_cases'], list):
            test_cases = data['test_cases']
        else:
            test_cases = data.get('functional_testcases', []) + data.get('non_functional_testcases', [])
        metadata = data.get('metadata', {})
        
        if not test_cases:
            return {}
        
        # Categorize Functional vs Non-Functional
        functional, non_functional = categorize_testcases(test_cases)
        
        # Calculate statistics
        all_stats = calculate_statistics(test_cases)
        
        # Prepare template data with all variables
        return {
            # Metadata
            'feature_name': metadata.get('feature_name', 'Test Cases'),
            'prd_version': metadata.get('prd_version', '1.0.0'),
            'created_date': datetime.now().strftime('%Y-%m-%d'),
            'tester': metadata.get('tester', 'QA Team'),
            
            # Dashboard Statistics
            'total_cases': all_stats['total_cases'],
            'functional_count': len(functional),
            'non_functional_count': len(non_functional),
            'p0_count': all_stats['p0_count'],
            'p0_percent': all_stats['p0_percent'],
            'p1_count': all_stats['p1_count'],
            'p1_percent': all_stats['p1_percent'],
            'p2_count': all_stats['p2_count'],
            'p2_percent': all_stats['p2_percent'],
            'p3_count': all_stats['p3_count'],
            'p3_percent': all_stats['p3_percent'],
            
            # Test Cases Lists
            'functional_testcases': self._prepare_functional_data(functional, metadata),
            'non_functional_testcases': self._prepare_nonfunctional_data(non_functional),
            
            # NFT Categories
            'nft_categories': extract_nft_categories(non_functional)
        }

    def export_to_template_markdown(self, data: dict, template_path: str, output_filename: str = "test_cases.md") -> str:
        """
        Export test cases using Jinja2 template
        """
        import sys
        sys.path.append(os.path.dirname(__file__))
        from template_engine import render_template
        
        # Prepare data (handle both raw data dict and already prepared dict)
        if 'test_cases' in data and isinstance(data['test_cases'], list):
             # Raw data passed, prepare it
             template_data = self.prepare_data_for_template(data)
        else:
             # Already prepared or different structure (legacy support)
             template_data = data
             
        try:
            # Render template
            rendered = render_template(template_path, template_data)
            
            # Save to file
            filepath = os.path.join(self.output_dir, output_filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(rendered)
            
            return filepath
        except Exception as e:
            import traceback
            return f"Error rendering template: {e}\n{traceback.format_exc()}"
    
    def _prepare_functional_data(self, test_cases: list, metadata: dict = {}) -> list:
        """
        Prepare functional test cases for template
        Ensures all 11 required fields are present
        """
        import sys
        sys.path.append(os.path.dirname(__file__))
        from template_engine import format_test_data, format_steps
        
        prepared = []
        for tc in test_cases:
            prepared_tc = tc.copy()
            
            # Ensure all required fields with defaults
            prepared_tc.setdefault('module', metadata.get('feature_name', 'General'))
            prepared_tc.setdefault('pre_condition', 'User is logged in' if 'login' in str(tc.get('description', '')).lower() else '-')
            prepared_tc.setdefault('test_data', '-')
            prepared_tc.setdefault('status', '[ ] Pass / [ ] Fail / [ ] Skip / [ ] Blocked')
            prepared_tc.setdefault('created_date', datetime.now().strftime('%Y-%m-%d'))
            prepared_tc.setdefault('execute_date', '')
            
            # Map description to title if title is missing
            if 'title' not in prepared_tc and 'description' in prepared_tc:
                prepared_tc['title'] = prepared_tc['description']
            
            # Calculate step count for collapsible display
            if isinstance(prepared_tc.get('steps'), list):
                prepared_tc['step_count'] = len(prepared_tc['steps'])
                prepared_tc['steps'] = format_steps(prepared_tc['steps'])
            else:
                # Count steps by bullet separator
                steps_str = str(prepared_tc.get('steps', ''))
                prepared_tc['step_count'] = steps_str.count('•') + 1 if '•' in steps_str else 1
                # Format string steps (replace \n with <br> for display)
                # markdown_generator handles this but let's be safe
            
            # Create shortened version for simplified table
            steps_full = prepared_tc.get('steps', '-')
            if len(str(steps_full)) > 100:
                prepared_tc['steps_short'] = str(steps_full)[:100] + '...'
            else:
                prepared_tc['steps_short'] = steps_full
            
            # Simplified status for table
            prepared_tc['status_short'] = '[ ]'
            
            if prepared_tc.get('test_data') and prepared_tc['test_data'] != '-':
                prepared_tc['test_data'] = format_test_data(prepared_tc['test_data'])
            
            prepared.append(prepared_tc)
        
        return prepared
    
    def _prepare_nonfunctional_data(self, test_cases: list) -> list:
        """
        Prepare non-functional test cases for template
        Ensures all 9 required fields are present
        """
        import sys
        sys.path.append(os.path.dirname(__file__))
        from template_engine import format_steps
        
        # Extended mapping for both code types and full names
        type_to_category = {
            # Code types
            'SEC': 'Security',
            'PERF': 'Performance',
            'COMP': 'Compatibility',
            'UX': 'Usability',
            'ANA': 'Analytics',
            'AVAIL': 'Availability',
            'REL': 'Reliability',
            'ACCESS': 'Accessibility',
            
            # Full names (from AI output)
            'Security': 'Security',
            'Performance': 'Performance',
            'Compatibility': 'Compatibility',
            'Usability': 'Usability',
            'UI/UX': 'Usability',
            'Analytics': 'Analytics',
            'Availability': 'Availability',
            'Reliability': 'Reliability',
            'Accessibility': 'Accessibility'
        }
        
        prepared = []
        for tc in test_cases:
            prepared_tc = tc.copy()
            
            # Auto-derive category from type if not set
            tc_type = prepared_tc.get('type', '')
            if 'category' not in prepared_tc or not prepared_tc['category']:
                prepared_tc['category'] = type_to_category.get(tc_type, 'Other')

            # Map description to title if title is missing
            if 'title' not in prepared_tc and 'description' in prepared_tc:
                prepared_tc['title'] = prepared_tc['description']
            
            # Ensure all required fields
            prepared_tc.setdefault('tools', '-')
            
            # Map expected/expected_result to pass_criteria if not present
            if 'pass_criteria' not in prepared_tc or not prepared_tc['pass_criteria']:
                prepared_tc['pass_criteria'] = prepared_tc.get('expected_result') or prepared_tc.get('expected')

            prepared_tc.setdefault('pass_criteria', '-')
            prepared_tc.setdefault('created_date', '')
            prepared_tc.setdefault('execute_date', '')
            
            # Calculate step count for collapsible display
            if isinstance(prepared_tc.get('steps'), list):
                prepared_tc['step_count'] = len(prepared_tc['steps'])
                prepared_tc['steps'] = format_steps(prepared_tc['steps'])
            else:
                # Count steps by bullet separator  
                steps_str = str(prepared_tc.get('steps', ''))
                prepared_tc['step_count'] = steps_str.count('•') + 1 if '•' in steps_str else 1
            
            # Create shortened version for simplified table
            steps_full = prepared_tc.get('steps', '-')
            if len(str(steps_full)) > 100:
                prepared_tc['steps_short'] = str(steps_full)[:100] + '...'
            else:
                prepared_tc['steps_short'] = steps_full
            
            # Simplified status for table
            prepared_tc['status_short'] = '[ ]'
            
            prepared.append(prepared_tc)
        
        return prepared

if __name__ == "__main__":
    print("Exporter Initialized")

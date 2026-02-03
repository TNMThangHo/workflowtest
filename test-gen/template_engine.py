"""
Template Engine for Test Case Generation
Handles Jinja2 template rendering with statistics calculation
"""

from jinja2 import Environment, FileSystemLoader, select_autoescape
from typing import List, Dict, Any
from collections import Counter
from datetime import datetime
import os


def render_template(template_path: str, data: dict) -> str:
    """
    Load Jinja2 template and render with data
    
    Args:
        template_path: Path to template file (e.g., 'test-gen/templates/test-case-template.md')
        data: Dictionary containing all template variables
        
    Returns:
        Rendered markdown content
    """
    # Extract directory and filename
    template_dir = os.path.dirname(template_path)
    template_file = os.path.basename(template_path)
    
    # Create Jinja2 environment
    env = Environment(
        loader=FileSystemLoader(template_dir or '.'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    
    # Load and render template
    template = env.get_template(template_file)
    rendered = template.render(**data)
    
    return rendered


def calculate_statistics(test_cases: List[Dict[str, Any]]) -> dict:
    """
    Calculate dashboard statistics from test cases
    
    Args:
        test_cases: List of test case dictionaries
        
    Returns:
        Dictionary with counts and percentages for priorities
    """
    total = len(test_cases)
    
    if total == 0:
        return {
            'total_cases': 0,
            'p0_count': 0, 'p0_percent': 0,
            'p1_count': 0, 'p1_percent': 0,
            'p2_count': 0, 'p2_percent': 0,
            'p3_count': 0, 'p3_percent': 0
        }
    
    # Count by priority
    priorities = Counter([tc.get('priority', 'P2') for tc in test_cases])
    
    return {
        'total_cases': total,
        'p0_count': priorities.get('P0', 0),
        'p0_percent': round(priorities.get('P0', 0) / total * 100, 1),
        'p1_count': priorities.get('P1', 0),
        'p1_percent': round(priorities.get('P1', 0) / total * 100, 1),
        'p2_count': priorities.get('P2', 0),
        'p2_percent': round(priorities.get('P2', 0) / total * 100, 1),
        'p3_count': priorities.get('P3', 0),
        'p3_percent': round(priorities.get('P3', 0) / total * 100, 1)
    }


def categorize_testcases(test_cases: List[Dict[str, Any]]) -> tuple:
    """
    Separate Functional vs Non-Functional test cases
    
    Handles both:
    - Code types: FUNC, VAL
    - Full names: Functional, Validation
    
    Args:
        test_cases: List of test case dictionaries
        
    Returns:
        Tuple of (functional_tests, non_functional_tests)
    """
    functional = []
    non_functional = []
    
    # Define Functional types (both code and full names)
    functional_types = [
        'FUNC', 'VAL',  # Code types
        'Functional', 'Validation'  # Full names from AI
    ]
    
    for tc in test_cases:
        tc_type = tc.get('type', 'FUNC')
        
        # Check if it's a functional type
        if tc_type in functional_types:
            functional.append(tc)
        else:
            # Non-Functional: SEC, PERF, Security, Performance, etc.
            non_functional.append(tc)
    
    return functional, non_functional


def extract_nft_categories(non_functional: List[Dict[str, Any]]) -> list:
    """
    Extract unique Non-Functional Testing categories from test cases
    
    Handles both code types (SEC, PERF) and full names (Security, Performance)
    
    Args:
        non_functional: List of non-functional test cases
        
    Returns:
        Sorted list of unique category names
    """
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
    
    categories = set()
    
    for tc in non_functional:
        tc_type = tc.get('type', '')
        
        # If category is already set, use it
        if 'category' in tc and tc['category']:
            categories.add(tc['category'])
        # Otherwise derive from type
        elif tc_type in type_to_category:
            categories.add(type_to_category[tc_type])
    
    return sorted(list(categories))


def format_test_data(test_data: Any) -> str:
    """
    Format test data for display in template
    
    Args:
        test_data: Test data (can be dict, list, or string)
        
    Returns:
        Formatted string
    """
    if isinstance(test_data, dict):
        return ', '.join([f"{k}={v}" for k, v in test_data.items()])
    elif isinstance(test_data, list):
        return ', '.join([str(item) for item in test_data])
    else:
        return str(test_data) if test_data else '-'


def format_steps(steps: Any) -> str:
    """
    Format steps for display in template
    
    Args:
        steps: Steps (can be list or string)
        
    Returns:
        Formatted string with bullet separator
    """
    if isinstance(steps, list):
        return ' • '.join([str(step) for step in steps])
    else:
        return str(steps) if steps else '-'


if __name__ == "__main__":
    # Test the template engine
    print("Template Engine Initialized")
    print("Available functions:")
    print("  - render_template()")
    print("  - calculate_statistics()")
    print("  - categorize_testcases()")
    print("  - extract_nft_categories()")

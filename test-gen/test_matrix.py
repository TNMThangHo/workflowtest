import itertools
import json
import argparse
import sys
import os

from .logger import log

def generate_full_factorial(factors):
    """
    Generate Full Factorial combinations (Cartesian Product).
    factors: dict { "param_name": [val1, val2] }
    """
    keys = list(factors.keys())
    values = list(factors.values())
    
    combinations = list(itertools.product(*values))
    
    result = []
    for combo in combinations:
        # Zip keys with values to make readable dict
        scenario = dict(zip(keys, combo))
        result.append(scenario)
        
    return result

def load_matrix_def(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Test Matrix (Combinations)")
    parser.add_argument("--input", required=True, help="JSON Definition of Factors (e.g. {'Role': ['A','B'], 'Status': [1,0]})")
    parser.add_argument("--output", help="Output JSON file path", default="output/test_matrix.json")
    
    args = parser.parse_args()
    
    try:
        factors = load_matrix_def(args.input)
        
        matrix = generate_full_factorial(factors)
        
        output_data = {
            "strategy": "Full Factorial (Cartesian Product)",
            "total_scenarios": len(matrix),
            "scenarios": matrix
        }
        
        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2)
            
        log.info(f"Generated {len(matrix)} scenarios. Saved to {args.output}")
        
    except Exception as e:
        log.error(f"Error: {e}")
        sys.exit(1)

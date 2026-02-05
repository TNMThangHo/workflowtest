
import json
import os
from hypothesis import given, strategies as st
from hypothesis.strategies import emails, integers, text, characters
import random

# Keyword mapping to strategies
def get_strategy_for_keyword(text_content):
    text_content = text_content.lower()
    if "email" in text_content:
        return st.emails()
    if "age" in text_content or "quantity" in text_content or "number" in text_content:
        return st.integers(min_value=-100, max_value=1000)
    if "name" in text_content:
        return st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=1, max_size=20)
    if "xss" in text_content or "script" in text_content:
        # Custom strategy for XSS-like strings
        return st.sampled_from(["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"])
    return None

def generate_example(strategy):
    """Generate a single example from a strategy."""
    return strategy.example()

def enrich_test_cases(input_path="output/raw_testcases.json"):
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        return False
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ JSON Load Error: {e}")
        return False
    
    # Process Functional Test Cases
    enriched_count = 0
    all_tcs = data.get('functional_testcases', []) + data.get('non_functional_testcases', [])
    
    print(f"🔍 Scanning {len(all_tcs)} test cases for data enrichment potential...")
    
    for tc in all_tcs:
        # Check Title or Test Data for keywords
        target_text = (tc.get('title', '') + " " + tc.get('test_data', '')).lower()
        strategy = get_strategy_for_keyword(target_text)
        
        if strategy:
            # Generate 3 examples
            examples = []
            for _ in range(3):
                # We interpret the strategy manually since .example() is deprecated/discouraged for tests 
                # but okay for this specialized 'data gen' tool usage.
                # A robust way is usually `data.draw(strategy)` inside @given, 
                # but here we use the provider.
                try:
                    # Quick hack to get an example value
                    # In real impl we might use a dedicated generator instance
                    val = generate_example(strategy) 
                    examples.append(str(val))
                except:
                    pass
            
            if examples:
                # Append to Test Data
                current_data = tc.get('test_data', '')
                if current_data == '-' or current_data == '':
                    current_data = "Auto-Generated:"
                
                # Check for existing enrichment to avoid duplication/spam
                if "[Hypothesis Examples:" not in current_data:
                    enrichment = f" <br> **[Hypothesis Examples]:** `{', '.join(examples)}`"
                    tc['test_data'] = current_data + enrichment
                    enriched_count += 1


    # Save back
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Enriched {enriched_count} test cases with Hypothesis data.")
    return True

if __name__ == "__main__":
    enrich_test_cases()

import json
import os
import random
import string

# Simple data generators
def gen_email():
    domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    return f"{name}@{random.choice(domains)}"

def gen_int():
    return random.randint(-100, 1000)

def gen_text():
    chars = string.ascii_letters + string.digits + " "
    return ''.join(random.choices(chars, k=random.randint(5, 20)))

def gen_xss():
    payloads = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>", "javascript:alert(1)"]
    return random.choice(payloads)

# Keyword mapping
def get_example_for_keyword(text_content):
    text_content = text_content.lower()
    if "email" in text_content:
        return gen_email()
    if "age" in text_content or "quantity" in text_content or "number" in text_content:
        return gen_int()
    if "name" in text_content:
        return gen_text()
    if "xss" in text_content or "script" in text_content:
        return gen_xss()
    return None

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
    # Support both old and new schema
    all_tcs = data.get('test_cases', []) + data.get('functional_testcases', []) + data.get('non_functional_testcases', [])
    
    print(f"🔍 Scanning {len(all_tcs)} test cases for data enrichment potential...")
    
    for tc in all_tcs:
        # Check Title or Test Data for keywords
        target_text = (tc.get('title', '') + " " + tc.get('test_data', '')).lower()
        
        # Generate 3 examples
        examples = []
        for _ in range(3):
            val = get_example_for_keyword(target_text)
            if val:
                examples.append(str(val))
        
        if examples:
            # Sanitize examples for markdown table compatibility
            sanitized_examples = [sanitize_for_markdown(ex) for ex in examples]
            
            # Append to Test Data
            current_data = tc.get('test_data', '')
            if current_data == '-' or current_data == '':
                current_data = "Auto-Generated:"
            
            # Check for existing enrichment to avoid duplication/spam
            # [MODIFIED v3.1] Disabled Random Examples injection as per user feedback
            # if "[Random Examples:" not in current_data and "[Hypothesis Examples:" not in current_data:
            #     enrichment = f" <br> **[Random Examples]:** `{', '.join(sanitized_examples)}`"
            #     tc['test_data'] = current_data + enrichment
            #     enriched_count += 1
            pass


    # Save back
    with open(input_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Enriched {enriched_count} test cases with Hypothesis data.")
    return True

def sanitize_for_markdown(text):
    """Remove characters that break markdown tables."""
    if not text:
        return text
    
    # Remove control characters (including newlines, tabs, vertical tabs)
    sanitized = ''.join(char for char in text if ord(char) >= 32 or char in [' '])
    
    # Remove pipe characters that break tables
    sanitized = sanitized.replace('|', '/')
    
    # Limit length to prevent overflow
    if len(sanitized) > 30:
        sanitized = sanitized[:27] + "..."
    
    return sanitized

if __name__ == "__main__":
    enrich_test_cases()


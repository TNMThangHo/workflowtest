
from hypothesis import given, strategies as st
import sys
import os
import importlib.util

# --- DYNAMIC IMPORT FIX ---
# Since "test-gen" has a hyphen, we cannot use standard "import test-gen"
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
module_path = os.path.join(project_root, "test-gen", "markdown_generator.py")

spec = importlib.util.spec_from_file_location("markdown_generator", module_path)
markdown_generator = importlib.util.module_from_spec(spec)
sys.modules["markdown_generator"] = markdown_generator
spec.loader.exec_module(markdown_generator)

# Now we can import the function
generate_markdown_report = markdown_generator.generate_markdown_report
# ---------------------------

# Strategies for valid-ish but potentially dangerous text
text_strategy = st.text(alphabet=st.characters(blacklist_categories=("Cs",)), min_size=0, max_size=1000)
# Include markdown special chars, newlines, pipes
dangerous_text = st.text(alphabet=['|', '\n', '\r', '#', '*', '_', '<', '>', '&'], min_size=1, max_size=100)

# Combined text strategy
any_text = st.one_of(text_strategy, dangerous_text)

# Strategy for a Test Case Dictionary
test_case_strategy = st.fixed_dictionaries({
    "id": any_text,
    "module": any_text,
    "title": any_text,
    "pre_condition": any_text,
    "steps_short": any_text,
    "test_data": any_text,
    "expected_result": any_text,
    "status": any_text,
    "priority": st.one_of(st.just("P0"), st.just("P1"), st.just("P2"), st.just("P3"), any_text),
    "created_date": any_text,
    "execute_date": any_text,
    # NFT specific
    "category": any_text,
    "tools": any_text,
    "pass_criteria": any_text
})

# Strategy for the Main Input Dictionary
input_data_strategy = st.fixed_dictionaries({
    "feature_name": any_text,
    "prd_version": any_text,
    "tester": any_text,
    "functional_testcases": st.lists(test_case_strategy, max_size=20),
    "non_functional_testcases": st.lists(test_case_strategy, max_size=10),
    "nft_categories": st.lists(any_text, max_size=5)
})

@given(input_data_strategy)
def test_markdown_generator_robustness(data):
    """
    Fuzz test for generate_markdown_report.
    It should NEVER raise an exception, regardless of input content (as long as structure matches).
    """
    try:
        output = generate_markdown_report(data)
        assert isinstance(output, str)
        assert len(output) > 0
        # Basic sanity check: Header should always be there
        assert "# 📘 TÀI LIỆU TEST CASE" in output
        
    except Exception as e:
        print(f"\nCRASH DETECTED with input: {data}")
        raise e

if __name__ == "__main__":
    print("🚀 Running Hypothesis Fuzz Test for Markdown Generator...")
    try:
        test_markdown_generator_robustness()
        print("✅ Fuzz Test Passed! No crashes detected after default hypothesis runs.")
    except Exception as e:
        print(f"❌ Fuzz Test Failed: {e}")
        sys.exit(1)

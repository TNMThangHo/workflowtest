import argparse
import os
import subprocess
import sys
import json

def run_cmd(command):
    """Run a shell command and print status."""
    print(f"🔧 [Exec] {command}")
    try:
        # Use shell=True to handle python command on Windows vs Linux similarly
        result = subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e}")
        return False

def step_prepare():
    print("🚀 Starting Phase 1: PREPARE (Context Collection)...")
    
    context_report = {
        "specs": False,
        "matrix": False,
        "prd": False
    }

    # 1. Check & Run Swagger Parser
    swagger_path = os.path.join("input", "swagger.json")
    if os.path.exists(swagger_path):
        print(f"   -> Found Swagger: {swagger_path}")
        if run_cmd(f"python test-gen/parse_swagger.py --input {swagger_path} --output output/technical_specs.json"):
            context_report["specs"] = True
    else:
        # Check for mock
        mock_swagger = os.path.join("input", "mock_swagger.json")
        if os.path.exists(mock_swagger):
            print(f"   -> Found Mock Swagger: {mock_swagger}")
            if run_cmd(f"python test-gen/parse_swagger.py --input {mock_swagger} --output output/technical_specs.json"):
                context_report["specs"] = True

    # 2. Check & Run Matrix Generator
    matrix_input = os.path.join("input", "matrix_factors.json")
    if os.path.exists(matrix_input):
        print(f"   -> Found Matrix Definition: {matrix_input}")
        if run_cmd(f"python test-gen/test_matrix.py --input {matrix_input} --output output/test_matrix.json"):
             context_report["matrix"] = True
    else:
         # Check for mock
        mock_matrix = os.path.join("input", "mock_matrix.json")
        if os.path.exists(mock_matrix):
            print(f"   -> Found Mock Matrix: {mock_matrix}")
            if run_cmd(f"python test-gen/test_matrix.py --input {mock_matrix} --output output/test_matrix.json"):
                context_report["matrix"] = True

    # 3. Check PRD & References
    context_report["prd_files"] = []
    
    # Check for references.md
    ref_path = os.path.join("docs", "references.md")
    if os.path.exists(ref_path):
        context_report["references"] = True
        print(f"   -> Found Knowledge Base: {ref_path}")

    # Check for PRDs
    if os.path.exists("input"):
        for f in os.listdir("input"):
            if f.endswith(".md"):
                context_report["prd_files"].append(os.path.join("input", f))
                context_report["prd"] = True
        if context_report["prd"]:
             print(f"   -> Found {len(context_report['prd_files'])} PRD document(s).")

    # Save Context for Agent
    with open("output/run_context.json", "w") as f:
        json.dump(context_report, f, indent=2)
    
    print("\n✅ PREPARE Phase Complete. Ready for AI Generation.")
    print(json.dumps(context_report, indent=2))

def step_format():
    print("🚀 Starting Phase: FORMAT (JSON -> Markdown)...")
    
    # 1. Format JSON -> Markdown
    raw_json = os.path.join("output", "raw_testcases.json")
    if os.path.exists(raw_json):
        print("   -> Formatting Test Cases...")
        run_cmd(f"python test-gen/format_output.py --input {raw_json}")
        print("\n✅ FORMAT Complete. Check output/test_cases.md")
    else:
        print("❌ output/raw_testcases.json not found. Did AI generate it?")

def step_report():
    print("🚀 Starting Phase: REPORT (Markdown -> Excel)...")

    # 2. Analyze Markdown -> Excel Report
    test_cases_md = os.path.join("output", "test_cases.md")
    if os.path.exists(test_cases_md):
        print("   -> Generating Excel Report...")
        run_cmd(f"python test-gen/analyze_results.py --input {test_cases_md} --output-excel output/TEST_REPORT.xlsx")
        print("\n✅ REPORT Complete. Check output/TEST_REPORT.xlsx")
    else:
        print("❌ output/test_cases.md not found. Generate it first!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test Gen Orchestrator")
    parser.add_argument("--step", choices=["prepare", "format", "report"], required=True, help="Workflow step to execute")
    
    args = parser.parse_args()
    
    # Ensure output dir exists
    if not os.path.exists("output"):
        os.makedirs("output")

    if args.step == "prepare":
        step_prepare()
    elif args.step == "format":
        step_format()
    elif args.step == "report":
        step_report()

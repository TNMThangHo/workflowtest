import argparse
import sys
import os
import subprocess
import json
from .logger import log, setup_logger
from .markdown_parser import PRDParser

def setup_dirs():
    if not os.path.exists("output"):
        os.makedirs("output")
    if not os.path.exists("logs"):
        os.makedirs("logs")

def run_prepare():
    log.info("🚀 Starting Phase: PREPARE...")
    
    context = {"prd_files": []}
    
    # Check input dir
    if os.path.exists("input"):
        for f in os.listdir("input"):
            if f.endswith(".md"):
                fpath = os.path.join("input", f)
                parser = PRDParser(fpath)
                if parser.run():
                    context["prd_files"].append(fpath)
                    log.info(f"   -> Analyzed PRD: {f}")
    
    # Save context
    with open("output/run_context.json", "w") as f:
        json.dump(context, f, indent=2)
    
    log.info("✅ PREPARE Complete.")

def run_format(prd=None):
    log.info("🚀 Starting Phase: FORMAT...")
    
    raw_json = os.path.join("output", "raw_testcases.json")
    if not os.path.exists(raw_json):
        log.error("❌ raw_testcases.json not found.")
        return False

    # Call existing legacy formatter for now, or we could refactor it too.
    # Keeping legacy call to minimize risk, but wrapped in new logging.
    cmd = f"{sys.executable} test-gen/format_output.py --input {raw_json}"
    if prd:
        # If naming logic is needed
        pass 
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        log.info("✅ FORMAT Complete.")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"❌ Format failed: {e}")
        return False

def run_validate(prd_path):
    log.info("🚀 Starting Phase: VALIDATE...")
    
    testcases_path = "output/raw_testcases.json" # Validate JSON source
    if not os.path.exists(testcases_path):
        log.warning("JSON not found, trying Markdown...")
        testcases_path = "output/test_cases.md"
    
    # Import here to avoid circular imports if any, or just good practice
    from .validator import run_validate as validate_logic
    
    success = validate_logic(prd_path, testcases_path)
    if success:
        log.info("✅ VALIDATION PASSED.")
        return True
    else:
        log.error("❌ VALIDATION FAILED.")
        return False

def run_report(md_path):
    log.info("🚀 Starting Phase: REPORT...")
    if not os.path.exists(md_path):
        log.error(f"❌ Input file not found: {md_path}")
        return False
        
    from .reporter import Reporter
    rep = Reporter(md_path)
    rep.generate_excel("output/TEST_REPORT.xlsx")
    rep.generate_summary_md()
    return True

def run_sync(new_path, existing_path):
    log.info("🚀 Starting Phase: SYNC/UPDATE...")
    from .updater import Updater
    upd = Updater(new_path, existing_path)
    upd.sync(existing_path)
    return True

def main():
    setup_dirs()
    
    parser = argparse.ArgumentParser(description="Test Gen Orchestrator v2")
    parser.add_argument("--step", choices=["prepare", "format", "validate", "report", "sync"], required=True)
    parser.add_argument("--prd", help="Path to PRD file")
    parser.add_argument("--input", help="Input file for Report/Sync")
    parser.add_argument("--target", help="Target file for Sync")
    
    args = parser.parse_args()
    
    if args.step == "prepare":
        run_prepare()
    elif args.step == "format":
        run_format(args.prd)
    elif args.step == "validate":
        if not args.prd:
            log.error("❌ Validations requires --prd argument")
            sys.exit(1)
        if not run_validate(args.prd):
            sys.exit(1)
    elif args.step == "report":
        input_file = args.input or "output/test_cases.md"
        run_report(input_file)
    elif args.step == "sync":
        run_sync(args.input, args.target)

if __name__ == "__main__":
    main()

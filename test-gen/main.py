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

def run_format(prd=None, filename=None):
    log.info("🚀 Starting Phase: FORMAT...")
    
    raw_json = os.path.join("output", "raw_testcases.json")
    if not os.path.exists(raw_json):
        log.error("❌ raw_testcases.json not found.")
        return False

    # Call existing legacy formatter for now, or we could refactor it too.
    # Keeping legacy call to minimize risk, but wrapped in new logging.
    cmd = f"{sys.executable} -m test-gen.format_output --input {raw_json}"
    if filename:
        cmd += f" --filename {filename}"
    
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

def run_add(title, steps, expected, priority):
    log.info("🚀 Starting Phase: ADD TEST CASE...")
    from .manage import run_add_testcase
    run_add_testcase(title, steps, expected, priority)
    return True

def run_extract(prd_path):
    log.info("🚀 Starting Phase: STRICT EXTRACTION...")
    from .extractor import run_extraction
    run_extraction(prd_path)
    return True

def run_enrich():
    log.info("🚀 Starting Phase: HYPOTHESIS ENRICHMENT...")
    from .data_fuzzer import enrich_test_cases
    return enrich_test_cases()

def main():
    setup_dirs()
    
    parser = argparse.ArgumentParser(description="Test Gen Orchestrator v2")
    parser.add_argument("--step", choices=["prepare", "format", "validate", "report", "sync", "add", "extract", "init", "finish", "update-report", "enrich"], required=True)
    parser.add_argument("--prd", type=str, help="Path to PRD file")
    parser.add_argument("--filename", type=str, default="tc_001", help="Output filename for test cases")
    parser.add_argument("--input", type=str, help="Input file for report/sync")
    parser.add_argument("--target", type=str, help="Target file for sync")
    parser.add_argument("--report-file", type=str, help="Existing report file to update")
    
    # Args for Add Step
    parser.add_argument("--title", help="Test Case Title")
    parser.add_argument("--steps", help="Steps (semicolon separated)")
    parser.add_argument("--expected", help="Expected Result")
    parser.add_argument("--priority", default="P2", help="Priority")
    
    args = parser.parse_args()
    
    if args.step == "init":
        if not args.prd:
            log.error("❌ --prd is required for init step")
            sys.exit(1)
        run_prepare()
        run_extract(args.prd)
    elif args.step == "finish":
        if not args.prd:
            log.error("❌ --prd is required for finish step")
            sys.exit(1)
        
        # 1. Enrich (NEW)
        run_enrich() # Attempt to enrich before formatting

        # 2. Format
        fmt_success = run_format(args.prd, args.filename)
        if not fmt_success: sys.exit(1)
            
        # 3. Validate
        val_success = run_validate(args.prd)
        if not val_success: 
            log.warning("⚠️ Validation failed. Attempting Auto-Fix logic could go here.")
            # We don't exit here to allow Report to run if needed, or strictly exit?
            # User wants automation, so failing hard stops the flow. 
            # Let's keep strict for now but log distinct error.
            sys.exit(1)
            
    elif args.step == "prepare":
        run_prepare()
    elif args.step == "enrich":
        run_enrich()
    elif args.step == "extract":
        if not args.prd:
            log.error("❌ --prd is required for extraction")
            sys.exit(1)
        run_extract(args.prd)
    elif args.step == "format":
        run_format(args.prd, args.filename)
    elif args.step == "validate":
        if not args.prd:
            log.error("❌ Validations requires --prd argument")
            sys.exit(1)
        if not run_validate(args.prd):
            sys.exit(1)
    elif args.step == "report":
        input_file = args.input or "output/test_cases.md"
        run_report(input_file)
    elif args.step == "update-report":
        from .update_report import run_update_report
        if not args.input:
            log.error("❌ --input required for update-report")
            sys.exit(1)
        success = run_update_report(args.input, args.report_file)
        if not success:
            sys.exit(1)
    elif args.step == "sync":
        run_sync(args.input, args.target)
    elif args.step == "add":
        if not args.title:
            log.error("❌ --title is required for add step")
            sys.exit(1)
        run_add(args.title, args.steps, args.expected, args.priority)

if __name__ == "__main__":
    main()

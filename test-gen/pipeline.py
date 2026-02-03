"""
Auto-Resume Test Generation Pipeline
Eliminates the need for multiple command clicks by maintaining state.
"""
import sys
import os
import json
import subprocess
from pathlib import Path

STATE_FILE = "output/.pipeline_state.json"

def load_state():
    """Load current pipeline state"""
    if not os.path.exists(STATE_FILE):
        return {"stage": "init", "prd_path": None}
    with open(STATE_FILE, 'r') as f:
        return json.load(f)

def save_state(stage, prd_path=None):
    """Save current pipeline state"""
    os.makedirs("output", exist_ok=True)
    state = {"stage": stage, "prd_path": prd_path}
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)

def reset_state():
    """Reset pipeline to initial state"""
    if os.path.exists(STATE_FILE):
        os.remove(STATE_FILE)

def run_init(prd_path):
    """Run init phase (Prepare + Extract)"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from test_gen.main import run_prepare, run_extract
    print("🚀 Running INIT phase...")
    run_prepare()
    run_extract(prd_path)
    print("✅ INIT Complete. Requirements extracted.")

def run_finish(prd_path, filename="tc_auto"):
    """Run finish phase (Format + Validate)"""
    import sys
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from test_gen.main import run_format, run_validate
    print("🚀 Running FINISH phase...")
    
    if not run_format(prd_path, filename):
        print("❌ Format failed!")
        sys.exit(1)
    
    if not run_validate(prd_path):
        print("❌ Validation failed!")
        sys.exit(1)
    
    print("✅ FINISH Complete. Test cases ready!")

def main():
    if len(sys.argv) < 2:
        print("Usage: python -m test-gen.pipeline <prd_path> [--reset]")
        sys.exit(1)
    
    if "--reset" in sys.argv:
        reset_state()
        print("🔄 Pipeline state reset.")
        return
    
    prd_path = sys.argv[1]
    state = load_state()
    
    # Stage 1: INIT
    if state["stage"] == "init":
        run_init(prd_path)
        save_state("generate", prd_path)
        print("\n⏸️  PAUSED: Agent needs to generate raw_testcases.json")
        print("💡 Agent will auto-detect this file and resume pipeline.")
        sys.exit(0)  # Exit cleanly to allow Agent to continue
    
    # Stage 2: GENERATE (Check if ready)
    if state["stage"] == "generate":
        if not os.path.exists("output/raw_testcases.json"):
            print("⏳ Waiting for Agent to generate raw_testcases.json...")
            sys.exit(0)  # Not ready yet, exit gracefully
        
        print("✅ Detected raw_testcases.json! Proceeding to FINISH...")
        save_state("finish", prd_path or state["prd_path"])
        # Fall through to finish
    
    # Stage 3: FINISH
    if state["stage"] == "finish":
        actual_prd = prd_path if prd_path != "--check" else state["prd_path"]
        run_finish(actual_prd)
        save_state("done", actual_prd)
        reset_state()  # Clean up
        print("\n🎉 Pipeline COMPLETE!")

if __name__ == "__main__":
    main()

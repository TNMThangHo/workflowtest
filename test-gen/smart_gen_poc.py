import json
import sys
import os
from .schema_models import SmartSchema
from .matrix_engine import MatrixEngine

def run_poc(json_path: str):
    """
    Simulates Phase 2 (Python Factory) of the Smart Schema architecture.
    It reads a 'Smart Schema' JSON (produced by AI) and expands it into Test Cases.
    """
    print(f"🚀 [POC] Loading Schema from: {json_path}")
    
    if not os.path.exists(json_path):
        print(f"❌ Error: File not found: {json_path}")
        return

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)
        
        # 1. Validate Schema (Pydantic)
        print("🔍 Validating Schema against Pydantic Model...")
        schema = SmartSchema(**raw_data)
        print("✅ Schema Validated Successfully!")
        
        # 2. Run Matrix Engine
        print("💥 Running Matrix Engine (Explosion Strategy)...")
        engine = MatrixEngine(schema)
        test_cases = engine.generate_all()
        
        # 3. Report Results
        print(f"\n🎉 Generated {len(test_cases)} Test Cases from Schema!")
        print("-" * 50)
        
        # Print first 10 for review
        for i, tc in enumerate(test_cases[:10]):
            print(f"[{i+1}] {tc['id']}: {tc['title']}")
            print(f"    Step: {tc['steps']}")
            print(f"    Exp:  {tc['expected']}")
            print("-" * 20)
            
        if len(test_cases) > 10:
            print(f"... and {len(test_cases) - 10} more cases hidden.")

        # Save to file for inspection
        output_file = "output/poc_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({"test_cases": test_cases}, f, indent=2)
        print(f"\n💾 Full results saved to: {output_file}")

    except Exception as e:
        print(f"❌ Error during POC execution: {e}")

if __name__ == "__main__":
    # Ensure output dir exists
    os.makedirs("output", exist_ok=True)
    
    # Default to use a mockup file if not provided
    target_file = sys.argv[1] if len(sys.argv) > 1 else "output/schema_signup_mock.json"
    run_poc(target_file)

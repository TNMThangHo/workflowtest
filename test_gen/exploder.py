import json
import os
import sys

# Support dual import for package/standalone
try:
    from .schema_models import SmartSchema
    from .matrix_engine import MatrixEngine
    from .logger import log
except ImportError:
    from schema_models import SmartSchema
    from matrix_engine import MatrixEngine
    from logger import log

def run_explode(schema_path="output/schema_input.json", output_path="output/raw_testcases.json"):
    log.info(f"🚀 Starting Phase: SMART EXPLOSION (Matrix Engine)...")
    
    if not os.path.exists(schema_path):
        log.error(f"❌ Schema file not found: {schema_path}")
        return False
        
    try:
        # 1. Load Schema
        with open(schema_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Handle if schema is wrapped or raw
        if "feature_name" not in data and "sections" not in data:
            # Try finding nested key
            keys = list(data.keys())
            if keys:
                data = data[keys[0]]

        schema = SmartSchema(**data)
        log.info(f"   ✅ Schema Loaded: {schema.feature_name}")
        
        # 2. Initialize Matrix Engine
        engine = MatrixEngine(schema)
        
        # 3. Generate
        test_cases = engine.generate_all()
        log.info(f"   💥 Matrix Engine Exploded: {len(test_cases)} Test Cases")
        
        # 4. Save to raw_testcases.json
        output_data = {"test_cases": test_cases}
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
            
        log.info(f"   ✅ Saved to: {output_path}")
        return True
        
    except Exception as e:
        log.error(f"❌ Explosion Failed: {e}")
        import traceback
        log.error(traceback.format_exc())
        return False

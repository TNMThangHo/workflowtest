import json
import re
from typing import Optional
from .schema_models import SmartSchema

def clean_json_string(raw_text: str) -> str:
    """Clean markdown code blocks from LLM response"""
    if "```json" in raw_text:
        return raw_text.split("```json")[1].split("```")[0].strip()
    if "```" in raw_text:
        return raw_text.split("```")[1].split("```")[0].strip()
    return raw_text.strip()

def parse_schema_from_ai(ai_response: str) -> Optional[SmartSchema]:
    """
    Parses raw AI text into a strict SmartSchema object.
    Returns None if parsing fails.
    """
    try:
        clean_json = clean_json_string(ai_response)
        data = json.loads(clean_json)
        
        # Validate with Pydantic
        schema = SmartSchema(**data)
        return schema
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON Parse Error: {e}")
        return None
    except Exception as e:
        print(f"❌ Schema Validation Error: {e}")
        return None

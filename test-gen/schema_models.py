from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field

# --- Enums & Constraints ---

class FieldType(BaseModel):
    name: str
    type: Literal["text", "email", "password", "number", "date", "select", "checkbox", "radio", "textarea", "file", "chart", "list", "table", "label", "text_display"]
    required: bool = True
    
    # Text/Password Constraints
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    regex: Optional[str] = None
    
    # Number Constraints
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    
    # Select/Radio Constraints
    options: Optional[List[str]] = None
    
    # File Constraints
    allowed_extensions: Optional[List[str]] = None
    max_size_mb: Optional[int] = None

class BusinessRule(BaseModel):
    id: str
    description: str
    condition: str
    expected_result: str
    priority: Literal["P0", "P1", "P2"] = "P1"

class VisualRule(BaseModel):
    element_name: str
    description: str 
    # e.g., "Button color must be #007bff", "Stacked on mobile"

class Section(BaseModel):
    name: str # e.g. "Personal Info", "Payment Details"
    fields: List[FieldType] = []

# --- Root Schema (AI Output Target) ---

class SmartSchema(BaseModel):
    feature_name: str
    sections: List[Section] = []
    business_rules: List[BusinessRule] = []
    visual_rules: List[VisualRule] = []
    
    # Metadata for tracking
    version: str = "5.0"

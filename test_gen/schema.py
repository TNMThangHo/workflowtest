from dataclasses import dataclass, field, asdict
from typing import List, Optional, Literal
import json

@dataclass
class TestCase:
    id: str
    title: str
    pre_condition: str
    steps: List[str]
    expected_result: str
    type: str  # Functional, Security, Performance, UI/UX, etc.
    priority: str  # P0, P1, P2, P3
    status: Optional[str] = None  # To be filled during execution
    notes: Optional[str] = ""

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", ""),
            title=data.get("title", ""),
            pre_condition=data.get("pre_condition", ""),
            steps=data.get("steps", []) if isinstance(data.get("steps"), list) else [str(data.get("steps", ""))],
            expected_result=data.get("expected_result", ""),
            type=data.get("type", "Functional"),
            priority=data.get("priority", "P1"),
            status=data.get("status"),
            notes=data.get("notes", "")
        )

@dataclass
class TestSuite:
    test_cases: List[TestCase] = field(default_factory=list)

    def to_json(self, indent=2):
        return json.dumps({"test_cases": [tc.to_dict() for tc in self.test_cases]}, ensure_ascii=False, indent=indent)

    @classmethod
    def from_json_file(cls, filepath: str):
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            # Check for legacy flat list
            if "test_cases" in data:
                cases_data = data["test_cases"]
            else:
                # Handle new sectioned structure
                cases_data = data.get("functional_testcases", []) + data.get("non_functional_testcases", [])
        else:
            cases_data = data
        
        return cls(test_cases=[TestCase.from_dict(tc) for tc in cases_data])

@dataclass
class PRDSection:
    heading: str
    content: str
    subsections: List['PRDSection'] = field(default_factory=list)

# module_analysis_engine/parsers/base_parser.py
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class CodeIssue:
    """Represents a code issue found during analysis"""
    file_path: str
    line_start: int
    line_end: int
    column_start: int
    column_end: int
    rule_id: str
    message: str
    severity: str  # critical, high, medium, low
    issue_type: str  # bug, vulnerability, code_smell, performance
    suggestion: Optional[str] = None
    code_snippet: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "file_path": self.file_path,
            "location": {
                "start": {"line": self.line_start, "column": self.column_start},
                "end": {"line": self.line_end, "column": self.column_end}
            },
            "rule_id": self.rule_id,
            "message": self.message,
            "severity": self.severity,
            "type": self.issue_type,
            "suggestion": self.suggestion,
            "code_snippet": self.code_snippet,
            "metadata": self.metadata
        }

class BaseParser(ABC):
    """Abstract base class for all language parsers"""
    
    def __init__(self, language: str):
        self.language = language
        self.issues: List[CodeIssue] = []
        
    @abstractmethod
    def parse(self, code: str, file_path: str) -> List[CodeIssue]:
        """Parse code and return list of issues"""
        pass
    
    @abstractmethod
    def get_supported_rules(self) -> List[str]:
        """Return list of supported rule IDs"""
        pass
    
    def add_issue(self, issue: CodeIssue):
        """Add an issue to the list"""
        self.issues.append(issue)
    
    def clear_issues(self):
        """Clear all issues"""
        self.issues = []
    
    def get_issues(self) -> List[CodeIssue]:
        """Get all issues found"""
        return self.issues
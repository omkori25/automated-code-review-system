# module_analysis_engine/rules/rule_manager.py
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
import json
import yaml
import os
from pathlib import Path

@dataclass
class Rule:
    """Represents an analysis rule"""
    id: str
    name: str
    description: str
    severity: str  # critical, high, medium, low
    category: str  # security, performance, code_smell, bug
    languages: List[str]
    pattern: Optional[str] = None
    enabled: bool = True
    custom: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "severity": self.severity,
            "category": self.category,
            "languages": self.languages,
            "pattern": self.pattern,
            "enabled": self.enabled,
            "custom": self.custom,
            "metadata": self.metadata
        }

class RuleManager:
    """Manages analysis rules"""
    
    def __init__(self, rules_path: str = None):
        self.rules_path = rules_path or os.path.join(
            os.path.dirname(__file__), "rules_data"
        )
        self.rules: Dict[str, Rule] = {}
        self.categories = {
            "security": "🔒 Security",
            "performance": "⚡ Performance", 
            "code_smell": "👃 Code Smell",
            "bug": "🐛 Bug Risk"
        }
        
        # Create rules directory if it doesn't exist
        Path(self.rules_path).mkdir(parents=True, exist_ok=True)
        
        # Load built-in rules
        self._load_builtin_rules()
        
        # Load custom rules
        self._load_custom_rules()
    
    def _load_builtin_rules(self):
        """Load built-in rules for all languages"""
        
        # =========================================
        # PYTHON RULES
        # =========================================
        
        # Python - Imports
        self.add_rule(Rule(
            id="PY001",
            name="Wildcard Import",
            description="Avoid wildcard imports (from module import *)",
            severity="medium",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Python - Functions
        self.add_rule(Rule(
            id="PY002",
            name="Long Function",
            description="Function is too long, consider breaking it down",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"max_lines": 50, "effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="PY003",
            name="Too Many Parameters",
            description="Function has too many parameters",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"max_params": 5, "effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="PY006",
            name="Missing Return Type Hint",
            description="Function missing return type hint",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Python - Classes
        self.add_rule(Rule(
            id="PY004",
            name="God Class",
            description="Class has too many methods",
            severity="medium",
            category="code_smell",
            languages=["python"],
            metadata={"max_methods": 15, "effort": "high"}
        ))
        
        self.add_rule(Rule(
            id="PY007",
            name="Missing __init__ Method",
            description="Class missing __init__ method",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        # Python - Exceptions
        self.add_rule(Rule(
            id="PY005",
            name="Bare Except",
            description="Bare except clause catches all exceptions",
            severity="high",
            category="bug",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="PY008",
            name="Too Broad Except",
            description="Catching Exception is too broad",
            severity="medium",
            category="bug",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        # Python - Security
        self.add_rule(Rule(
            id="SEC001",
            name="Eval Usage",
            description="Use of eval/exec is dangerous",
            severity="critical",
            category="security",
            languages=["python"],
            metadata={"effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="SEC002",
            name="Hardcoded Secret",
            description="Hardcoded password or token detected",
            severity="high",
            category="security",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="SEC003",
            name="SQL Injection",
            description="Possible SQL injection vulnerability",
            severity="critical",
            category="security",
            languages=["python"],
            metadata={"effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="SEC004",
            name="Unsafe Pickle",
            description="Using pickle on untrusted data is dangerous",
            severity="high",
            category="security",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="SEC005",
            name="Shell Injection",
            description="Potential shell injection vulnerability",
            severity="critical",
            category="security",
            languages=["python"],
            metadata={"effort": "high"}
        ))
        
        # Python - Complexity
        self.add_rule(Rule(
            id="CMP001",
            name="High Complexity",
            description="Function has high cyclomatic complexity",
            severity="medium",
            category="performance",
            languages=["python"],
            metadata={"max_complexity": 10, "effort": "high"}
        ))
        
        # Python - Naming
        self.add_rule(Rule(
            id="NAM001",
            name="Class Naming",
            description="Class names should use CamelCase",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="NAM002",
            name="Function Naming",
            description="Function names should use snake_case",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="NAM003",
            name="Variable Naming",
            description="Variable names should use snake_case",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Python - Documentation
        self.add_rule(Rule(
            id="DOC001",
            name="Module Docstring",
            description="Module missing docstring",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="DOC002",
            name="Function Docstring",
            description="Function missing docstring",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="DOC003",
            name="Class Docstring",
            description="Class missing docstring",
            severity="low",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low"}
        ))
        
        # Python - Bugs
        self.add_rule(Rule(
            id="MUT001",
            name="Mutable Default Arguments",
            description="Mutable default argument detected",
            severity="high",
            category="bug",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # =========================================
        # JAVASCRIPT / TYPESCRIPT RULES
        # =========================================
        
        # JavaScript - Security
        self.add_rule(Rule(
            id="JS_SEC001",
            name="JavaScript Eval Usage",
            description="Use of eval() is dangerous and can lead to code injection",
            severity="critical",
            category="security",
            languages=["javascript", "typescript"],
            metadata={"effort": "low", "auto_fixable": False}
        ))
        
        self.add_rule(Rule(
            id="JS_SEC002",
            name="setTimeout with String",
            description="setTimeout with string argument is dangerous (similar to eval)",
            severity="high",
            category="security",
            languages=["javascript", "typescript"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="JS_SEC003",
            name="document.write Usage",
            description="document.write() can lead to XSS vulnerabilities",
            severity="high",
            category="security",
            languages=["javascript"],
            metadata={"effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="JS_SEC004",
            name="innerHTML with Dynamic Content",
            description="innerHTML with dynamic content can lead to XSS",
            severity="high",
            category="security",
            languages=["javascript", "typescript"],
            metadata={"effort": "medium"}
        ))
        
        # JavaScript - Functions
        self.add_rule(Rule(
            id="JS_FUNC001",
            name="Long JavaScript Function",
            description="Function is too long, consider breaking it down",
            severity="low",
            category="code_smell",
            languages=["javascript", "typescript"],
            metadata={"max_lines": 30, "effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="JS_FUNC002",
            name="Too Many Parameters",
            description="Function has too many parameters",
            severity="low",
            category="code_smell",
            languages=["javascript", "typescript"],
            metadata={"max_params": 5, "effort": "low"}
        ))
        
        # JavaScript - Global
        self.add_rule(Rule(
            id="JS_GLOB001",
            name="Global Namespace Pollution",
            description="Too many global variables pollute the global namespace",
            severity="medium",
            category="code_smell",
            languages=["javascript"],
            metadata={"max_globals": 5, "effort": "high"}
        ))
        
        # JavaScript - Async
        self.add_rule(Rule(
            id="JS_ASYNC001",
            name="Missing await with fetch",
            description="fetch() called without await in async function",
            severity="medium",
            category="bug",
            languages=["javascript", "typescript"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # JavaScript - React
        self.add_rule(Rule(
            id="JS_REACT001",
            name="Hook Called Outside Component",
            description="React hooks must be called in function components",
            severity="high",
            category="bug",
            languages=["javascript", "typescript"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="JS_REACT002",
            name="Missing Key Prop",
            description="Missing 'key' prop in list rendering",
            severity="medium",
            category="bug",
            languages=["javascript", "typescript"],
            metadata={"effort": "low", "auto_fixable": False}
        ))
        
        # =========================================
        # JAVA RULES
        # =========================================
        
        # Java - Security
        self.add_rule(Rule(
            id="JAVA_SEC001",
            name="Runtime.exec() Usage",
            description="Runtime.exec() can lead to command injection",
            severity="critical",
            category="security",
            languages=["java"],
            metadata={"effort": "high"}
        ))
        
        self.add_rule(Rule(
            id="JAVA_SEC002",
            name="SQL Injection",
            description="Possible SQL injection vulnerability",
            severity="critical",
            category="security",
            languages=["java"],
            metadata={"effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="JAVA_SEC003",
            name="Insecure Deserialization",
            description="Insecure deserialization detected",
            severity="high",
            category="security",
            languages=["java"],
            metadata={"effort": "high"}
        ))
        
        # Java - Exceptions
        self.add_rule(Rule(
            id="JAVA_EXC001",
            name="Empty Catch Block",
            description="Empty catch block detected",
            severity="medium",
            category="bug",
            languages=["java"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="JAVA_EXC002",
            name="Generic Exception Catch",
            description="Catching generic Exception is too broad",
            severity="medium",
            category="code_smell",
            languages=["java"],
            metadata={"effort": "low"}
        ))
        
        # Java - Serialization
        self.add_rule(Rule(
            id="JAVA_SER001",
            name="Missing serialVersionUID",
            description="Serializable class missing serialVersionUID",
            severity="medium",
            category="code_smell",
            languages=["java"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Java - Naming
        self.add_rule(Rule(
            id="JAVA_NAM001",
            name="Class Naming Convention",
            description="Class names should start with uppercase letter",
            severity="low",
            category="code_smell",
            languages=["java"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="JAVA_NAM002",
            name="Method Naming Convention",
            description="Method names should start with lowercase letter",
            severity="low",
            category="code_smell",
            languages=["java"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="JAVA_NAM003",
            name="Constant Naming Convention",
            description="Constants should be UPPER_SNAKE_CASE",
            severity="low",
            category="code_smell",
            languages=["java"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Java - Complexity
        self.add_rule(Rule(
            id="JAVA_CMP001",
            name="God Class",
            description="Class has too many methods",
            severity="medium",
            category="code_smell",
            languages=["java"],
            metadata={"max_methods": 15, "effort": "high"}
        ))
        
        # =========================================
        # GENERAL RULES (All Languages)
        # =========================================
        
        self.add_rule(Rule(
            id="GEN001",
            name="TODO Comment",
            description="TODO comment found - indicates incomplete code",
            severity="low",
            category="code_smell",
            languages=["python", "javascript", "typescript", "java", "go", "rust"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="GEN002",
            name="FIXME Comment",
            description="FIXME comment found - indicates known issue",
            severity="medium",
            category="bug",
            languages=["python", "javascript", "typescript", "java", "go", "rust"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="GEN003",
            name="Debug Print Statement",
            description="Debug print statement found in production code",
            severity="low",
            category="code_smell",
            languages=["python", "javascript", "typescript", "java"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        self.add_rule(Rule(
            id="GEN004",
            name="Empty File",
            description="File contains no code",
            severity="low",
            category="code_smell",
            languages=["python", "javascript", "typescript", "java"],
            metadata={"effort": "low"}
        ))
    
    def _load_custom_rules(self):
        """Load custom rules from files"""
        custom_rules_file = os.path.join(self.rules_path, "custom_rules.json")
        if os.path.exists(custom_rules_file):
            try:
                with open(custom_rules_file, 'r') as f:
                    rules_data = json.load(f)
                    for rule_data in rules_data:
                        rule = Rule(**rule_data)
                        self.add_rule(rule)
            except Exception as e:
                print(f"Error loading custom rules: {e}")
    
    def add_rule(self, rule: Rule):
        """Add a rule"""
        self.rules[rule.id] = rule
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get rule by ID"""
        return self.rules.get(rule_id)
    
    def get_rules_by_language(self, language: str) -> List[Rule]:
        """Get all rules for a specific language"""
        return [
            rule for rule in self.rules.values()
            if language in rule.languages and rule.enabled
        ]
    
    def get_rules_by_category(self, category: str) -> List[Rule]:
        """Get all rules in a category"""
        return [
            rule for rule in self.rules.values()
            if rule.category == category and rule.enabled
        ]
    
    def get_rules_by_severity(self, severity: str) -> List[Rule]:
        """Get all rules with specific severity"""
        return [
            rule for rule in self.rules.values()
            if rule.severity == severity and rule.enabled
        ]
    
    def disable_rule(self, rule_id: str):
        """Disable a rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = False
    
    def enable_rule(self, rule_id: str):
        """Enable a rule"""
        if rule_id in self.rules:
            self.rules[rule_id].enabled = True
    
    def add_custom_rule(self, rule: Rule):
        """Add a custom rule and save to file"""
        rule.custom = True
        self.add_rule(rule)
        self._save_custom_rules()
    
    def _save_custom_rules(self):
        """Save custom rules to file"""
        custom_rules = [
            rule.to_dict() for rule in self.rules.values()
            if rule.custom
        ]
        
        custom_rules_file = os.path.join(self.rules_path, "custom_rules.json")
        try:
            with open(custom_rules_file, 'w') as f:
                json.dump(custom_rules, f, indent=2)
        except Exception as e:
            print(f"Error saving custom rules: {e}")
    
    def validate_rule(self, rule_data: Dict) -> bool:
        """Validate rule data"""
        required_fields = ['id', 'name', 'description', 'severity', 'category', 'languages']
        
        # Check required fields
        for field in required_fields:
            if field not in rule_data:
                return False
        
        # Validate severity
        if rule_data['severity'] not in ['critical', 'high', 'medium', 'low']:
            return False
        
        # Validate category
        if rule_data['category'] not in self.categories:
            return False
        
        # Validate languages is a list
        if not isinstance(rule_data['languages'], list):
            return False
        
        return True
    
    def export_rules(self, format: str = 'json') -> str:
        """Export all rules in specified format"""
        if format == 'json':
            return json.dumps(
                [rule.to_dict() for rule in self.rules.values()],
                indent=2
            )
        elif format == 'yaml':
            return yaml.dump(
                [rule.to_dict() for rule in self.rules.values()]
            )
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_rules(self, data: str, format: str = 'json'):
        """Import rules from file"""
        try:
            if format == 'json':
                rules_data = json.loads(data)
            elif format == 'yaml':
                rules_data = yaml.safe_load(data)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            for rule_data in rules_data:
                if self.validate_rule(rule_data):
                    rule = Rule(**rule_data)
                    self.add_rule(rule)
        except Exception as e:
            print(f"Error importing rules: {e}")
    
    def get_statistics(self) -> Dict:
        """Get rule statistics"""
        rules_list = list(self.rules.values())
        
        return {
            "total_rules": len(rules_list),
            "by_category": {
                category: len([r for r in rules_list if r.category == category])
                for category in self.categories.keys()
            },
            "by_severity": {
                severity: len([r for r in rules_list if r.severity == severity])
                for severity in ['critical', 'high', 'medium', 'low']
            },
            "by_language": {
                "python": len([r for r in rules_list if 'python' in r.languages]),
                "javascript": len([r for r in rules_list if 'javascript' in r.languages]),
                "typescript": len([r for r in rules_list if 'typescript' in r.languages]),
                "java": len([r for r in rules_list if 'java' in r.languages]),
                "go": len([r for r in rules_list if 'go' in r.languages]),
                "rust": len([r for r in rules_list if 'rust' in r.languages]),
            },
            "enabled_rules": len([r for r in rules_list if r.enabled]),
            "custom_rules": len([r for r in rules_list if r.custom])
        }

# Create singleton instance
rule_manager = RuleManager()
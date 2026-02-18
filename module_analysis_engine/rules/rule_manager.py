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
        """Load built-in rules"""
        # Python rules
        self.add_rule(Rule(
            id="PY001",
            name="Wildcard Import",
            description="Avoid wildcard imports (from module import *)",
            severity="medium",
            category="code_smell",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
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
            id="PY004",
            name="God Class",
            description="Class has too many methods",
            severity="medium",
            category="code_smell",
            languages=["python"],
            metadata={"max_methods": 15, "effort": "high"}
        ))
        
        self.add_rule(Rule(
            id="PY005",
            name="Bare Except",
            description="Bare except clause catches all exceptions",
            severity="high",
            category="bug",
            languages=["python"],
            metadata={"effort": "low", "auto_fixable": True}
        ))
        
        # Security rules
        self.add_rule(Rule(
            id="SEC001",
            name="Eval Usage",
            description="Use of eval/exec is dangerous",
            severity="critical",
            category="security",
            languages=["python", "javascript"],
            metadata={"effort": "medium"}
        ))
        
        self.add_rule(Rule(
            id="SEC002",
            name="Hardcoded Secret",
            description="Hardcoded password or token detected",
            severity="high",
            category="security",
            languages=["python", "javascript", "java"],
            metadata={"effort": "low"}
        ))
        
        self.add_rule(Rule(
            id="SEC003",
            name="SQL Injection",
            description="Possible SQL injection vulnerability",
            severity="critical",
            category="security",
            languages=["python", "javascript", "java"],
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
            languages=["python", "javascript"],
            metadata={"effort": "high"}
        ))
        
        # Complexity rules
        self.add_rule(Rule(
            id="CMP001",
            name="High Complexity",
            description="Function has high cyclomatic complexity",
            severity="medium",
            category="performance",
            languages=["python", "javascript", "java"],
            metadata={"max_complexity": 10, "effort": "high"}
        ))
        
        # Naming rules
        self.add_rule(Rule(
            id="NAM001",
            name="Class Naming",
            description="Class names should use CamelCase",
            severity="low",
            category="code_smell",
            languages=["python", "java"],
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
        
        # Documentation rules
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
        return {
            "total_rules": len(self.rules),
            "by_category": {
                category: len(self.get_rules_by_category(category))
                for category in self.categories
            },
            "by_severity": {
                severity: len(self.get_rules_by_severity(severity))
                for severity in ['critical', 'high', 'medium', 'low']
            },
            "enabled_rules": len([r for r in self.rules.values() if r.enabled]),
            "custom_rules": len([r for r in self.rules.values() if r.custom])
        }

# Create singleton instance
rule_manager = RuleManager()
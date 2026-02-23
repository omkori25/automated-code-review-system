# module_analysis_engine/parsers/java/java_parser.py
import javalang
from typing import List, Optional, Any
from ..base_parser import BaseParser, CodeIssue
import logging

logger = logging.getLogger(__name__)

class JavaParser(BaseParser):
    """Java code parser using javalang"""
    
    def __init__(self):
        super().__init__("java")
        self.tree: Optional[Any] = None
        self.code: str = ""
        self.file_path: str = ""
        
    def parse(self, code: str, file_path: str = "<string>") -> List[CodeIssue]:
        """Parse Java code and detect issues"""
        self.code = code
        self.file_path = file_path
        self.clear_issues()
        
        try:
            # Parse to AST
            self.tree = javalang.parse.parse(code)
            
            # Run visitors
            self._check_security()
            self._check_exceptions()
            self._check_threading()
            self._check_serialization()
            self._check_naming()
            self._check_complexity()
            
        except javalang.parser.JavaSyntaxError as e:
            # Handle syntax errors
            self.add_issue(CodeIssue(
                file_path=file_path,
                line_start=e.position.line if e.position else 1,
                line_end=e.position.line if e.position else 1,
                column_start=e.position.column if e.position else 0,
                column_end=(e.position.column if e.position else 0) + 1,
                rule_id="JAVA_SYNTAX001",
                message=f"Java syntax error: {str(e)}",
                severity="critical",
                issue_type="bug",
                suggestion="Fix the syntax error"
            ))
            logger.error(f"Syntax error in {file_path}: {e}")
        
        return self.get_issues()
    
    def _check_security(self):
        """Check Java security issues"""
        if not self.tree:
            return
        
        for path, node in self.tree:
            # Check for dangerous methods
            if isinstance(node, javalang.tree.MethodInvocation):
                if node.member == 'exec' and isinstance(node.qualifier, javalang.tree.MemberReference):
                    if node.qualifier.member == 'Runtime':
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.position.line,
                            line_end=node.position.line,
                            column_start=node.position.column,
                            column_end=node.position.column + len('Runtime.getRuntime().exec'),
                            rule_id="JAVA_SEC001",
                            message="Runtime.exec() can lead to command injection",
                            severity="critical",
                            issue_type="security",
                            suggestion="Avoid using Runtime.exec() with user input. Use ProcessBuilder with safe arguments."
                        ))
            
            # Check for SQL injection
            if isinstance(node, javalang.tree.MethodInvocation):
                if node.member in ['executeQuery', 'executeUpdate']:
                    # Check if using string concatenation
                    for arg in node.arguments:
                        if isinstance(arg, javalang.tree.BinaryOperation) and arg.operator == '+':
                            self.add_issue(CodeIssue(
                                file_path=self.file_path,
                                line_start=node.position.line,
                                line_end=node.position.line,
                                column_start=node.position.column,
                                column_end=node.position.column + len(node.member),
                                rule_id="JAVA_SEC002",
                                message="Possible SQL injection vulnerability",
                                severity="critical",
                                issue_type="security",
                                suggestion="Use prepared statements: PreparedStatement ps = conn.prepareStatement('SELECT * FROM users WHERE id = ?')"
                            ))
            
            # Check for insecure deserialization
            if isinstance(node, javalang.tree.MethodInvocation):
                if node.member == 'readObject' and isinstance(node.qualifier, javalang.tree.MemberReference):
                    if node.qualifier.member == 'ObjectInputStream':
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.position.line,
                            line_end=node.position.line,
                            column_start=node.position.column,
                            column_end=node.position.column + len('readObject'),
                            rule_id="JAVA_SEC003",
                            message="Insecure deserialization detected",
                            severity="high",
                            issue_type="security",
                            suggestion="Validate input before deserialization or use safer alternatives"
                        ))
    
    def _check_exceptions(self):
        """Check exception handling"""
        if not self.tree:
            return
        
        for path, node in self.tree:
            # Check for empty catch blocks
            if isinstance(node, javalang.tree.CatchClause):
                if not node.block.statements:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.position.line,
                        line_end=node.position.line,
                        column_start=node.position.column,
                        column_end=node.position.column + 5,
                        rule_id="JAVA_EXC001",
                        message="Empty catch block detected",
                        severity="medium",
                        issue_type="bug",
                        suggestion="Either handle the exception or log it. Don't leave catch blocks empty."
                    ))
            
            # Check for generic Exception catching
            if isinstance(node, javalang.tree.CatchClause):
                if node.parameter.type.name == 'Exception':
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.position.line,
                        line_end=node.position.line,
                        column_start=node.position.column,
                        column_end=node.position.column + 5,
                        rule_id="JAVA_EXC002",
                        message="Catching generic Exception is too broad",
                        severity="medium",
                        issue_type="code_smell",
                        suggestion="Catch specific exceptions instead of generic Exception"
                    ))
    
    def _check_threading(self):
        """Check threading issues"""
        if not self.tree:
            return
        
        has_synchronized = False
        has_volatile = False
        
        for path, node in self.tree:
            # Check for synchronized keyword
            if isinstance(node, javalang.tree.MethodDeclaration):
                if 'synchronized' in node.modifiers:
                    has_synchronized = True
            
            # Check for volatile keyword
            if isinstance(node, javalang.tree.FieldDeclaration):
                if 'volatile' in node.modifiers:
                    has_volatile = True
        
        # Check for threading issues in concurrent code
        for path, node in self.tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                # Check if class might be used in multithreaded context
                if has_synchronized or has_volatile:
                    # Check for double-checked locking (simplified)
                    pass
    
    def _check_serialization(self):
        """Check serialization issues"""
        if not self.tree:
            return
        
        for path, node in self.tree:
            # Check for Serializable classes without serialVersionUID
            if isinstance(node, javalang.tree.ClassDeclaration):
                implements_serializable = False
                has_serial_version_uid = False
                
                # Check if implements Serializable
                if node.implements:
                    for impl in node.implements:
                        if impl.name == 'Serializable':
                            implements_serializable = True
                
                # Check for serialVersionUID field
                if implements_serializable:
                    for field in node.fields:
                        for declarator in field.declarators:
                            if declarator.name == 'serialVersionUID':
                                has_serial_version_uid = True
                    
                    if not has_serial_version_uid:
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.position.line,
                            line_end=node.position.line,
                            column_start=node.position.column,
                            column_end=node.position.column + len(node.name),
                            rule_id="JAVA_SER001",
                            message=f"Serializable class {node.name} missing serialVersionUID",
                            severity="medium",
                            issue_type="code_smell",
                            suggestion="Add 'private static final long serialVersionUID = 1L;' to the class"
                        ))
    
    def _check_naming(self):
        """Check naming conventions (Java style)"""
        if not self.tree:
            return
        
        for path, node in self.tree:
            # Class names should be PascalCase
            if isinstance(node, javalang.tree.ClassDeclaration):
                if not node.name[0].isupper():
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.position.line,
                        line_end=node.position.line,
                        column_start=node.position.column,
                        column_end=node.position.column + len(node.name),
                        rule_id="JAVA_NAM001",
                        message=f"Class name '{node.name}' should start with uppercase letter",
                        severity="low",
                        issue_type="code_smell",
                        suggestion=f"Rename class to '{node.name[0].upper() + node.name[1:]}'"
                    ))
            
            # Method names should be camelCase
            if isinstance(node, javalang.tree.MethodDeclaration):
                if node.name[0].isupper() and not node.name.startswith('get') and not node.name.startswith('set'):
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.position.line,
                        line_end=node.position.line,
                        column_start=node.position.column,
                        column_end=node.position.column + len(node.name),
                        rule_id="JAVA_NAM002",
                        message=f"Method name '{node.name}' should start with lowercase letter",
                        severity="low",
                        issue_type="code_smell",
                        suggestion=f"Rename method to '{node.name[0].lower() + node.name[1:]}'"
                    ))
            
            # Constants should be UPPER_SNAKE_CASE
            if isinstance(node, javalang.tree.FieldDeclaration):
                if 'static' in node.modifiers and 'final' in node.modifiers:
                    for declarator in node.declarators:
                        if not declarator.name.isupper() or '_' not in declarator.name:
                            self.add_issue(CodeIssue(
                                file_path=self.file_path,
                                line_start=node.position.line,
                                line_end=node.position.line,
                                column_start=node.position.column,
                                column_end=node.position.column + len(declarator.name),
                                rule_id="JAVA_NAM003",
                                message=f"Constant '{declarator.name}' should be UPPER_SNAKE_CASE",
                                severity="low",
                                issue_type="code_smell",
                                suggestion=f"Rename constant to '{declarator.name.upper()}'"
                            ))
    
    def _check_complexity(self):
        """Check code complexity"""
        if not self.tree:
            return
        
        # Count methods per class
        class_methods = {}
        
        for path, node in self.tree:
            if isinstance(node, javalang.tree.ClassDeclaration):
                class_methods[node.name] = 0
            
            if isinstance(node, javalang.tree.MethodDeclaration):
                # Find containing class
                for cls_path, cls_node in self.tree:
                    if isinstance(cls_node, javalang.tree.ClassDeclaration):
                        # Check if method is in this class (simplified)
                        if node.position and cls_node.position:
                            if node.position.line > cls_node.position.line:
                                if node.name not in class_methods:
                                    class_methods[cls_node.name] = class_methods.get(cls_node.name, 0) + 1
        
        # Check for God Class
        for class_name, method_count in class_methods.items():
            if method_count > 15:
                self.add_issue(CodeIssue(
                    file_path=self.file_path,
                    line_start=1,
                    line_end=1,
                    column_start=0,
                    column_end=1,
                    rule_id="JAVA_CMP001",
                    message=f"Class '{class_name}' has {method_count} methods (God Class)",
                    severity="medium",
                    issue_type="code_smell",
                    suggestion="Consider splitting this class into multiple smaller classes"
                ))
    
    def get_supported_rules(self) -> List[str]:
        """Return list of supported rule IDs"""
        return [
            "JAVA_SEC001", "JAVA_SEC002", "JAVA_SEC003",
            "JAVA_EXC001", "JAVA_EXC002",
            "JAVA_SER001",
            "JAVA_NAM001", "JAVA_NAM002", "JAVA_NAM003",
            "JAVA_CMP001"
        ]
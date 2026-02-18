# module_analysis_engine/parsers/python/python_parser.py
import ast
from typing import List, Optional, Any
from ..base_parser import BaseParser, CodeIssue
import logging

logger = logging.getLogger(__name__)

class PythonParser(BaseParser):
    """Python code parser using AST"""
    
    def __init__(self):
        super().__init__("python")
        self.tree: Optional[ast.AST] = None
        self.code: str = ""
        self.file_path: str = ""
        
    def parse(self, code: str, file_path: str = "<string>") -> List[CodeIssue]:
        """Parse Python code and detect issues"""
        self.code = code
        self.file_path = file_path
        self.clear_issues()
        
        try:
            # Parse AST
            self.tree = ast.parse(code)
            
            # Run visitors
            self._check_imports()
            self._check_functions()
            self._check_classes()
            self._check_exceptions()
            self._check_security()
            self._check_complexity()
            self._check_naming_conventions()
            self._check_docstrings()
            self._check_unused_variables()
            self._check_mutable_defaults()
            
        except SyntaxError as e:
            # Handle syntax errors
            self.add_issue(CodeIssue(
                file_path=file_path,
                line_start=e.lineno or 1,
                line_end=e.lineno or 1,
                column_start=e.offset or 0,
                column_end=(e.offset or 0) + 1,
                rule_id="SYNTAX001",
                message=f"Syntax error: {e.msg}",
                severity="critical",
                issue_type="bug",
                suggestion="Fix the syntax error",
                code_snippet=self._get_line(e.lineno or 1)
            ))
            logger.error(f"Syntax error in {file_path}: {e}")
        
        return self.get_issues()
    
    def _check_imports(self):
        """Check import statements"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            # Check for wildcard imports
            if isinstance(node, ast.ImportFrom):
                if node.module == "*":
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + 10,
                        rule_id="PY001",
                        message="Avoid wildcard imports (from module import *)",
                        severity="medium",
                        issue_type="code_smell",
                        suggestion="Import only what you need: 'from module import func1, func2'"
                    ))
            
            # Check for unused imports (simplified - would need more complex analysis)
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.asname:
                        name = alias.asname
                    else:
                        name = alias.name.split('.')[0]
                    
                    # This is a simplified check - real unused import detection needs symbol table
                    if name not in ['os', 'sys', 're']:  # Example whitelist
                        pass  # In real implementation, check if name is used in code
    
    def _check_functions(self):
        """Check function definitions"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Check function length
                if node.end_lineno and (node.end_lineno - node.lineno > 50):
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.end_lineno or node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="PY002",
                        message=f"Function '{node.name}' is too long ({node.end_lineno - node.lineno} lines)",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Consider breaking this function into smaller functions"
                    ))
                
                # Check number of arguments
                if len(node.args.args) > 5:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="PY003",
                        message=f"Function '{node.name}' has too many parameters ({len(node.args.args)})",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Consider using a dataclass or reducing parameters"
                    ))
                
                # Check for missing return type hints
                if not node.returns:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="PY006",
                        message=f"Function '{node.name}' missing return type hint",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Add return type hint: 'def function() -> type:'"
                    ))
    
    def _check_classes(self):
        """Check class definitions"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                # Count methods
                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                if len(methods) > 15:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="PY004",
                        message=f"Class '{node.name}' has too many methods ({len(methods)}) (God Class)",
                        severity="medium",
                        issue_type="code_smell",
                        suggestion="Consider splitting this class into multiple classes"
                    ))
                
                # Check for missing __init__ method
                has_init = any(isinstance(m, ast.FunctionDef) and m.name == '__init__' for m in node.body)
                if not has_init and methods:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="PY007",
                        message=f"Class '{node.name}' missing __init__ method",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Add an __init__ method to initialize class attributes"
                    ))
    
    def _check_exceptions(self):
        """Check exception handling"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.ExceptHandler):
                # Check for bare except
                if node.type is None:
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + 6,  # "except" length
                        rule_id="PY005",
                        message="Bare except clause detected",
                        severity="high",
                        issue_type="bug",
                        suggestion="Specify which exceptions to catch: except SpecificError:"
                    ))
                
                # Check for too broad except
                if node.type and isinstance(node.type, ast.Name):
                    if node.type.id == 'Exception':
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=node.col_offset,
                            column_end=node.col_offset + len(node.type.id),
                            rule_id="PY008",
                            message="Too broad except clause (catching all Exceptions)",
                            severity="medium",
                            issue_type="bug",
                            suggestion="Catch specific exceptions instead of all Exceptions"
                        ))
    
    def _check_security(self):
        """Check security issues"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            # Check for eval/exec usage
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec', 'compile']:
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=node.col_offset,
                            column_end=node.col_offset + len(node.func.id),
                            rule_id="SEC001",
                            message=f"Use of '{node.func.id}' is dangerous",
                            severity="critical",
                            issue_type="security",
                            suggestion="Avoid using eval/exec. Use safer alternatives like ast.literal_eval()"
                        ))
            
            # Check for hardcoded secrets
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        secret_keywords = ['password', 'token', 'key', 'secret', 'api_key', 'apikey', 'pwd']
                        if any(secret in target.id.lower() for secret in secret_keywords):
                            if isinstance(node.value, (ast.Str, ast.Constant)):
                                self.add_issue(CodeIssue(
                                    file_path=self.file_path,
                                    line_start=node.lineno,
                                    line_end=node.lineno,
                                    column_start=target.col_offset,
                                    column_end=target.col_offset + len(target.id),
                                    rule_id="SEC002",
                                    message=f"Hardcoded {target.id} detected",
                                    severity="high",
                                    issue_type="security",
                                    suggestion="Use environment variables or a secrets manager"
                                ))
            
            # Check for SQL injection
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['execute', 'executemany']:
                        for arg in node.args:
                            if isinstance(arg, ast.JoinedStr):  # f-string
                                self.add_issue(CodeIssue(
                                    file_path=self.file_path,
                                    line_start=node.lineno,
                                    line_end=node.lineno,
                                    column_start=node.col_offset,
                                    column_end=node.col_offset + 10,
                                    rule_id="SEC003",
                                    message="Possible SQL injection vulnerability",
                                    severity="critical",
                                    issue_type="security",
                                    suggestion="Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
                                ))
            
            # Check for pickling (security risk)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr in ['loads', 'load'] and node.func.value.id == 'pickle':
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=node.col_offset,
                            column_end=node.col_offset + 10,
                            rule_id="SEC004",
                            message="Using pickle.load/loads on untrusted data is dangerous",
                            severity="high",
                            issue_type="security",
                            suggestion="Use json or a safer serialization format for untrusted data"
                        ))
            
            # Check for shell injection (os.system, subprocess with shell=True)
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Attribute):
                    if node.func.attr == 'system' and node.func.value.id == 'os':
                        for arg in node.args:
                            if isinstance(arg, ast.Str) or isinstance(arg, ast.JoinedStr):
                                self.add_issue(CodeIssue(
                                    file_path=self.file_path,
                                    line_start=node.lineno,
                                    line_end=node.lineno,
                                    column_start=node.col_offset,
                                    column_end=node.col_offset + 10,
                                    rule_id="SEC005",
                                    message="Potential shell injection vulnerability",
                                    severity="critical",
                                    issue_type="security",
                                    suggestion="Use subprocess.run with list arguments instead of shell commands"
                                ))
    
    def _check_complexity(self):
        """Check code complexity"""
        if not self.tree:
            return
            
        class ComplexityVisitor(ast.NodeVisitor):
            def __init__(self, parser):
                self.parser = parser
                self.complexity = 0
                
            def visit_If(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_While(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_For(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_ExceptHandler(self, node):
                self.complexity += 1
                self.generic_visit(node)
                
            def visit_BoolOp(self, node):
                if isinstance(node.op, (ast.And, ast.Or)):
                    self.complexity += len(node.values) - 1
                self.generic_visit(node)
                
            def visit_FunctionDef(self, node):
                old_complexity = self.complexity
                self.complexity = 0
                self.generic_visit(node)
                
                if self.complexity > 10:
                    self.parser.add_issue(CodeIssue(
                        file_path=self.parser.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="CMP001",
                        message=f"Function '{node.name}' has high cyclomatic complexity ({self.complexity})",
                        severity="medium",
                        issue_type="code_smell",
                        suggestion="Break this function into smaller, more focused functions"
                    ))
                
                self.complexity = old_complexity
        
        ComplexityVisitor(self).visit(self.tree)
    
    def _check_naming_conventions(self):
        """Check naming conventions (PEP 8)"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            # Class names should be CamelCase
            if isinstance(node, ast.ClassDef):
                if not node.name[0].isupper():
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="NAM001",
                        message=f"Class name '{node.name}' should use CamelCase",
                        severity="low",
                        issue_type="code_smell",
                        suggestion=f"Rename class to '{node.name.title()}'"
                    ))
            
            # Function names should be snake_case
            if isinstance(node, ast.FunctionDef):
                if not node.name.islower() and '_' not in node.name:
                    if not node.name.startswith('__') or not node.name.endswith('__'):  # Skip magic methods
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=node.col_offset,
                            column_end=node.col_offset + len(node.name),
                            rule_id="NAM002",
                            message=f"Function name '{node.name}' should use snake_case",
                            severity="low",
                            issue_type="code_smell",
                            suggestion="Use lowercase with underscores for function names"
                        ))
            
            # Variable names should be lowercase
            if isinstance(node, ast.Name):
                if isinstance(node.ctx, ast.Store):  # Variable assignment
                    if not node.id.islower() and '_' not in node.id:
                        if not node.id.startswith('__'):  # Skip dunder names
                            self.add_issue(CodeIssue(
                                file_path=self.file_path,
                                line_start=node.lineno,
                                line_end=node.lineno,
                                column_start=node.col_offset,
                                column_end=node.col_offset + len(node.id),
                                rule_id="NAM003",
                                message=f"Variable name '{node.id}' should use snake_case",
                                severity="low",
                                issue_type="code_smell",
                                suggestion="Use lowercase with underscores for variable names"
                            ))
    
    def _check_docstrings(self):
        """Check for missing docstrings"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            # Check module docstring
            if isinstance(node, ast.Module):
                if not ast.get_docstring(node):
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=1,
                        line_end=1,
                        column_start=0,
                        column_end=1,
                        rule_id="DOC001",
                        message="Module missing docstring",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Add a module-level docstring describing the module's purpose"
                    ))
            
            # Check function docstrings
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    if not node.name.startswith('__'):  # Skip magic methods
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=node.col_offset,
                            column_end=node.col_offset + len(node.name),
                            rule_id="DOC002",
                            message=f"Function '{node.name}' missing docstring",
                            severity="low",
                            issue_type="code_smell",
                            suggestion="Add a docstring describing what the function does"
                        ))
            
            # Check class docstrings
            if isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    self.add_issue(CodeIssue(
                        file_path=self.file_path,
                        line_start=node.lineno,
                        line_end=node.lineno,
                        column_start=node.col_offset,
                        column_end=node.col_offset + len(node.name),
                        rule_id="DOC003",
                        message=f"Class '{node.name}' missing docstring",
                        severity="low",
                        issue_type="code_smell",
                        suggestion="Add a class docstring describing the class's purpose"
                    ))
    
    def _check_unused_variables(self):
        """Check for unused variables"""
        if not self.tree:
            return
            
        # This is a simplified check - real implementation would need symbol table
        class VariableVisitor(ast.NodeVisitor):
            def __init__(self):
                self.defined = set()
                self.used = set()
                
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    self.defined.add(node.id)
                elif isinstance(node.ctx, ast.Load):
                    self.used.add(node.id)
                self.generic_visit(node)
            
            def visit_FunctionDef(self, node):
                # Skip nested functions for simplicity
                pass
        
        visitor = VariableVisitor()
        visitor.visit(self.tree)
        
        unused = visitor.defined - visitor.used
        for var in unused:
            # Skip common patterns
            if var.startswith('_') or var in ['self', 'cls']:
                continue
            # In real implementation, would need to map back to line number
            pass
    
    def _check_mutable_defaults(self):
        """Check for mutable default arguments"""
        if not self.tree:
            return
            
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                for default in node.args.defaults:
                    # Check for list, dict, set literals
                    if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                        self.add_issue(CodeIssue(
                            file_path=self.file_path,
                            line_start=node.lineno,
                            line_end=node.lineno,
                            column_start=default.col_offset,
                            column_end=default.col_offset + 10,
                            rule_id="MUT001",
                            message="Mutable default argument detected",
                            severity="high",
                            issue_type="bug",
                            suggestion="Use None as default and initialize inside function: def func(arg=None): if arg is None: arg = []"
                        ))
    
    def _get_line(self, line_no: int) -> str:
        """Get source code line"""
        if not self.code:
            return ""
        lines = self.code.split('\n')
        if 1 <= line_no <= len(lines):
            return lines[line_no - 1]
        return ""
    
    def get_supported_rules(self) -> List[str]:
        """Return list of supported rule IDs"""
        return [
            "PY001", "PY002", "PY003", "PY004", "PY005", "PY006", "PY007", "PY008",
            "SEC001", "SEC002", "SEC003", "SEC004", "SEC005",
            "CMP001",
            "NAM001", "NAM002", "NAM003",
            "DOC001", "DOC002", "DOC003",
            "MUT001"
        ]
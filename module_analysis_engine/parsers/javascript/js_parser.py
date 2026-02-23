# module_analysis_engine/parsers/javascript/js_parser.py
import esprima
from typing import List, Optional, Any
from ..base_parser import BaseParser, CodeIssue
import logging

logger = logging.getLogger(__name__)

class JavaScriptParser(BaseParser):
    """JavaScript/TypeScript code parser using esprima"""
    
    def __init__(self):
        super().__init__("javascript")
        self.tree: Optional[Any] = None
        self.code: str = ""
        self.file_path: str = ""
        
    def parse(self, code: str, file_path: str = "<string>") -> List[CodeIssue]:
        """Parse JavaScript code and detect issues"""
        self.code = code
        self.file_path = file_path
        self.clear_issues()
        
        try:
            # Parse to AST
            self.tree = esprima.parseScript(code, {'loc': True, 'range': True})
            
            # Run visitors
            self._check_security()
            self._check_functions()
            self._check_globals()
            self._check_async_patterns()
            self._check_react_patterns()
            self._check_typescript_features()
            
        except Exception as e:
            # Handle parsing errors
            self.add_issue(CodeIssue(
                file_path=file_path,
                line_start=1,
                line_end=1,
                column_start=0,
                column_end=1,
                rule_id="JS_SYNTAX001",
                message=f"JavaScript parsing error: {str(e)}",
                severity="critical",
                issue_type="bug",
                suggestion="Fix syntax error",
                code_snippet=code[:100]
            ))
            logger.error(f"Parse error in {file_path}: {e}")
        
        return self.get_issues()
    
    def _check_security(self):
        """Check JavaScript security issues"""
        if not self.tree:
            return
        
        class SecurityVisitor:
            def __init__(self, parser):
                self.parser = parser
            
            def visit(self, node):
                if node.type == 'CallExpression':
                    # Check for eval()
                    if node.callee.name == 'eval':
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_SEC001",
                            message="Use of eval() is dangerous",
                            severity="critical",
                            issue_type="security",
                            suggestion="Avoid eval(). Use Function constructor or JSON.parse for JSON"
                        ))
                    
                    # Check for setTimeout with string (same as eval)
                    if node.callee.name == 'setTimeout' and len(node.arguments) > 0:
                        if node.arguments[0].type == 'Literal' and isinstance(node.arguments[0].value, str):
                            self.parser.add_issue(CodeIssue(
                                file_path=self.parser.file_path,
                                line_start=node.loc.start.line,
                                line_end=node.loc.end.line,
                                column_start=node.loc.start.column,
                                column_end=node.loc.end.column,
                                rule_id="JS_SEC002",
                                message="setTimeout with string argument is dangerous",
                                severity="high",
                                issue_type="security",
                                suggestion="Use function instead of string: setTimeout(() => {...}, 1000)"
                            ))
                
                # Check for document.write (security risk)
                if node.type == 'MemberExpression' and node.object.name == 'document':
                    if node.property.name == 'write':
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_SEC003",
                            message="document.write() can lead to XSS vulnerabilities",
                            severity="high",
                            issue_type="security",
                            suggestion="Use DOM manipulation methods like innerHTML with caution"
                        ))
                
                # Check for innerHTML with dynamic content
                if node.type == 'AssignmentExpression' and node.left.property:
                    if node.left.property.name == 'innerHTML':
                        if node.right.type != 'Literal':  # Dynamic content
                            self.parser.add_issue(CodeIssue(
                                file_path=self.parser.file_path,
                                line_start=node.loc.start.line,
                                line_end=node.loc.end.line,
                                column_start=node.loc.start.column,
                                column_end=node.loc.end.column,
                                rule_id="JS_SEC004",
                                message="innerHTML with dynamic content can lead to XSS",
                                severity="high",
                                issue_type="security",
                                suggestion="Use textContent or sanitize input with DOMPurify"
                            ))
                
                # Continue traversal
                for key in node.__dict__:
                    if key not in ['parent', 'loc', 'range']:
                        value = getattr(node, key)
                        if isinstance(value, list):
                            for item in value:
                                if hasattr(item, 'type'):
                                    self.visit(item)
                        elif hasattr(value, 'type'):
                            self.visit(value)
        
        visitor = SecurityVisitor(self)
        visitor.visit(self.tree)
    
    def _check_functions(self):
        """Check function-related issues"""
        if not self.tree:
            return
        
        class FunctionVisitor:
            def __init__(self, parser):
                self.parser = parser
                self.function_count = 0
            
            def visit(self, node):
                # Check function length/complexity
                if node.type in ['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression']:
                    self.function_count += 1
                    
                    # Check function length (rough estimate)
                    if node.loc.end.line - node.loc.start.line > 30:
                        name = node.id.name if hasattr(node, 'id') and node.id else 'anonymous'
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_FUNC001",
                            message=f"Function '{name}' is too long ({node.loc.end.line - node.loc.start.line} lines)",
                            severity="low",
                            issue_type="code_smell",
                            suggestion="Consider breaking this function into smaller functions"
                        ))
                    
                    # Check number of parameters
                    if hasattr(node, 'params') and len(node.params) > 5:
                        name = node.id.name if hasattr(node, 'id') and node.id else 'anonymous'
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_FUNC002",
                            message=f"Function '{name}' has too many parameters ({len(node.params)})",
                            severity="low",
                            issue_type="code_smell",
                            suggestion="Use an object parameter or reduce parameters"
                        ))
                
                # Continue traversal
                for key in node.__dict__:
                    if key not in ['parent', 'loc', 'range']:
                        value = getattr(node, key)
                        if isinstance(value, list):
                            for item in value:
                                if hasattr(item, 'type'):
                                    self.visit(item)
                        elif hasattr(value, 'type'):
                            self.visit(value)
        
        visitor = FunctionVisitor(self)
        visitor.visit(self.tree)
    
    def _check_globals(self):
        """Check global namespace pollution"""
        if not self.tree:
            return
        
        class GlobalVisitor:
            def __init__(self, parser):
                self.parser = parser
                self.globals = []
            
            def visit(self, node):
                # Check for variable declarations in global scope
                if node.type in ['VariableDeclaration', 'FunctionDeclaration']:
                    # Check if at top level (simplified)
                    if self.is_global_scope(node):
                        if node.type == 'VariableDeclaration':
                            for decl in node.declarations:
                                if decl.id.name:
                                    self.globals.append(decl.id.name)
                        elif node.type == 'FunctionDeclaration' and node.id:
                            self.globals.append(node.id.name)
                
                # Continue traversal
                for key in node.__dict__:
                    if key not in ['parent', 'loc', 'range']:
                        value = getattr(node, key)
                        if isinstance(value, list):
                            for item in value:
                                if hasattr(item, 'type'):
                                    self.visit(item)
                        elif hasattr(value, 'type'):
                            self.visit(value)
            
            def is_global_scope(self, node):
                # Simplified: check if parent is Program
                return hasattr(node, 'parent') and node.parent and node.parent.type == 'Program'
        
        visitor = GlobalVisitor(self)
        visitor.visit(self.tree)
        
        if len(visitor.globals) > 5:
            self.add_issue(CodeIssue(
                file_path=self.file_path,
                line_start=1,
                line_end=1,
                column_start=0,
                column_end=1,
                rule_id="JS_GLOB001",
                message=f"Too many global variables ({len(visitor.globals)})",
                severity="medium",
                issue_type="code_smell",
                suggestion="Use modules or namespaces to avoid polluting global scope"
            ))
    
    def _check_async_patterns(self):
        """Check async/await patterns"""
        if not self.tree:
            return
        
        class AsyncVisitor:
            def __init__(self, parser):
                self.parser = parser
            
            def visit(self, node):
                # Check for missing await
                if node.type == 'CallExpression' and node.callee.name == 'fetch':
                    # Check if inside async function but no await
                    if self.is_in_async_function(node) and not self.has_await_parent(node):
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_ASYNC001",
                            message="fetch() called without await in async function",
                            severity="medium",
                            issue_type="bug",
                            suggestion="Add await: await fetch(...)"
                        ))
                
                # Check for promise without error handling
                if node.type == 'CallExpression' and node.callee.name in ['then', 'catch', 'finally']:
                    # This indicates promise usage, check if parent handles errors
                    pass
                
                # Continue traversal
                for key in node.__dict__:
                    if key not in ['parent', 'loc', 'range']:
                        value = getattr(node, key)
                        if isinstance(value, list):
                            for item in value:
                                if hasattr(item, 'type'):
                                    self.visit(item)
                        elif hasattr(value, 'type'):
                            self.visit(value)
            
            def is_in_async_function(self, node):
                current = node
                while current:
                    if getattr(current, "async", False):
                        return True
                    current = getattr(current, 'parent', None)
                return False
            
            def has_await_parent(self, node):
                current = node.parent
                while current:
                    if current.type == 'AwaitExpression':
                        return True
                    current = getattr(current, 'parent', None)
                return False
        
        visitor = AsyncVisitor(self)
        visitor.visit(self.tree)
    
    def _check_react_patterns(self):
        """Check React-specific patterns"""
        if not self.tree:
            return
        
        class ReactVisitor:
            def __init__(self, parser):
                self.parser = parser
                self.has_react = False
                self.has_hooks = False
            
            def visit(self, node):
                # Check for React import
                if node.type == 'ImportDeclaration':
                    if node.source.value == 'react':
                        self.has_react = True
                
                # Check for hooks
                if node.type == 'CallExpression' and node.callee.name:
                    if node.callee.name.startswith('use') and len(node.callee.name) > 3:
                        self.has_hooks = True
                        
                        # Check hook rules
                        if not self.is_in_function_component(node):
                            self.parser.add_issue(CodeIssue(
                                file_path=self.parser.file_path,
                                line_start=node.loc.start.line,
                                line_end=node.loc.end.line,
                                column_start=node.loc.start.column,
                                column_end=node.loc.end.column,
                                rule_id="JS_REACT001",
                                message=f"Hook '{node.callee.name}' called outside of function component",
                                severity="high",
                                issue_type="bug",
                                suggestion="Hooks must be called in React function components"
                            ))
                
                # Check for missing key in lists
                if node.type == 'JSXElement':
                    # Simplified check for key attribute
                    has_key = False
                    for attr in node.openingElement.attributes:
                        if attr.type == 'JSXAttribute' and attr.name.name == 'key':
                            has_key = True
                            break
                    
                    # Check if this is likely in a map (simplified)
                    if not has_key and self.is_in_map(node):
                        self.parser.add_issue(CodeIssue(
                            file_path=self.parser.file_path,
                            line_start=node.loc.start.line,
                            line_end=node.loc.end.line,
                            column_start=node.loc.start.column,
                            column_end=node.loc.end.column,
                            rule_id="JS_REACT002",
                            message="Missing 'key' prop in list rendering",
                            severity="medium",
                            issue_type="bug",
                            suggestion="Add a unique key prop to each element in the list"
                        ))
                
                # Continue traversal
                for key in node.__dict__:
                    if key not in ['parent', 'loc', 'range']:
                        value = getattr(node, key)
                        if isinstance(value, list):
                            for item in value:
                                if hasattr(item, 'type'):
                                    self.visit(item)
                        elif hasattr(value, 'type'):
                            self.visit(value)
            
            def is_in_function_component(self, node):
                current = node
                while current:
                    if current.type in ['FunctionDeclaration', 'FunctionExpression', 'ArrowFunctionExpression']:
                        # Check if returns JSX (simplified)
                        return True
                    current = getattr(current, 'parent', None)
                return False
            
            def is_in_map(self, node):
                current = node
                while current:
                    if current.type == 'CallExpression' and current.callee.property:
                        if current.callee.property.name == 'map':
                            return True
                    current = getattr(current, 'parent', None)
                return False
        
        visitor = ReactVisitor(self)
        visitor.visit(self.tree)
    
    def _check_typescript_features(self):
        """Check TypeScript-specific patterns"""
        if self.language != 'typescript':
            return
        
        # TypeScript-specific checks would go here
        # This would require a TypeScript parser like ts-morph or typescript compiler API
        pass
    
    def get_supported_rules(self) -> List[str]:
        """Return list of supported rule IDs"""
        return [
            "JS_SEC001", "JS_SEC002", "JS_SEC003", "JS_SEC004",
            "JS_FUNC001", "JS_FUNC002",
            "JS_GLOB001",
            "JS_ASYNC001",
            "JS_REACT001", "JS_REACT002"
        ]
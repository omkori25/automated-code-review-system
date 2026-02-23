# module_backend/services/analysis_service.py
import asyncio
from typing import Dict, Any, List, Optional
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import logging

# Import parsers for different languages
from module_analysis_engine.parsers.python.python_parser import PythonParser
from module_analysis_engine.parsers.javascript.js_parser import JavaScriptParser
from module_analysis_engine.parsers.java.java_parser import JavaParser
from module_analysis_engine.rules.rule_manager import rule_manager

# Import ML models
from module_ml.models.bug_predictor import bug_predictor
from module_ml.models.code_embedder import CodeBERTEmbedder

# Import database operations
from module_backend.database.crud_operations import AnalysisCRUD, IssueCRUD

logger = logging.getLogger(__name__)

class AnalysisService:
    """Service for managing code analysis"""
    
    def __init__(self):
        # Initialize parsers for different languages
        self.parsers = {
            'python': PythonParser(),
            'javascript': JavaScriptParser(),
            'typescript': JavaScriptParser(),  # Reuse JS parser for TS
            'java': JavaParser(),
        }
        
        # Initialize ML models
        try:
            self.ml_enabled = True
            self.embedder = CodeBERTEmbedder()
            logger.info("✅ ML models initialized successfully")
        except Exception as e:
            self.ml_enabled = False
            logger.warning(f"⚠️ ML models not available: {e}")
        
        # Store active analyses
        self.active_analyses: Dict[str, Dict[str, Any]] = {}
        
        # Rule statistics
        self.rule_stats = rule_manager.get_statistics()
        logger.info(f"📊 Loaded {self.rule_stats['total_rules']} rules across {len(self.parsers)} languages")
    
    async def start_analysis(self, db: Session, project_id: str, files: List[Dict[str, Any]]) -> Any:
        """Start code analysis for multiple files"""
        analysis_id = str(uuid.uuid4())
        
        # Count files by language
        language_counts = {}
        for file in files:
            lang = file.get('language', 'unknown')
            language_counts[lang] = language_counts.get(lang, 0) + 1
        
        logger.info(f"🚀 Starting analysis {analysis_id} for project {project_id}")
        logger.info(f"📁 Files: {len(files)} total, by language: {language_counts}")
        
        # Create analysis record in database
        analysis = AnalysisCRUD.create_analysis(db, {
            "project_id": project_id,
            "status": "running",
            "started_at": datetime.now(),
            "total_files": len(files),
            "metadata": {
                "languages": language_counts,
                "ml_enabled": self.ml_enabled
            }
        })
        
        # Store in active analyses
        self.active_analyses[str(analysis.id)] = {
            "id": str(analysis.id),
            "project_id": project_id,
            "status": "running",
            "files": files,
            "started_at": datetime.now().isoformat(),
            "progress": 0,
            "results": None,
            "language_counts": language_counts
        }
        
        # Start background analysis
        asyncio.create_task(self._run_analysis(db, str(analysis.id), files))
        
        return analysis
    
    async def _run_analysis(self, db: Session, analysis_id: str, files: List[Dict[str, Any]]):
        """Run analysis in background"""
        logger.info(f"🔍 Running analysis {analysis_id} on {len(files)} files")
        
        try:
            all_issues = []
            file_results = []
            
            for idx, file_info in enumerate(files):
                file_path = file_info.get('path', 'unknown')
                language = file_info.get('language', 'unknown')
                content = file_info.get('content', '')
                
                logger.info(f"  Analyzing [{idx+1}/{len(files)}]: {file_path} ({language})")
                
                file_issues = []
                
                # Step 1: Static analysis with language-specific parser
                parser = self.parsers.get(language)
                if parser:
                    try:
                        static_issues = parser.parse(content, file_path)
                        file_issues.extend(static_issues)
                        logger.info(f"    ✅ Static analysis found {len(static_issues)} issues")
                    except Exception as e:
                        logger.error(f"    ❌ Static analysis failed: {e}")
                
                # Step 2: ML-based analysis (if enabled)
                if self.ml_enabled and language in ['python', 'javascript', 'typescript']:
                    try:
                        ml_result = bug_predictor.predict(content)
                        
                        # Convert ML results to issues
                        if ml_result.get('needs_review'):
                            for bug_type, details in ml_result['predictions'].items():
                                if details['has_issue']:
                                    file_issues.append({
                                        'file_path': file_path,
                                        'rule_id': f"ML_{bug_type.upper()}",
                                        'message': f"ML detected possible {bug_type}",
                                        'severity': 'medium' if details['confidence'] == 'high' else 'low',
                                        'issue_type': bug_type,
                                        'line_start': 1,
                                        'line_end': 1,
                                        'column_start': 0,
                                        'column_end': 0,
                                        'suggestion': 'Review this code for potential issues',
                                        'metadata': {
                                            'confidence': details['confidence'],
                                            'probability': details['probability'],
                                            'ml_detected': True
                                        }
                                    })
                            
                            logger.info(f"    🤖 ML analysis found potential issues")
                    except Exception as e:
                        logger.error(f"    ❌ ML analysis failed: {e}")
                
                # Step 3: Apply general rules (TODO, FIXME, etc.)
                general_issues = self._check_general_rules(content, file_path)
                file_issues.extend(general_issues)
                
                # Store file results
                file_result = {
                    'file_path': file_path,
                    'language': language,
                    'issues': file_issues,
                    'issue_count': len(file_issues)
                }
                file_results.append(file_result)
                all_issues.extend(file_issues)
                
                # Update progress
                progress = int(((idx + 1) / len(files)) * 100)
                self.active_analyses[analysis_id]['progress'] = progress
                
                # Small delay to prevent overwhelming the system
                await asyncio.sleep(0.1)
            
            # Count issues by severity
            severity_counts = {
                'critical': sum(1 for i in all_issues if i.get('severity') == 'critical'),
                'high': sum(1 for i in all_issues if i.get('severity') == 'high'),
                'medium': sum(1 for i in all_issues if i.get('severity') == 'medium'),
                'low': sum(1 for i in all_issues if i.get('severity') == 'low')
            }
            
            # Count issues by type
            type_counts = {}
            for issue in all_issues:
                issue_type = issue.get('issue_type', 'unknown')
                type_counts[issue_type] = type_counts.get(issue_type, 0) + 1
            
            # Prepare results
            results = {
                'analysis_id': analysis_id,
                'total_issues': len(all_issues),
                'files_analyzed': len(files),
                'files_with_issues': len([f for f in file_results if f['issue_count'] > 0]),
                'issues': all_issues,
                'file_results': file_results,
                'summary': {
                    'by_severity': severity_counts,
                    'by_type': type_counts,
                    'by_language': self.active_analyses[analysis_id]['language_counts']
                },
                'ml_used': self.ml_enabled,
                'completed_at': datetime.now().isoformat()
            }
            
            # Update analysis status
            self.active_analyses[analysis_id].update({
                'status': 'completed',
                'completed_at': datetime.now().isoformat(),
                'results': results,
                'progress': 100
            })
            
            # Update database
            AnalysisCRUD.update_analysis_status(db, analysis_id, "completed")
            
            # Save issues to database
            for issue in all_issues:
                try:
                    IssueCRUD.create_issue(db, {
                        'analysis_id': analysis_id,
                        'file_path': issue['file_path'],
                        'line_start': issue.get('line_start', 1),
                        'line_end': issue.get('line_end', 1),
                        'column_start': issue.get('column_start', 0),
                        'column_end': issue.get('column_end', 0),
                        'rule_id': issue['rule_id'],
                        'message': issue['message'],
                        'severity': issue['severity'],
                        'issue_type': issue.get('issue_type', 'unknown'),
                        'suggestion': issue.get('suggestion', ''),
                        'metadata': issue.get('metadata', {})
                    })
                except Exception as e:
                    logger.error(f"Failed to save issue to database: {e}")
            
            logger.info(f"✅ Analysis {analysis_id} completed")
            logger.info(f"📊 Results: {len(all_issues)} total issues")
            logger.info(f"   Critical: {severity_counts['critical']}, High: {severity_counts['high']}, "
                       f"Medium: {severity_counts['medium']}, Low: {severity_counts['low']}")
            
        except Exception as e:
            logger.error(f"❌ Analysis {analysis_id} failed: {e}", exc_info=True)
            self.active_analyses[analysis_id]['status'] = 'failed'
            self.active_analyses[analysis_id]['error'] = str(e)
            AnalysisCRUD.update_analysis_status(db, analysis_id, "failed")
    
    def _check_general_rules(self, content: str, file_path: str) -> List[Dict]:
        """Check general rules that apply to all languages"""
        issues = []
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for TODO comments
            if 'TODO' in line and '#' not in line and '//' not in line:
                issues.append({
                    'file_path': file_path,
                    'rule_id': 'GEN001',
                    'message': 'TODO comment found',
                    'severity': 'low',
                    'issue_type': 'code_smell',
                    'line_start': i,
                    'line_end': i,
                    'column_start': line.find('TODO'),
                    'column_end': line.find('TODO') + 4,
                    'suggestion': 'Complete the TODO task before production',
                    'metadata': {'line_content': line.strip()}
                })
            
            # Check for FIXME comments
            if 'FIXME' in line and '#' not in line and '//' not in line:
                issues.append({
                    'file_path': file_path,
                    'rule_id': 'GEN002',
                    'message': 'FIXME comment found - known issue',
                    'severity': 'medium',
                    'issue_type': 'bug',
                    'line_start': i,
                    'line_end': i,
                    'column_start': line.find('FIXME'),
                    'column_end': line.find('FIXME') + 5,
                    'suggestion': 'Fix this known issue',
                    'metadata': {'line_content': line.strip()}
                })
            
            # Check for debug print statements
            if 'print(' in line and ('console.log' in line or 'System.out.println' in line):
                issues.append({
                    'file_path': file_path,
                    'rule_id': 'GEN003',
                    'message': 'Debug print statement found',
                    'severity': 'low',
                    'issue_type': 'code_smell',
                    'line_start': i,
                    'line_end': i,
                    'column_start': max(line.find('print'), line.find('console.log'), line.find('System.out')),
                    'column_end': len(line),
                    'suggestion': 'Remove debug print statements before production',
                    'metadata': {'line_content': line.strip()}
                })
        
        # Check for empty file
        if not content.strip():
            issues.append({
                'file_path': file_path,
                'rule_id': 'GEN004',
                'message': 'File contains no code',
                'severity': 'low',
                'issue_type': 'code_smell',
                'line_start': 1,
                'line_end': 1,
                'column_start': 0,
                'column_end': 0,
                'suggestion': 'Remove empty file or add code',
                'metadata': {}
            })
        
        return issues
    
    def get_analysis_status(self, analysis_id: str) -> Dict[str, Any]:
        """Get analysis status"""
        if analysis_id not in self.active_analyses:
            return {
                'status': 'not_found',
                'analysis_id': analysis_id,
                'message': 'Analysis not found'
            }
        
        analysis = self.active_analyses[analysis_id]
        return {
            'status': analysis['status'],
            'analysis_id': analysis_id,
            'project_id': analysis.get('project_id'),
            'progress': analysis.get('progress', 0),
            'started_at': analysis.get('started_at'),
            'completed_at': analysis.get('completed_at'),
            'files_total': len(analysis.get('files', [])),
            'languages': analysis.get('language_counts', {}),
            'error': analysis.get('error') if analysis['status'] == 'failed' else None
        }
    
    def get_analysis_results(self, analysis_id: str) -> Dict[str, Any]:
        """Get analysis results"""
        if analysis_id not in self.active_analyses:
            return {
                'status': 'not_found',
                'analysis_id': analysis_id,
                'message': 'Analysis not found'
            }
        
        analysis = self.active_analyses[analysis_id]
        
        if analysis['status'] != 'completed':
            return {
                'status': analysis['status'],
                'analysis_id': analysis_id,
                'message': f'Analysis is {analysis["status"]}',
                'progress': analysis.get('progress', 0)
            }
        
        return analysis.get('results', {})
    
    def cancel_analysis(self, analysis_id: str) -> bool:
        """Cancel a running analysis"""
        if analysis_id in self.active_analyses and self.active_analyses[analysis_id]['status'] == 'running':
            self.active_analyses[analysis_id]['status'] = 'cancelled'
            logger.info(f"🛑 Cancelled analysis {analysis_id}")
            return True
        return False
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get service statistics"""
        total_analyses = len(self.active_analyses)
        completed = sum(1 for a in self.active_analyses.values() if a['status'] == 'completed')
        running = sum(1 for a in self.active_analyses.values() if a['status'] == 'running')
        failed = sum(1 for a in self.active_analyses.values() if a['status'] == 'failed')
        
        return {
            'total_analyses': total_analyses,
            'completed': completed,
            'running': running,
            'failed': failed,
            'ml_enabled': self.ml_enabled,
            'supported_languages': list(self.parsers.keys()),
            'total_rules': self.rule_stats['total_rules'],
            'rules_by_language': self.rule_stats['by_language']
        }

# Create singleton instance
analysis_service = AnalysisService()
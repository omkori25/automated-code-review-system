# module_backend/services/analysis_service.py
import asyncio
from typing import Dict, Any, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session
import logging

from module_analysis_engine.parsers.python.python_parser import PythonParser
from module_ml.models.bug_predictor import bug_predictor
from module_backend.database.crud_operations import AnalysisCRUD, IssueCRUD

logger = logging.getLogger(__name__)

class AnalysisService:
    def __init__(self):
        self.python_parser = PythonParser()
        self.active_analyses = {}
    
    async def start_analysis(self, db: Session, project_id: str, files: List[Dict[str, str]]):
        """Start code analysis"""
        analysis_id = str(uuid.uuid4())
        
        # Create analysis record
        analysis = AnalysisCRUD.create_analysis(db, {
            "project_id": project_id,
            "status": "running",
            "started_at": datetime.now(),
            "total_files": len(files)
        })
        
        # Store in active analyses
        self.active_analyses[str(analysis.id)] = {
            "status": "running",
            "files": files,
            "results": []
        }
        
        # Start background analysis
        asyncio.create_task(self._run_analysis(db, str(analysis.id), files))
        
        return analysis
    
    async def _run_analysis(self, db: Session, analysis_id: str, files: List[Dict[str, str]]):
        """Run analysis in background"""
        try:
            all_issues = []
            
            for idx, file_info in enumerate(files):
                # Parse file
                if file_info['language'] == 'python':
                    issues = self.python_parser.parse(
                        file_info['content'],
                        file_info['path']
                    )
                    
                    # Run ML prediction
                    ml_result = bug_predictor.predict(file_info['content'])
                    
                    # Combine results
                    for issue in issues:
                        issue_dict = issue.to_dict()
                        issue_dict['analysis_id'] = analysis_id
                        issue_dict['ml_confidence'] = ml_result['overall_risk']
                        
                        # Save to database
                        IssueCRUD.create_issue(db, issue_dict)
                        all_issues.append(issue_dict)
                
                # Update progress
                progress = ((idx + 1) / len(files)) * 100
                self.active_analyses[analysis_id]['progress'] = progress
            
            # Update analysis status
            AnalysisCRUD.update_analysis_status(db, analysis_id, "completed")
            
            # Count issues by severity
            severity_counts = {
                "critical": sum(1 for i in all_issues if i['severity'] == 'critical'),
                "high": sum(1 for i in all_issues if i['severity'] == 'high'),
                "medium": sum(1 for i in all_issues if i['severity'] == 'medium'),
                "low": sum(1 for i in all_issues if i['severity'] == 'low')
            }
            
            # Update analysis with counts
            analysis = AnalysisCRUD.update_analysis_status(db, analysis_id, "completed")
            if analysis:
                analysis.critical_issues = severity_counts['critical']
                analysis.high_issues = severity_counts['high']
                analysis.medium_issues = severity_counts['medium']
                analysis.low_issues = severity_counts['low']
                db.commit()
            
            self.active_analyses[analysis_id]['results'] = all_issues
            self.active_analyses[analysis_id]['status'] = "completed"
            
        except Exception as e:
            logger.error(f"Analysis failed: {e}")
            AnalysisCRUD.update_analysis_status(db, analysis_id, "failed")
            self.active_analyses[analysis_id]['status'] = "failed"
            self.active_analyses[analysis_id]['error'] = str(e)
    
    def get_analysis_status(self, analysis_id: str):
        """Get analysis status"""
        return self.active_analyses.get(analysis_id, {"status": "not_found"})

# Create singleton instance
analysis_service = AnalysisService()
# module_backend/api/routes/analysis_routes.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import chardet
import os
import logging

from module_backend.database.database import get_db
from module_backend.services.analysis_service import analysis_service
from module_backend.database.crud_operations import AnalysisCRUD, IssueCRUD

router = APIRouter(prefix="/analysis", tags=["Analysis"])
logger = logging.getLogger(__name__)

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload files for analysis"""
    file_data = []
    
    for file in files:
        try:
            # Read file content
            content = await file.read()
            
            # Detect encoding
            encoding_result = chardet.detect(content)
            encoding = encoding_result['encoding'] or 'utf-8'
            
            # Decode content
            try:
                text_content = content.decode(encoding)
            except:
                text_content = content.decode('utf-8', errors='ignore')
            
            # Determine language from extension
            ext = os.path.splitext(file.filename)[1].lower()
            language = {
                '.py': 'python',
                '.js': 'javascript',
                '.jsx': 'javascript',
                '.ts': 'typescript',
                '.tsx': 'typescript',
                '.java': 'java',
                '.go': 'go',
                '.rs': 'rust'
            }.get(ext, 'unknown')
            
            file_data.append({
                'path': file.filename,
                'content': text_content,
                'language': language,
                'size': len(content)
            })
            
            logger.info(f"File uploaded: {file.filename} ({language}, {len(content)} bytes)")
            
        except Exception as e:
            logger.error(f"Error uploading file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {file.filename}")
    
    return {"files": file_data}

@router.post("/start/{project_id}")
async def start_analysis(
    project_id: str,
    files: List[dict],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start analysis for uploaded files"""
    try:
        analysis = await analysis_service.start_analysis(db, project_id, files)
        logger.info(f"Analysis started: {analysis.id} for project {project_id}")
        return {"analysis_id": analysis.id, "status": "started"}
    except Exception as e:
        logger.error(f"Failed to start analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get analysis status"""
    status = analysis_service.get_analysis_status(analysis_id)
    return status

@router.get("/results/{analysis_id}")
async def get_analysis_results(
    analysis_id: str,
    db: Session = Depends(get_db)
):
    """Get analysis results"""
    try:
        issues = IssueCRUD.get_analysis_issues(db, analysis_id)
        
        # Count issues by severity
        summary = {
            "critical": sum(1 for i in issues if i.severity == 'critical'),
            "high": sum(1 for i in issues if i.severity == 'high'),
            "medium": sum(1 for i in issues if i.severity == 'medium'),
            "low": sum(1 for i in issues if i.severity == 'low')
        }
        
        return {
            "analysis_id": analysis_id,
            "total_issues": len(issues),
            "issues": [issue.to_dict() for issue in issues],
            "summary": summary
        }
    except Exception as e:
        logger.error(f"Failed to get results: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{issue_id}/false-positive")
async def mark_false_positive(
    issue_id: str,
    db: Session = Depends(get_db)
):
    """Mark an issue as false positive"""
    try:
        issue = IssueCRUD.mark_false_positive(db, issue_id)
        return {"message": "Issue marked as false positive", "issue": issue.to_dict()}
    except Exception as e:
        logger.error(f"Failed to mark false positive: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "analysis-routes",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
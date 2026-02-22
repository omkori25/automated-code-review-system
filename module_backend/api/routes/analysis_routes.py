# module_backend/api/routes/analysis_routes.py
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
import chardet
import os

from module_backend.database.database import get_db
from module_backend.services.analysis_service import analysis_service
from module_backend.database.crud_operations import AnalysisCRUD, IssueCRUD

router = APIRouter(prefix="/analysis", tags=["Analysis"])

@router.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    """Upload files for analysis"""
    file_data = []
    
    for file in files:
        # Read file content
        content = await file.read()
        
        # Detect encoding
        encoding = chardet.detect(content)['encoding'] or 'utf-8'
        
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
            '.java': 'java'
        }.get(ext, 'unknown')
        
        file_data.append({
            'path': file.filename,
            'content': text_content,
            'language': language,
            'size': len(content)
        })
    
    return {"files": file_data}

@router.post("/start/{project_id}")
async def start_analysis(
    project_id: str,
    files: List[dict],
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Start analysis for uploaded files"""
    analysis = await analysis_service.start_analysis(db, project_id, files)
    return {"analysis_id": analysis.id, "status": "started"}

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
    issues = IssueCRUD.get_analysis_issues(db, analysis_id)
    analysis = AnalysisCRUD.update_analysis_status(db, analysis_id, "completed")
    
    return {
        "analysis_id": analysis_id,
        "total_issues": len(issues),
        "issues": [issue.to_dict() for issue in issues],
        "summary": {
            "critical": sum(1 for i in issues if i.severity == 'critical'),
            "high": sum(1 for i in issues if i.severity == 'high'),
            "medium": sum(1 for i in issues if i.severity == 'medium'),
            "low": sum(1 for i in issues if i.severity == 'low')
        }
    }
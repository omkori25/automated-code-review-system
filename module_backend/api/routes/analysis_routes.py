# module_backend/api/routes/analysis_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import chardet
import os
import logging

logger = logging.getLogger(__name__)

# Create router WITHOUT prefix here (prefix will be added in main.py)
router = APIRouter(tags=["Analysis"])

@router.post("/analysis/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload files for analysis"""
    logger.info(f"Received upload request with {len(files)} files")
    file_data = []
    
    for file in files:
        try:
            # Read file content
            content = await file.read()
            logger.info(f"Processing file: {file.filename}, size: {len(content)} bytes")
            
            # Detect encoding
            encoding_result = chardet.detect(content)
            encoding = encoding_result['encoding'] or 'utf-8'
            
            # Decode content
            try:
                text_content = content.decode(encoding)
            except:
                text_content = content.decode('utf-8', errors='ignore')
            
            # Get language from extension
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
            
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {file.filename}")
    
    logger.info(f"Successfully processed {len(file_data)} files")
    return {"files": file_data}

@router.get("/analysis/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get analysis status"""
    return {
        "status": "completed",
        "analysis_id": analysis_id,
        "progress": 100
    }

@router.get("/analysis/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """Get analysis results"""
    return {
        "analysis_id": analysis_id,
        "total_issues": 2,
        "issues": [
            {
                "rule_id": "SEC001",
                "message": "Use of eval detected",
                "severity": "critical",
                "line_start": 3,
                "file_path": "test.py"
            }
        ],
        "summary": {
            "critical": 1,
            "high": 0,
            "medium": 1,
            "low": 0
        }
    }

@router.post("/analysis/start/{project_id}")
async def start_analysis(project_id: str, files: List[dict]):
    """Start analysis for uploaded files"""
    return {
        "analysis_id": "test-123",
        "status": "started"
    }
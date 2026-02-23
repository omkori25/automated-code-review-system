# module_backend/api/routes/analysis_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from typing import List, Optional
import chardet
import os
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(tags=["Analysis"])

# In-memory storage for demo (replace with database later)
analyses = {}

@router.post("/analysis/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    """Upload files for analysis"""
    logger.info(f"📤 Received {len(files)} files for upload")
    
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")
    
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
            except UnicodeDecodeError:
                text_content = content.decode('utf-8', errors='ignore')
            
            # Get language from extension
            ext = os.path.splitext(file.filename)[1].lower()
            language_map = {
                '.py': 'python',
                '.js': 'javascript',
                '.jsx': 'javascript',
                '.ts': 'typescript',
                '.tsx': 'typescript',
                '.java': 'java',
                '.go': 'go',
                '.rs': 'rust',
                '.cpp': 'cpp',
                '.c': 'c',
                '.cs': 'csharp',
                '.php': 'php',
                '.rb': 'ruby',
                '.swift': 'swift',
                '.kt': 'kotlin'
            }
            language = language_map.get(ext, 'unknown')
            
            file_data.append({
                'path': file.filename,
                'content': text_content,
                'language': language,
                'size': len(content),
                'encoding': encoding
            })
            
            logger.info(f"  ✅ Processed: {file.filename} ({language}, {len(content)} bytes)")
            
        except Exception as e:
            logger.error(f"❌ Error processing {file.filename}: {e}")
            raise HTTPException(status_code=500, detail=f"Error processing {file.filename}: {str(e)}")
    
    return {
        "success": True,
        "message": f"Successfully uploaded {len(file_data)} files",
        "files": file_data
    }

@router.post("/analysis/start/{project_id}")
async def start_analysis(
    project_id: str,
    files: List[dict],
    background_tasks: BackgroundTasks
):
    """Start analysis for uploaded files"""
    analysis_id = str(uuid.uuid4())
    
    # Store analysis info
    analyses[analysis_id] = {
        "id": analysis_id,
        "project_id": project_id,
        "status": "running",
        "files": files,
        "started_at": datetime.now().isoformat(),
        "progress": 0
    }
    
    # Start background analysis task
    background_tasks.add_task(run_analysis, analysis_id, files)
    
    logger.info(f"🚀 Started analysis {analysis_id} for project {project_id}")
    
    return {
        "analysis_id": analysis_id,
        "project_id": project_id,
        "status": "started",
        "message": "Analysis started successfully"
    }

@router.get("/analysis/status/{analysis_id}")
async def get_analysis_status(analysis_id: str):
    """Get analysis status"""
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return analyses[analysis_id]

@router.get("/analysis/results/{analysis_id}")
async def get_analysis_results(analysis_id: str):
    """Get analysis results"""
    if analysis_id not in analyses:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    analysis = analyses[analysis_id]
    
    if analysis["status"] != "completed":
        return {
            "analysis_id": analysis_id,
            "status": analysis["status"],
            "message": "Analysis still in progress",
            "progress": analysis.get("progress", 0)
        }
    
    return analysis.get("results", {})

async def run_analysis(analysis_id: str, files: List[dict]):
    """Background task to run analysis"""
    logger.info(f"🔍 Running analysis {analysis_id} on {len(files)} files")
    
    try:
        # Update status
        analyses[analysis_id]["status"] = "running"
        
        # Process each file
        all_issues = []
        for i, file in enumerate(files):
            # Simulate analysis
            import asyncio
            await asyncio.sleep(1)  # Simulate work
            
            # Mock issues for demo
            if file['language'] == 'python':
                issues = [
                    {
                        "rule_id": "SEC001",
                        "message": "Use of eval detected",
                        "severity": "critical",
                        "line_start": 3,
                        "file_path": file['path'],
                        "suggestion": "Avoid using eval. Use safer alternatives."
                    },
                    {
                        "rule_id": "SEC002",
                        "message": "Hardcoded password detected",
                        "severity": "high",
                        "line_start": 5,
                        "file_path": file['path'],
                        "suggestion": "Use environment variables for secrets."
                    }
                ]
                all_issues.extend(issues)
            
            # Update progress
            progress = int(((i + 1) / len(files)) * 100)
            analyses[analysis_id]["progress"] = progress
        
        # Count issues by severity
        summary = {
            "critical": sum(1 for i in all_issues if i['severity'] == 'critical'),
            "high": sum(1 for i in all_issues if i['severity'] == 'high'),
            "medium": sum(1 for i in all_issues if i['severity'] == 'medium'),
            "low": sum(1 for i in all_issues if i['severity'] == 'low')
        }
        
        # Store results
        analyses[analysis_id].update({
            "status": "completed",
            "completed_at": datetime.now().isoformat(),
            "results": {
                "analysis_id": analysis_id,
                "total_issues": len(all_issues),
                "issues": all_issues,
                "summary": summary
            }
        })
        
        logger.info(f"✅ Analysis {analysis_id} completed with {len(all_issues)} issues")
        
    except Exception as e:
        logger.error(f"❌ Analysis {analysis_id} failed: {e}")
        analyses[analysis_id]["status"] = "failed"
        analyses[analysis_id]["error"] = str(e)

@router.post("/analysis/{issue_id}/false-positive")
async def mark_false_positive(issue_id: str):
    """Mark an issue as false positive"""
    return {
        "success": True,
        "message": f"Issue {issue_id} marked as false positive"
    }

@router.get("/analysis/languages")
async def get_supported_languages():
    """Get supported languages"""
    return {
        "languages": [
            "python", "javascript", "typescript", "java",
            "go", "rust", "cpp", "c", "csharp", "php",
            "ruby", "swift", "kotlin"
        ],
        "total": 13
    }
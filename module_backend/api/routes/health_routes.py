# module_backend/api/routes/health_routes.py
from fastapi import APIRouter, Depends
from datetime import datetime
import logging
import sys

logger = logging.getLogger(__name__)

router = APIRouter(tags=["Health"])

@router.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "code-review-backend",
        "version": "1.0.0",
        "python_version": sys.version
    }

@router.get("/health/detailed")
async def detailed_health():
    """Detailed health check with system info"""
    import platform
    import psutil
    
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "system": {
            "platform": platform.platform(),
            "processor": platform.processor(),
            "cpu_count": psutil.cpu_count(),
            "memory": f"{psutil.virtual_memory().percent}% used"
        },
        "service": {
            "name": "code-review-backend",
            "version": "1.0.0",
            "uptime": "N/A"
        }
    }

@router.get("/health/database")
async def database_health():
    """Database connection health"""
    try:
        from module_backend.database.database import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
        
        return {
            "status": "connected",
            "timestamp": datetime.now().isoformat(),
            "database": str(engine.url).split('@')[0].split('://')[0] + "://***@***",
            "connection_test": "passed" if result == 1 else "failed"
        }
    except ImportError:
        return {
            "status": "warning",
            "timestamp": datetime.now().isoformat(),
            "message": "Database module not available",
            "database": "sqlite (default)"
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }

@router.get("/health/ml")
async def ml_health():
    """ML models health check"""
    try:
        from module_ml.models.code_embedder import CodeBERTEmbedder
        embedder = CodeBERTEmbedder()
        
        return {
            "status": "available",
            "timestamp": datetime.now().isoformat(),
            "models": {
                "code_embedder": "loaded",
                "bug_predictor": "available"
            }
        }
    except ImportError as e:
        return {
            "status": "unavailable",
            "timestamp": datetime.now().isoformat(),
            "error": f"ML module not available: {e}",
            "models": {}
        }
    except Exception as e:
        return {
            "status": "error",
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }
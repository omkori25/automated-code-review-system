# module_backend/api/routes/health_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from module_backend.database.database import get_db
from module_backend.database import models
import logging

router = APIRouter(prefix="/health", tags=["Health"])
logger = logging.getLogger(__name__)

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "code-review-backend",
        "version": "1.0.0"
    }

@router.get("/database")
async def database_health(db: Session = Depends(get_db)):
    """Check database connection"""
    try:
        # Try to execute a simple query
        db.execute("SELECT 1").first()
        return {
            "status": "connected",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return {
            "status": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }
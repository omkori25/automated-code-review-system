# module_backend/api/main.py
import sys
import os
from pathlib import Path
import logging

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers - FIXED IMPORTS
from module_backend.api.routes import health_routes, analysis_routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import settings
try:
    from module_utils.config.settings import settings
    logger.info(f"✅ Settings loaded: {settings.APP_NAME}")
except Exception as e:
    logger.warning(f"⚠️ Could not load settings: {e}")
    
    class DummySettings:
        CORS_ORIGINS = ["*"]
        DEBUG = True
        ENVIRONMENT = "development"
        APP_NAME = "Code Review API"
    settings = DummySettings()

# Create FastAPI app
app = FastAPI(
    title="Code Review API",
    description="Automated Code Review & Bug Detection System",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, 'CORS_ORIGINS', ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers - THIS IS CRITICAL
app.include_router(health_routes.router, prefix="/api", tags=["Health"])
app.include_router(analysis_routes.router, prefix="/api", tags=["Analysis"])

# Also include without /api prefix for backward compatibility
app.include_router(health_routes.router)
app.include_router(analysis_routes.router)

@app.get("/")
async def root():
    return {
        "message": "Code Review API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "health": "/health",
            "analysis": "/analysis/upload"
        }
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "timestamp": __import__('datetime').datetime.now().isoformat(),
        "service": "code-review-backend",
        "version": "1.0.0"
    }

@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Starting up Code Review API...")
    logger.info(f"Registered routes: {[route.path for route in app.routes]}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "module_backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
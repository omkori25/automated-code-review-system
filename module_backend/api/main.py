# module_backend/api/main.py
import sys
import os
from pathlib import Path
import logging
from datetime import datetime

# Add project root to Python path
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
    print(f"📂 Added {project_root} to Python path")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import settings
try:
    from module_utils.config.settings import settings
    logger.info(f"✅ Settings loaded: {settings.APP_NAME}")
except Exception as e:
    logger.warning(f"⚠️ Using default settings: {e}")
    
    class DefaultSettings:
        CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173", "*"]
        DEBUG = True
        ENVIRONMENT = "development"
        APP_NAME = "Code Review API"
        VERSION = "1.0.0"
        DATABASE_URL = "sqlite:///./test.db"
    settings = DefaultSettings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Automated Code Review & Bug Detection System",
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=getattr(settings, 'CORS_ORIGINS', ["*"]),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
try:
    from module_backend.api.routes import health_routes, analysis_routes
    
    # Include with multiple prefixes for compatibility
    app.include_router(health_routes.router, prefix="/api", tags=["Health"])
    app.include_router(analysis_routes.router, prefix="/api", tags=["Analysis"])
    app.include_router(health_routes.router, tags=["Health"])  # Also at root
    app.include_router(analysis_routes.router, tags=["Analysis"])  # Also at root
    
    logger.info("✅ Routes loaded successfully")
except Exception as e:
    logger.error(f"❌ Failed to load routes: {e}")

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Code Review API",
        "version": settings.VERSION,
        "status": "running",
        "environment": settings.ENVIRONMENT,
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "analysis": "/analysis/upload",
            "api": "/api"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": settings.APP_NAME,
        "version": settings.VERSION
    }

@app.get("/health/database")
async def database_health():
    """Database health check"""
    try:
        from module_backend.database.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "timestamp": datetime.now().isoformat(),
            "database": str(engine.url).split('@')[0] + '@...'  # Hide credentials
        }
    except Exception as e:
        return {
            "status": "disconnected",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("🚀 Starting Code Review API...")
    
    # Log all registered routes
    routes = [{"path": route.path, "name": route.name} for route in app.routes]
    logger.info(f"📋 Registered {len(routes)} routes")
    
    # Initialize database
    try:
        from module_backend.database.database import init_db
        init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️ Database initialization skipped: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("🛑 Shutting down Code Review API...")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"💥 Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "module_backend.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
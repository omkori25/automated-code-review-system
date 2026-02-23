# module_utils/config/settings.py - Simplified version
import os
from typing import List
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings:
    """Application settings loaded from environment variables"""
    
    def __init__(self):
        # Database
        self.DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:admin123@localhost:5433/code_review_db")
        
        # Environment
        self.ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
        self.DEBUG = os.getenv("DEBUG", "True").lower() == "true"
        
        # Security
        self.SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-in-production")
        
        # API Settings
        self.APP_NAME = os.getenv("APP_NAME", "Code Review API")
        self.VERSION = os.getenv("VERSION", "1.0.0")
        
        # CORS - parse from string to list
        cors_str = os.getenv("CORS_ORIGINS", '["http://localhost:3000"]')
        try:
            self.CORS_ORIGINS = eval(cors_str)
        except:
            self.CORS_ORIGINS = ["http://localhost:3000"]
        
        # File Upload
        self.MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
        extensions_str = os.getenv("ALLOWED_EXTENSIONS", ".py,.js,.jsx,.ts,.java")
        self.ALLOWED_EXTENSIONS = [ext.strip() for ext in extensions_str.split(",")]
        
        # ML Settings
        self.ML_MODEL_PATH = os.getenv("ML_MODEL_PATH", "./models")
        self.ENABLE_ML_ANALYSIS = os.getenv("ENABLE_ML_ANALYSIS", "True").lower() == "true"

# Create a global settings instance
settings = Settings()
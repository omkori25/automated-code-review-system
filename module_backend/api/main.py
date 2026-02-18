# module_utils/logging/logger_config.py
import logging
import logging.config
import sys
import os
from datetime import datetime

def setup_logging():
    """Configure logging for the application"""
    
    # Create logs directory if it doesn't exist
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename with timestamp
    log_filename = os.path.join(
        log_dir, 
        f"codereview_{datetime.now().strftime('%Y%m%d')}.log"
    )
    
    # Logging configuration
    LOGGING_CONFIG = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
            "colored": {
                "format": "\033[36m%(asctime)s\033[0m - \033[32m%(name)s\033[0m - \033[1m%(levelname)s\033[0m - %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": "INFO",
                "formatter": "colored",
                "stream": sys.stdout
            },
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "DEBUG",
                "formatter": "detailed",
                "filename": log_filename,
                "maxBytes": 10485760,  # 10MB
                "backupCount": 5,
                "encoding": "utf8"
            },
            "error_file": {
                "class": "logging.handlers.RotatingFileHandler",
                "level": "ERROR",
                "formatter": "detailed",
                "filename": os.path.join(log_dir, "errors.log"),
                "maxBytes": 10485760,
                "backupCount": 5,
                "encoding": "utf8"
            }
        },
        "root": {
            "level": "DEBUG",
            "handlers": ["console", "file", "error_file"]
        },
        "loggers": {
            "uvicorn": {
                "level": "INFO",
                "handlers": ["console"],
                "propagate": False
            },
            "uvicorn.error": {
                "level": "INFO",
                "handlers": ["error_file"],
                "propagate": False
            },
            "sqlalchemy": {
                "level": "WARNING",
                "handlers": ["console"],
                "propagate": False
            },
            "module_backend": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "module_ml": {
                "level": "INFO",
                "handlers": ["console", "file"],
                "propagate": False
            },
            "module_analysis_engine": {
                "level": "DEBUG",
                "handlers": ["console", "file"],
                "propagate": False
            }
        }
    }
    
    # Apply configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log startup
    logging.info("="*60)
    logging.info("🚀 Logging configured successfully")
    logging.info(f"Log file: {log_filename}")
    logging.info("="*60)
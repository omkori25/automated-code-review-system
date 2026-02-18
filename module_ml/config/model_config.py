# module_ml/config/model_config.py
from dataclasses import dataclass
from typing import Dict, Any
import os

@dataclass
class ModelConfig:
    """Configuration for ML models"""
    
    # Model paths
    BASE_PATH: str = os.path.join(os.path.dirname(__file__), "..", "models")
    
    # Bug Detection Model
    BUG_MODEL: Dict[str, Any] = None
    
    # CodeBERT Model
    CODEBERT_MODEL: str = "microsoft/codebert-base"
    
    # Training parameters
    BATCH_SIZE: int = 32
    LEARNING_RATE: float = 2e-5
    EPOCHS: int = 10
    MAX_SEQUENCE_LENGTH: int = 512
    
    # Inference parameters
    CONFIDENCE_THRESHOLD: float = 0.7
    DEVICE: str = "cuda" if os.path.exists("/dev/nvidia0") else "cpu"
    
    def __post_init__(self):
        """Initialize after creation"""
        self.BUG_MODEL = {
            "bug_detector": os.path.join(self.BASE_PATH, "bug_detector.pth"),
            "security_classifier": os.path.join(self.BASE_PATH, "security.pth"),
            "code_smell_detector": os.path.join(self.BASE_PATH, "code_smell.pth"),
            "performance_analyzer": os.path.join(self.BASE_PATH, "performance.pth")
        }
        
        # Create directories if they don't exist
        os.makedirs(self.BASE_PATH, exist_ok=True)
        for path in self.BUG_MODEL.values():
            os.makedirs(os.path.dirname(path), exist_ok=True)

# Create global config instance
config = ModelConfig()
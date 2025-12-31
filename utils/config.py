import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    Centralized Configuration Object.
    Manages paths, constants, and environment variables.
    """
    # Base Project Paths
    BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    SRC_DIR = BASE_DIR / "src"
    TESTS_DIR = BASE_DIR / "tests"
    
    # Sub-directories
    RAW_DATA_PATH = DATA_DIR / "raw"
    PROCESSED_DATA_PATH = DATA_DIR / "processed"
    ARTIFACTS_PATH = DATA_DIR / "artifacts"
    
    # Model Configuration
    RANDOM_SEED = 42
    TEST_SIZE = 0.2
    
    # Validation Thresholds
    MAX_NULL_PERCENTAGE = 0.4
    
    @classmethod
    def ensure_directories(cls):
        """Creates necessary directories if they don't exist."""
        cls.ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)
        cls.PROCESSED_DATA_PATH.mkdir(parents=True, exist_ok=True)

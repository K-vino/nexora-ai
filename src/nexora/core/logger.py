import logging
import sys
from pathlib import Path

class Logger:
    """
    Singleton Logger for Nexora AI.
    Ensures consistent logging format and destination across the application.
    """
    _instance = None

    @staticmethod
    def get_logger(name: str) -> logging.Logger:
        if Logger._instance is None:
            Logger._instance = Logger._setup_logger()
        return logging.getLogger(f"Nexora.{name}")

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger("Nexora")
        logger.setLevel(logging.INFO)
        
        # Prevent adding handlers multiple times
        if not logger.handlers:
            # Console Handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
            # File Handler (Optional, could be added here)
            
        return logger

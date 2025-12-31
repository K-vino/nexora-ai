from dl_engine.base_dl_model import BaseDLModel
from typing import Dict, Any, Tuple
import numpy as np
from utils.logging import Logger

class LSTMModel(BaseDLModel):
    """
    LSTM implementation for sequential data.
    """
    def __init__(self):
        self.logger = Logger.get_logger("LSTMModel")
        
    def build(self, input_shape: Tuple[int, ...]):
        # LSTM requires (batch, timesteps, features)
        # Tabular data usually lacks 'timesteps' unless engineered.
        pass

    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        self.logger.warning("LSTM training requested but tabular data lacks temporal sequence structure.")
        self.logger.info("Skipping LSTM training. Returning empty logs.")
        return {"status": "skipped", "reason": "No temporal structure in features (Phase-1 check)"}

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        return {}

    def predict(self, X: np.ndarray) -> np.ndarray:
        return np.zeros(len(X))

    @staticmethod
    def is_suitable(metadata: Dict[str, Any]) -> bool:
        """
        Checks if data is suitable for LSTM (e.g., Time Series).
        """
        # Phase-3 logic: Check metadata for time-series flags or specific ordering
        # For housing.csv, this is likely False.
        if "time_series" in metadata.get("tags", []):
            return True
        return False

from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple

class BaseDLModel(ABC):
    """
    Abstract interface for Nexora Deep Learning models (ANN, LSTM).
    """
    
    @abstractmethod
    def build(self, input_shape: Tuple[int, ...]):
        """Builds and compiles the neural network structure."""
        pass

    @abstractmethod
    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        """
        Trains the model and returns history/logs.
        Should handle EarlyStopping and Checkpointing internally.
        """
        pass

    @abstractmethod
    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        """Returns evaluation metrics (comparable to ML metrics)."""
        pass
    
    @abstractmethod
    def predict(self, X: np.ndarray) -> np.ndarray:
        """Returns predictions."""
        pass

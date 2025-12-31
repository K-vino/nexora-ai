from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Optional, Dict

class BaseMLModel(ABC):
    """
    Abstract interface for all Nexora ML models.
    """
    
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series):
        """Trains the model."""
        pass

    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Predictions."""
        pass
        
    @abstractmethod
    def evaluate(self, y_true: pd.Series, y_pred: np.ndarray) -> Dict[str, float]:
        """Returns specific metrics for the model type."""
        pass
        
    def get_feature_importance(self) -> Optional[pd.DataFrame]:
        """Returns feature importance if applicable."""
        return None

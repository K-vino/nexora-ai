from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
from typing import Any, Dict, Optional

class ModelStrategy(ABC):
    """
    Strategy Interface for ML Models.
    Allows runtime swapping of algorithms (e.g., swapping RF for LinearReg).
    """
    
    @abstractmethod
    def train(self, X: pd.DataFrame, y: pd.Series, params: Optional[Dict[str, Any]] = None) -> Any:
        """Train the model."""
        pass
        
    @abstractmethod
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """Generate predictions."""
        pass

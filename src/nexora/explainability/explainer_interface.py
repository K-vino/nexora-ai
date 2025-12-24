from abc import ABC, abstractmethod
from typing import Any, Dict
import pandas as pd

class Explainer(ABC):
    """Interface for Model Explainability."""
    
    @abstractmethod
    def explain_global(self, model: Any, X: pd.DataFrame) -> Dict[str, float]:
        """Return feature importance map."""
        pass

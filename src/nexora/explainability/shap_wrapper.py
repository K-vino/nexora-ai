import pandas as pd
import numpy as np
from typing import Any, Dict
from nexora.explainability.explainer_interface import Explainer
from nexora.core.logger import Logger

class SHAPWrapper(Explainer):
    """
    Simulates SHAP explanation for demonstration (simplifies dependencies).
    Extracts feature importances directly from tree-based models.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("SHAPWrapper")
        
    def explain_global(self, model: Any, X: pd.DataFrame) -> Dict[str, float]:
        self.logger.info("Computing global feature importance...")
        
        # 1. Tree-based importance (Random Forest, XGBoost)
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
            return dict(zip(X.columns, importances))
            
        # 2. Linear models (Coefficients)
        if hasattr(model, "coef_"):
            importances = np.abs(model.coef_)
            if importances.ndim > 1:
                importances = importances[0] # Take first class for binary clf
            return dict(zip(X.columns, importances))
            
        self.logger.warning("Model does not expose feature importances. Returning empty.")
        return {}

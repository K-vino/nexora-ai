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
        
        # 0. Try real SHAP if available
        try:
            import shap
            # Sampling for speed if dataset is huge
            X_sample = X.sample(min(len(X), 100), random_state=42)
            
            # Determine explainer type
            if hasattr(model, "feature_importances_"):
                 explainer = shap.TreeExplainer(model)
                 shap_values = explainer.shap_values(X_sample)
            else:
                 # Linear/Generic (Summarizer needed for speed)
                 explainer = shap.LinearExplainer(model, X_sample)
                 shap_values = explainer.shap_values(X_sample)

            # Handle shape variants (Binary class returns list)
            if isinstance(shap_values, list):
                shap_values = shap_values[1] # Positive class
                
            # Aggregate absolute mean
            vals = np.abs(shap_values).mean(0)
            return dict(zip(X.columns, vals))

        except ImportError:
            self.logger.warning("SHAP library not found. Falling back to simple importance.")
        except Exception as e:
            self.logger.warning(f"SHAP explanation failed ({e}). Falling back to simple importance.")

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

import pandas as pd
from typing import Dict, Any, List
from utils.logging import Logger

class FeatureImportance:
    """
    Standardizes feature importance extraction across models.
    """
    def __init__(self):
        self.logger = Logger.get_logger("FeatureImportance")
        
    def extract(self, model_results: Dict[str, Any], best_model_name: str) -> List[Dict[str, Any]]:
        """
        Extracts importance from selected model results.
        """
        if best_model_name not in model_results:
            self.logger.warning("Best model not found in results.")
            return []
            
        importance_data = model_results[best_model_name].get("feature_importance")
        
        if importance_data:
            self.logger.info(f"Extracted importance for top {len(importance_data)} features.")
            return importance_data
        else:
            self.logger.warning(f"No feature importance available for {best_model_name}")
            return []

import numpy as np
import pandas as pd
from typing import Dict
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score, accuracy_score, f1_score # type: ignore
from utils.logging import Logger

class ModelEvaluator:
    """
    Calculates metrics for Regression and Classification.
    """
    def __init__(self):
        self.logger = Logger.get_logger("ModelEvaluator")

    def evaluate(self, y_true, y_pred, task_type: str) -> Dict[str, float]:
        """
        Returns a dictionary of metrics based on task type.
        """
        metrics = {}
        
        if task_type == "regression":
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            
            metrics = {
                "RMSE": round(rmse, 4),
                "MAE": round(mae, 4),
                "R2": round(r2, 4)
            }
            
        elif task_type == "classification":
            acc = accuracy_score(y_true, y_pred)
            f1 = f1_score(y_true, y_pred, average='weighted')
            
            metrics = {
                "Accuracy": round(acc, 4),
                "F1_Score": round(f1, 4)
            }
            
        else:
            raise ValueError(f"Unknown task type: {task_type}")
            
        self.logger.info(f"Evaluation metrics: {metrics}")
        return metrics

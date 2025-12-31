from typing import Dict
import numpy as np
import pandas as pd
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, f1_score, mean_absolute_error, precision_score, recall_score
from utils.logging import Logger

class ModelEvaluator:
    """
    Calculates deterministic performance metrics.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("ModelEvaluator")
        
    def evaluate(self, y_true: np.ndarray, y_pred: np.ndarray, task_type: str) -> Dict[str, float]:
        """
        Evaluate predictions against ground truth.
        """
        self.logger.info(f"Evaluating {task_type} model...")
        metrics = {}
        
        if task_type == "regression":
            mse = mean_squared_error(y_true, y_pred)
            rmse = float(np.sqrt(mse))
            mae = mean_absolute_error(y_true, y_pred)
            r2 = r2_score(y_true, y_pred)
            metrics = {"rmse": rmse, "mae": mae, "r2": r2}
            
        elif task_type == "classification":
            acc = accuracy_score(y_true, y_pred)
            precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
            recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
            f1 = f1_score(y_true, y_pred, average='weighted')
            metrics = {
                "accuracy": acc, 
                "precision": precision, 
                "recall": recall, 
                "f1_score": f1
            }
            
        self.logger.info(f"Metrics: {metrics}")
        return metrics

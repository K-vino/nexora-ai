from typing import Dict, Any, List
from ml_engine.base_model import BaseMLModel
from ml_engine.regression_models import LinearRegressionModel, RidgeRegressionModel, RandomForestRegressionModel
from utils.logging import Logger
import pandas as pd

class ModelTrainer:
    """
    Trains multiple candidate models and selects the best one.
    """
    def __init__(self):
        self.logger = Logger.get_logger("ModelTrainer")
        self.models: Dict[str, BaseMLModel] = {}
        self.results: Dict[str, Any] = {}
        
    def train_and_evaluate(self, X_train, y_train, X_test, y_test, task_type: str) -> Dict[str, Any]:
        """
        Trains a suite of models appropriate for the task and compares them.
        """
        self.logger.info(f"Starting model training for task: {task_type}")
        
        # 1. Select Candidates
        if task_type == "regression":
            self.models = {
                "Linear Regression": LinearRegressionModel(),
                "Ridge Regression": RidgeRegressionModel(),
                "Random Forest": RandomForestRegressionModel()
            }
        else:
             # Placeholder for classification
             raise NotImplementedError("Classification not yet implemented in Phase-2 trainer.")
             
        best_score = -float('inf') 
        best_model_name = None
        
        # 2. Train & Eval Loop
        for name, model in self.models.items():
            self.logger.info(f"Training {name}...")
            model.train(X_train, y_train)
            
            preds = model.predict(X_test)
            metrics = model.evaluate(y_test, preds)
            
            importance = model.get_feature_importance()
            
            self.results[name] = {
                "metrics": metrics,
                "feature_importance": importance.to_dict(orient="records") if importance is not None else None
            }
            
            # Selection Logic (Maximize R2 or Minimize RMSE)
            # Using R2 for simplicity, higher is better
            score = metrics.get("R2", -float('inf'))
            if score > best_score:
                best_score = score
                best_model_name = name
                
        self.logger.info(f"Best model selected: {best_model_name} with R2: {best_score}")
        
        return {
            "best_model": best_model_name,
            "reason": f"Highest R2 Score ({best_score}) on test set.",
            "all_results": self.results
        }

    def get_model(self, name: str) -> BaseMLModel:
        return self.models[name]

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.base import BaseEstimator
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from nexora.modeling.model_interface import ModelStrategy
from nexora.core.logger import Logger

class RandomForestClassificationStrategy(ModelStrategy):
    """Random Forest Classifier Strategy."""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.logger = Logger.get_logger("RandomForestClf")
        
    def train(self, X: pd.DataFrame, y: pd.Series, params: Optional[Dict[str, Any]] = None) -> BaseEstimator:
        self.logger.info("Training Random Forest Classifier...")
        if params:
            self.model.set_params(**params)
        self.model.fit(X, y)
        return self.model
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

class LogisticRegressionStrategy(ModelStrategy):
    """Logistic Regression Strategy."""
    
    def __init__(self):
        self.model = LogisticRegression(max_iter=1000)
        self.logger = Logger.get_logger("LogisticReg")
        
    def train(self, X: pd.DataFrame, y: pd.Series, params: Optional[Dict[str, Any]] = None) -> BaseEstimator:
        self.logger.info("Training Logistic Regressor...")
        self.model.fit(X, y)
        return self.model
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

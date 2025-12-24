from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.base import BaseEstimator
import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from nexora.modeling.model_interface import ModelStrategy
from nexora.core.logger import Logger

class RandomForestRegressionStrategy(ModelStrategy):
    """Random Forest Regressor Strategy."""
    
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.logger = Logger.get_logger("RandomForestReg")
        
    def train(self, X: pd.DataFrame, y: pd.Series, params: Optional[Dict[str, Any]] = None) -> BaseEstimator:
        self.logger.info("Training Random Forest Regressor...")
        if params:
            self.model.set_params(**params)
        self.model.fit(X, y)
        return self.model
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

class LinearRegressionStrategy(ModelStrategy):
    """Linear Regression Strategy."""
    
    def __init__(self):
        self.model = LinearRegression()
        self.logger = Logger.get_logger("LinearReg")
        
    def train(self, X: pd.DataFrame, y: pd.Series, params: Optional[Dict[str, Any]] = None) -> BaseEstimator:
        self.logger.info("Training Linear Regressor...")
        self.model.fit(X, y)
        return self.model
        
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        return self.model.predict(X)

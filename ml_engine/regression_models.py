from ml_engine.base_model import BaseMLModel
from ml_engine.model_evaluator import ModelEvaluator
from sklearn.linear_model import LinearRegression, Ridge # type: ignore
from sklearn.ensemble import RandomForestRegressor # type: ignore
import pandas as pd
import numpy as np
from typing import Dict

class LinearRegressionModel(BaseMLModel):
    def __init__(self):
        self.model = LinearRegression()
        self.evaluator = ModelEvaluator()
        
    def train(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def evaluate(self, y_true, y_pred):
        return self.evaluator.evaluate(y_true, y_pred, "regression")
        
    def get_feature_importance(self):
        # Linear models have coefficients
        if hasattr(self.model, "coef_"):
             return pd.DataFrame({
                 "feature": self.model.feature_names_in_ if hasattr(self.model, "feature_names_in_") else [f"f{i}" for i in range(len(self.model.coef_))],
                 "importance": np.abs(self.model.coef_)
             }).sort_values(by="importance", ascending=False)
        return None

class RidgeRegressionModel(BaseMLModel):
    def __init__(self, alpha=1.0):
        self.model = Ridge(alpha=alpha)
        self.evaluator = ModelEvaluator()
        
    def train(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def evaluate(self, y_true, y_pred):
        return self.evaluator.evaluate(y_true, y_pred, "regression")

class RandomForestRegressionModel(BaseMLModel):
    def __init__(self, n_estimators=100, random_state=42):
        self.model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
        self.evaluator = ModelEvaluator()
        
    def train(self, X, y):
        self.model.fit(X, y)
        
    def predict(self, X):
        return self.model.predict(X)
        
    def evaluate(self, y_true, y_pred):
        return self.evaluator.evaluate(y_true, y_pred, "regression")
        
    def get_feature_importance(self):
        if hasattr(self.model, "feature_importances_"):
             return pd.DataFrame({
                 "feature": self.model.feature_names_in_ if hasattr(self.model, "feature_names_in_") else [f"f{i}" for i in range(len(self.model.feature_importances_))],
                 "importance": self.model.feature_importances_
             }).sort_values(by="importance", ascending=False)
        return None

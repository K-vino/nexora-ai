import pandas as pd
import numpy as np
from nexora.feature_engineering.engineer_interface import FeatureEngineer
from nexora.core.logger import Logger

class CategoricalEncoder(FeatureEngineer):
    """
    Handles categorical variables using One-Hot Encoding.
    Ensures train-serving skew is handled by aligning columns.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("CategoricalEncoder")
        self.cat_columns = []
        self.encoded_columns_ = []
        
    def fit(self, df: pd.DataFrame) -> 'CategoricalEncoder':
        self.logger.info("Fitting CategoricalEncoder...")
        
        # Identify categorical columns
        self.cat_columns = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if not self.cat_columns:
            self.logger.warning("No categorical columns found.")
            self.encoded_columns_ = df.columns.tolist()
            return self
            
        # Simulate One-Hot Encoding to get final column names
        # We process detailed encoding logic
        temp_df = pd.get_dummies(df, columns=self.cat_columns)
        self.encoded_columns_ = temp_df.columns.tolist()
        
        self.logger.info(f"Learned schema with {len(self.encoded_columns_)} columns (expanded from {len(df.columns)}).")
        return self
        
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info("Transforming categorical features...")
        
        if not self.cat_columns:
            return df
            
        # Perform One-Hot Encoding
        df_encoded = pd.get_dummies(df, columns=self.cat_columns)
        
        # Align with fitted columns (add missing, remove extra)
        # 1. Add missing columns with 0
        missing_cols = set(self.encoded_columns_) - set(df_encoded.columns)
        for c in missing_cols:
            df_encoded[c] = 0
            
        # 2. Select only fitted columns in correct order
        # This implicitly drops extra columns seen in new data but not in train
        df_encoded = df_encoded[self.encoded_columns_]
        
        return df_encoded

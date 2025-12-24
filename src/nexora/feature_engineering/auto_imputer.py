import pandas as pd
import numpy as np
from nexora.feature_engineering.engineer_interface import FeatureEngineer
from nexora.core.logger import Logger

class AutoImputer(FeatureEngineer):
    """
    Automatically fills missing values using Median (Numerical) and Mode (Categorical).
    Prevents data leakage by storing learned values during fit().
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("AutoImputer")
        self.imputation_values = {}
        
    def fit(self, df: pd.DataFrame) -> 'AutoImputer':
        self.logger.info("Fitting AutoImputer...")
        
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                median_val = df[col].median()
                self.imputation_values[col] = median_val
            else:
                mode_vals = df[col].mode()
                if not mode_vals.empty:
                    self.imputation_values[col] = mode_vals[0]
                else:
                    self.imputation_values[col] = "Missing"
                    
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.logger.info(f"Imputing missing values for {len(self.imputation_values)} columns...")
        df_copy = df.copy()
        
        df_copy = df_copy.fillna(value=self.imputation_values)
        
        # Fallback for columns not seen in fit but present in transform (if any)
        # In a strict pipeline, we might ignore or raise error. Here we leave them as is.
        
        return df_copy

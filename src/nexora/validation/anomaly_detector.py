import pandas as pd
import numpy as np
from nexora.core.logger import Logger

class AnomalyDetector:
    """
    Detects statistical anomalies using IQR (Interquartile Range).
    """
    
    def __init__(self, factor: float = 1.5):
        self.logger = Logger.get_logger("AnomalyDetector")
        self.factor = factor
        
    def detect_outliers(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Returns a dataframe indicating True for outlier values in numerical columns.
        """
        self.logger.info("Detecting anomalies using IQR method...")
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numerical_cols) == 0:
            self.logger.warning("No numerical columns found for anomaly detection.")
            return pd.DataFrame(False, index=df.index, columns=df.columns)
            
        Q1 = df[numerical_cols].quantile(0.25)
        Q3 = df[numerical_cols].quantile(0.75)
        IQR = Q3 - Q1
        
        outliers = ((df[numerical_cols] < (Q1 - self.factor * IQR)) | 
                    (df[numerical_cols] > (Q3 + self.factor * IQR)))
                    
        total_outliers = outliers.sum().sum()
        self.logger.info(f"Detected {total_outliers} outlier values across {len(numerical_cols)} columns.")
        
        return outliers

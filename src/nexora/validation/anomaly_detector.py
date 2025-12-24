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

    def detect_anomalies_isolation_forest(self, df: pd.DataFrame, contamination: float = 0.05) -> pd.Series:
        """
        Detects anomalies using Isolation Forest algorithm.
        Returns a boolean Series (True = anomaly).
        """
        self.logger.info(f"Detecting anomalies using Isolation Forest (contamination={contamination})...")
        
        try:
            from sklearn.ensemble import IsolationForest
            
            numerical_cols = df.select_dtypes(include=[np.number]).columns
            if len(numerical_cols) == 0:
                self.logger.warning("No numerical columns for Isolation Forest.")
                return pd.Series(False, index=df.index)
                
            model = IsolationForest(contamination=contamination, random_state=42)
            # IsolationForest returns -1 for outliers, 1 for inliers
            preds = model.fit_predict(df[numerical_cols])
            
            is_outlier = pd.Series(preds == -1, index=df.index)
            self.logger.info(f"Isolation Forest detected {is_outlier.sum()} anomalies.")
            
            return is_outlier
            
        except ImportError:
            self.logger.error("Scikit-learn not installed. Cannot run Isolation Forest.")
            raise ImportError("Please install scikit-learn to use Isolation Forest.")
        except Exception as e:
            self.logger.error(f"Isolation Forest failed: {e}")
            return pd.Series(False, index=df.index)

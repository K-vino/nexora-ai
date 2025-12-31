from abc import ABC, abstractmethod
import pandas as pd

class FeatureEngineer(ABC):
    """
    Abstract Base Class for Feature Engineering Transformers.
    Follows Sklearn-style API (fit, transform).
    """
    
    @abstractmethod
    def fit(self, df: pd.DataFrame) -> 'FeatureEngineer':
        """Learn parameters from data."""
        pass
        
    @abstractmethod
    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply transformations."""
        pass
        
    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        self.fit(df)
        return self.transform(df)

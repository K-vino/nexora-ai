from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class DataValidator(ABC):
    """
    Abstract Base Class for Data Validators.
    """
    
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """
        Validate the dataframe against specific rules.
        
        Args:
            df (pd.DataFrame): The dataframe to check.
            
        Returns:
            bool: True if valid, raises ValidationError otherwise.
        """
        pass

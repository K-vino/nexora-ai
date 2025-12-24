from abc import ABC, abstractmethod
import pandas as pd
from typing import Dict, Any

class DataConnector(ABC):
    """
    Abstract Base Class for Data Connectors.
    Enforces a contract for loading data from various sources.
    """
    
    @abstractmethod
    def load_data(self, source: str) -> pd.DataFrame:
        """
        Load data from the given source.
        
        Args:
            source (str): The path, URL, or connection string to the data.
            
        Returns:
            pd.DataFrame: The loaded data as a pandas DataFrame.
            
        Raises:
            DataIngestionError: If data cannot be loaded.
        """
        pass

    @abstractmethod
    def get_preview(self, source: str, rows: int = 5) -> pd.DataFrame:
        """
        Get a small preview of the data without loading everything.
        """
        pass
        
    @abstractmethod
    def get_metadata(self, source: str) -> Dict[str, Any]:
        """
        Extract metadata (rows, columns, types, file size) without full load if possible.
        """
        pass

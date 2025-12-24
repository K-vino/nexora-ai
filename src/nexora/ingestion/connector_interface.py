from abc import ABC, abstractmethod
import pandas as pd

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

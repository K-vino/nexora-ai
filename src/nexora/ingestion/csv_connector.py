import pandas as pd
from pathlib import Path
import os
from nexora.ingestion.connector_interface import DataConnector
from nexora.core.exceptions import DataIngestionError
from nexora.core.logger import Logger

class CSVConnector(DataConnector):
    """
    Concrete Connector for CSV files.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("CSVConnector")
        
    def load_data(self, source: str) -> pd.DataFrame:
        self.logger.info(f"Attempting to load CSV data from: {source}")
        
        path = Path(source)
        if not path.exists():
            self.logger.error(f"File not found: {source}")
            raise DataIngestionError(f"CSV file not found at {source}")
            
        try:
            df = pd.read_csv(path)
            if df.empty:
                self.logger.warning(f"File {source} is empty.")
                raise DataIngestionError("Loaded CSV is empty.")
                
            self.logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
            return df
            
        except pd.errors.ParserError as e:
            self.logger.error(f"Failed to parse CSV: {e}")
            raise DataIngestionError(f"CSV parsing failed: {e}")
        except Exception as e:
            self.logger.error(f"Unexpected error loading CSV: {e}")
            raise DataIngestionError(f"Unexpected error: {e}")

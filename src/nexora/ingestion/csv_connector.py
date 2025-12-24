import pandas as pd
from pathlib import Path
import os
from typing import Dict, Any
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

    def get_preview(self, source: str, rows: int = 5) -> pd.DataFrame:
        try:
            return pd.read_csv(source, nrows=rows)
        except Exception as e:
            raise DataIngestionError(f"Failed to preview CSV: {e}")

    def get_metadata(self, source: str) -> Dict[str, Any]:
        try:
            # Efficiently read just header and shape if possible, but for CSV we might need to parse
            # For speed on large files, we can count lines for rows (approx) or just read header for cols
            # For now, let's use pandas but maybe strict on memory
            df_iter = pd.read_csv(source, iterator=True, chunksize=1000)
            first_chunk = next(df_iter)
            
            columns = first_chunk.columns.tolist()
            dtypes = {col: str(dtype) for col, dtype in first_chunk.dtypes.items()}
            
            # Count rows (expensive for huge files, but safe for now)
            # A faster way is line counting, but let's stick to simple logic for MVP
            path = Path(source)
            file_size_mb = path.stat().st_size / (1024 * 1024)
            
            return {
                "columns": columns,
                "dtypes": dtypes,
                "file_size_mb": round(file_size_mb, 2),
                # "rows": ... # Skipping exact row count for speed on large files unless requested
            }
        except Exception as e:
            raise DataIngestionError(f"Failed to extract metadata: {e}")

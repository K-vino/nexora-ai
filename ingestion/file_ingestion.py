import pandas as pd
import os
import datetime
from typing import Dict, Any, Optional
from utils.data_types import DataBundle
from utils.logging import Logger

class FileIngestion:
    """
    Ingests data from files (CSV, Excel) into a standard DataBundle.
    """
    def __init__(self):
        self.logger = Logger.get_logger("FileIngestion")

    def ingest_csv(self, file_path: str, source_name: str = "file") -> DataBundle:
        """
        Reads a CSV file and wraps it in a DataBundle.
        """
        try:
            self.logger.info(f"Ingesting CSV data from {file_path}")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File not found: {file_path}")
                
            df = pd.read_csv(file_path)
            
            metadata = {
                "source": source_name,
                "file_path": file_path,
                "ingestion_timestamp": datetime.datetime.now().isoformat(),
                "original_rows": len(df),
                "original_columns": list(df.columns),
                "reasoning": [f"Ingested {len(df)} rows from {file_path}"]
            }
            
            self.logger.info(f"Successfully ingested {len(df)} rows.")
            return DataBundle(data=df, metadata=metadata)
            
        except Exception as e:
            self.logger.error(f"Ingestion failed: {e}")
            raise e

def ingest_data(source_type: str, config: Dict[str, Any]) -> DataBundle:
    """
    Factory function/entry point for ingestion as per blueprint.
    """
    ingestor = FileIngestion()
    if source_type == "csv":
        return ingestor.ingest_csv(config["file_path"])
    else:
        raise NotImplementedError(f"Source type '{source_type}' not supported in Phase-1.")

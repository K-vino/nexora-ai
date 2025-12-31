import pandas as pd
import numpy as np
from typing import Dict, Any
from utils.data_types import DataBundle
from utils.logging import Logger

class SchemaValidator:
    """
    Validates data schema and quality.
    """
    def __init__(self):
        self.logger = Logger.get_logger("SchemaValidator")

    def validate(self, bundle: DataBundle) -> DataBundle:
        """
        Performs data quality checks and updates the bundle's quality_report.
        """
        df = bundle.data
        self.logger.info("Starting data validation...")
        
        # 1. Missing Values
        missing_counts = df.isnull().sum()
        missing_pct = (missing_counts / len(df)) * 100
        
        # 2. Schema (Column Types)
        schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
        
        # 3. Outlier Detection (Interquartile Range Rule for Numerics)
        outlier_counts = {}
        for col in df.select_dtypes(include=[np.number]).columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            count = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
            outlier_counts[col] = int(count)
            
        # 4. Overall Health Score (Simple heuristic)
        # Penalize for missing data and high outlier count
        total_cells = df.size
        total_missing = missing_counts.sum()
        missing_penalty = (total_missing / total_cells) 
        
        # Determine score (starts at 1.0, reduce by missing %)
        health_score = max(0.0, 1.0 - missing_penalty)
        
        quality_report = {
            "missing_values": missing_counts.to_dict(),
            "missing_percentage": missing_pct.to_dict(),
            "outliers": outlier_counts,
            "schema": schema,
            "health_score": round(health_score, 2),
            "rows": len(df),
            "columns": len(df.columns)
        }
        
        bundle.quality_report = quality_report
        bundle.metadata["reasoning"].append(f"Validation complete. Health Score: {health_score:.2f}")
        self.logger.info(f"Validation complete. Health Score: {health_score:.2f}")
        
        return bundle

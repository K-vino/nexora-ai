import pandas as pd
from typing import Optional, List
from nexora.validation.validator_interface import DataValidator
from nexora.core.exceptions import ValidationError
from nexora.core.logger import Logger
from nexora.core.config import Config

class SchemaValidator(DataValidator):
    """
    Validates dataframe schema: required columns, empty checks, and null thresholds.
    """
    
    def __init__(self, required_columns: Optional[List[str]] = None):
        self.logger = Logger.get_logger("SchemaValidator")
        self.required_columns = required_columns or []

    def validate(self, df: pd.DataFrame) -> bool:
        self.logger.info("Starting schema validation...")
        
        # 1. Empty Check
        if df.empty:
            self.logger.error("DataFrame is empty.")
            raise ValidationError("DataFrame is empty.")
            
        # 2. Required Columns Check
        if self.required_columns:
            missing = [col for col in self.required_columns if col not in df.columns]
            if missing:
                self.logger.error(f"Missing required columns: {missing}")
                raise ValidationError(f"Missing required columns: {missing}")

        # 3. Null Percentage Check (Soft check, warns but doesn't necessarily fail unless critical)
        null_pct = df.isnull().mean()
        high_null_cols = null_pct[null_pct > Config.MAX_NULL_PERCENTAGE].index.tolist()
        if high_null_cols:
            self.logger.warning(f"Columns with high null percentage (> {Config.MAX_NULL_PERCENTAGE:.0%}): {high_null_cols}")
            
        self.logger.info("Schema validation passed.")
        return True

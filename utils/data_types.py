from dataclasses import dataclass
from typing import Optional, Dict, Any
import pandas as pd

@dataclass
class DataBundle:
    """
    Standard data contract for passing data between Nexora AI modules.
    
    Attributes:
        data: The current state of the dataset (DataFrame).
        metadata: Dictionary containing metadata about the data (source, history, reasoning).
        quality_report: Dictionary containing data quality metrics and health scores.
        features: DataFrame containing processed features ready for modeling (optional until preprocessing).
        eda_insights: Dictionary containing exploratory data analysis findings (optional until EDA).
    """
    data: pd.DataFrame
    metadata: Dict[str, Any]
    quality_report: Optional[Dict[str, Any]] = None
    features: Optional[pd.DataFrame] = None
    eda_insights: Optional[Dict[str, Any]] = None

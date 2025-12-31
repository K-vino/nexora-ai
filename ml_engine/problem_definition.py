from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from utils.logging import Logger
from utils.data_types import DataBundle

@dataclass
class ProblemDefinition:
    task_type: str # "regression" or "classification"
    target: str
    features_used: List[str]
    excluded_features: List[str]
    reason: str

class ProblemDefiner:
    """
    Analyzes the DataBundle and defines the ML problem.
    """
    def __init__(self):
        self.logger = Logger.get_logger("ProblemDefiner")

    def define_problem(self, bundle: DataBundle, target_col: Optional[str] = None) -> ProblemDefinition:
        """
        Determines the target, task type, and feature set.
        """
        df = bundle.features if bundle.features is not None else bundle.data
        
        # 1. Identify Target
        # In a real system, this might be config-driven. 
        # For Phase-2/Housing, we default to 'median_house_value' if present, or user input.
        if target_col is None:
            # Heuristic: Determine target (usually last column or specified)
            # For housing.csv, it's 'median_house_value'
            if "median_house_value" in df.columns:
                target_col = "median_house_value"
            else:
                target_col = df.columns[-1]
        
        self.logger.info(f"Target variable identified: {target_col}")
        
        # 2. Determine Task Type
        import pandas as pd
        if pd.api.types.is_numeric_dtype(df[target_col]):
            # Check unique count. If low, might be classification. 
            # Housing prices -> Regression.
            unique_count = df[target_col].nunique()
            if unique_count < 20: 
                task_type = "classification"
            else:
                task_type = "regression"
        else:
            task_type = "classification"
            
        self.logger.info(f"Task type determined: {task_type}")

        # 3. Feature Selection
        all_cols = df.columns.tolist()
        features = [c for c in all_cols if c != target_col]
        excluded = []
        
        # Exclude features based on EDA risks (e.g. Multicollinearity)
        # Using Phase-1 EDA insights if available
        if bundle.eda_insights and "correlations" in bundle.eda_insights:
             # Basic logic: If A vs B > 0.95, drop one.
             pass # Logic placeholder. For now, keep clear.
        
        reason = f"Selected {len(features)} features for {task_type} on {target_col}."
        
        return ProblemDefinition(
            task_type=task_type,
            target=target_col,
            features_used=features,
            excluded_features=excluded,
            reason=reason
        )

import pandas as pd
from typing import Tuple, Dict, Any
from sklearn.model_selection import train_test_split # type: ignore
from utils.logging import Logger
from utils.data_types import DataBundle
from ml_engine.problem_definition import ProblemDefinition

class DataSplitter:
    """
    Splits data into training and testing sets properly.
    """
    def __init__(self):
        self.logger = Logger.get_logger("DataSplitter")

    def split(self, bundle: DataBundle, problem: ProblemDefinition, test_size: float = 0.2, random_state: int = 42) -> Dict[str, Any]:
        """
        Returns a dictionary with X_train, X_test, y_train, y_test.
        """
        df = bundle.features if bundle.features is not None else bundle.data
        
        X = df[problem.features_used]
        y = df[problem.target]
        
        self.logger.info(f"Splitting data: {len(df)} rows. Test size: {test_size}")
        
        stratify = None
        if problem.task_type == "classification":
            stratify = y
            
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state,
            stratify=stratify
        )
        
        self.logger.info(f"Split complete. Train shape: {X_train.shape}, Test shape: {X_test.shape}")
        
        return {
            "X_train": X_train,
            "X_test": X_test,
            "y_train": y_train,
            "y_test": y_test
        }

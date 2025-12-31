from typing import Dict, Any, Optional
from dl_engine.ann_models import ANNRegressor
from dl_engine.lstm_models import LSTMModel
from utils.logging import Logger
import numpy as np

class DLTrainer:
    """
    Trains and evaluates Deep Learning models.
    """
    def __init__(self):
        self.logger = Logger.get_logger("DLTrainer")
        self.results: Dict[str, Any] = {}
        
    def train_and_evaluate(self, X_train, y_train, X_test, y_test, X_val, y_val, task_type: str) -> Dict[str, Any]:
        
        self.logger.info("Starting DL training phase...")
        
        # 1. Train ANN (Mandatory)
        ann = ANNRegressor()
        
        # Ensure inputs are numpy arrays/compatible
        X_train_np = np.array(X_train).astype('float32')
        y_train_np = np.array(y_train).astype('float32')
        X_val_np = np.array(X_val).astype('float32')
        y_val_np = np.array(y_val).astype('float32')
        X_test_np = np.array(X_test).astype('float32')
        y_test_np = np.array(y_test).astype('float32')

        ann.train(X_train_np, y_train_np, X_val_np, y_val_np)
        ann_metrics = ann.evaluate(X_test_np, y_test_np)
        
        self.results["ANN"] = ann_metrics
        
        # 2. Train LSTM (Conditional)
        lstm = LSTMModel()
        if LSTMModel.is_suitable({}): # passing empty meta for now
            lstm.train(X_train_np, y_train_np, X_val_np, y_val_np)
            lstm_metrics = lstm.evaluate(X_test_np, y_test_np)
            self.results["LSTM"] = lstm_metrics
        else:
            self.logger.info("LSTM skipped (Not suitable for this data).")
            self.results["LSTM"] = None
            
        return self.results

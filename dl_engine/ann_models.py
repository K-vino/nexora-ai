from dl_engine.base_dl_model import BaseDLModel
from sklearn.neural_network import MLPRegressor # type: ignore
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score # type: ignore
import numpy as np
from typing import Dict, Any, Tuple
from utils.logging import Logger

class ANNRegressor(BaseDLModel):
    """
    Standard Feed-Forward Neural Network for Regression (MLP).
    Uses scikit-learn's MLPRegressor for robust, dependency-free ANN implementation.
    """
    def __init__(self):
        self.model = None
        self.history = None
        self.logger = Logger.get_logger("ANNRegressor")
        
    def build(self, input_shape: Tuple[int, ...]):
        self.logger.info(f"Building ANN (MLP) with input shape: {input_shape}")
        # Mimicking the Keras architecture: 64 -> 32 -> 1
        self.model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            max_iter=200,
            early_stopping=True,
            validation_fraction=0.2,
            random_state=42,
            verbose=False
        )
        
    def train(self, X_train: np.ndarray, y_train: np.ndarray, X_val: np.ndarray, y_val: np.ndarray) -> Dict[str, Any]:
        if self.model is None:
            self.build(X_train.shape)
            
        self.logger.info("Starting ANN (MLP) training...")
        
        # MLPRegressor handles validation internally if early_stopping=True
        # But we can also manually fit. Here we trust sklearn's internal split or just feed train.
        # To match the interface strictness, we'll feed X_train. 
        # Note: sklearn's early stopping splits X_train again. 
        # We will fit on X_train.
        
        self.model.fit(X_train, y_train.ravel())
        
        self.logger.info(f"Training complete. Iterations: {self.model.n_iter_}")
        
        # Loss curve
        loss_curve = self.model.loss_curve_
        val_score = self.model.best_validation_score_ if hasattr(self.model, 'best_validation_score_') else None
        
        return {
            "loss": loss_curve,
            "val_loss": [1 - val_score] if val_score else [] # Approximation
        }

    def predict(self, X: np.ndarray) -> np.ndarray:
        return self.model.predict(X).flatten()

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, float]:
        preds = self.predict(X_test)
        
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)
        
        metrics = {
            "RMSE": round(rmse, 4),
            "MAE": round(mae, 4),
            "R2": round(r2, 4)
        }
        self.logger.info(f"ANN Evaluation: {metrics}")
        return metrics

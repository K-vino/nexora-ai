from typing import Dict, Any
from utils.logging import Logger

class ComparativeAnalysis:
    """
    Compares Classical ML vs Deep Learning performance.
    """
    def __init__(self):
        self.logger = Logger.get_logger("ComparativeAnalysis")
        
    def compare(self, ml_results: Dict[str, Any], dl_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Determines the winner based on R2 (Regression) or F1 (Classification).
        """
        self.logger.info("Comparing ML vs DL...")
        
        # Get Best ML Score
        ml_best_model = ml_results.get("best_model")
        ml_best_metrics = ml_results["all_results"][ml_best_model]["metrics"]
        
        # Assuming Regression (R2) for now based on Housing Data
        ml_score = ml_best_metrics.get("R2", -float('inf'))
        
        # Get Best DL Score (ANN)
        ann_metrics = dl_results.get("ANN", {})
        dl_score = ann_metrics.get("R2", -float('inf'))
        
        # Decision Logic
        # DL must beat ML by a margin to be worth the compute cost (e.g. 1%)
        margin = 0.01 
        
        if dl_score > (ml_score + margin):
            decision = "Deep Learning (ANN)"
            reason = f"ANN outperformed {ml_best_model} by >1% margin (R2: {dl_score:.4f} vs {ml_score:.4f})."
        else:
            decision = f"Classical ML ({ml_best_model})"
            reason = f"Deep Learning (R2: {dl_score:.4f}) did not significantly outperform ML (R2: {ml_score:.4f}). Simpler model preferred."
            
        result = {
            "ml_best_r2": ml_score,
            "ann_r2": dl_score,
            "lstm_r2": None,
            "final_decision": decision,
            "reason": reason
        }
        
        self.logger.info(f"Final Decision: {decision}")
        return result

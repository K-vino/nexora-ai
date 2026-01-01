from typing import Dict, Any
from utils.logging import Logger

class ChatAssistant:
    """
    Scoped AI Assistant for answering pre-defined questions.
    """
    def __init__(self):
        self.logger = Logger.get_logger("ChatAssistant")
        self.knowledge_base = {
            "why_linear_regression": "Linear Regression provided the highest R2 score with minimal complexity, ensuring interpretability.",
            "risks": "Main risk is potential overfitting if feature count increases relative to row count. Currently balanced.",
            "deep_learning": "Deep Learning was evaluated but did not yield a statistically significant improvement (>1%) over Classical ML."
        }
        
    def ask(self, question_id: str) -> str:
        """
        Retrieves grounded answer.
        """
        self.logger.info(f"User asked: {question_id}")
        return self.knowledge_base.get(question_id, "This question is out of scope for the current analysis context.")

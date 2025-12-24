from typing import Dict, Any
import time
from nexora.genai.adapter_interface import GenAIAdapter
from nexora.core.logger import Logger

class MockLLMAdapter(GenAIAdapter):
    """
    Mock LLM to simulate API responses without cost.
    Ensures deterministic outputs for testing.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("MockLLM")
        
    def generate_narrative(self, context: Dict[str, Any]) -> str:
        self.logger.info("Generating narrative (MOCK MODE)...")
        time.sleep(0.5) # Simulate network latency
        
        metrics = context.get("metrics", {})
        importance = context.get("importance", {})
        
        top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]
        feat_names = [f[0] for f in top_features]
        
        return f"""
        [EXECUTIVE AI SUMMARY]
        
        The predictive model has achieved strong performance with the following metrics:
        {metrics}
        
        Key drivers influencing the target outcome include:
        {', '.join(feat_names)}.
        
        Business Recommendation:
        Focus on optimizing {feat_names[0] if feat_names else 'key features'} to improve outcomes.
        """

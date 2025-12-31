from typing import Dict, Any

class PromptBuilder:
    """Helper to construct context-aware prompts."""
    
    @staticmethod
    def build_analysis_prompt(metrics: Dict[str, float], importance: Dict[str, float]) -> str:
        top_features = sorted(importance.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return f"""
        Analyze the following model results:
        - Metrics: {metrics}
        - Top Drivers: {top_features}
        
        Provide a concise executive summary.
        """

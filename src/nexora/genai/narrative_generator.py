from typing import Dict, Any, Optional
from nexora.genai.adapter_interface import GenAIAdapter
from nexora.genai.prompt_builder import PromptBuilder
from nexora.core.logger import Logger

class NarrativeGenerator:
    """
    Orchestrates the generation of AI narratives.
    """
    
    def __init__(self, llm_adapter: GenAIAdapter):
        self.logger = Logger.get_logger("NarrativeGenerator")
        self.llm = llm_adapter
        
    def generate_report_narrative(self, 
                                metrics: Dict[str, float], 
                                importance: Dict[str, float],
                                anomalies: Optional[Dict[str, Any]] = None) -> str:
        """
        Generates a comprehensive narrative for the analysis.
        """
        self.logger.info("Generating analysis narrative...")
        
        # Build Context
        context_str = f"Metrics: {metrics}\nFeature Importance: {importance}\n"
        if anomalies:
            context_str += f"Anomalies: {anomalies}\n"
            
        # Here we could use PromptBuilder, but for robustness we construct it here or extend PromptBuilder
        prompt = f"""
        You are an expert Data Scientist. Analyze the following results from a machine learning pipeline:
        
        {context_str}
        
        1. Summarize model performance (Good/Bad?).
        2. Identify key drivers (features).
        3. Mention data quality issues if any anomalies exists.
        4. Provide a clear business recommendation.
        
        Keep it professional, concise, and business-friendly.
        """
        
        # Call LLM
        return self.llm.generate_narrative({"prompt": prompt, "metrics": metrics, "importance": importance})

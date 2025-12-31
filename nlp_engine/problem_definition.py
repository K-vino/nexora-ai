from dataclasses import dataclass
from typing import Dict, Any
from utils.logging import Logger

@dataclass
class NLPProblemDefinition:
    nlp_task: str
    text_source: str
    goal: str

class NLPProblemDefiner:
    """
    Defines the NLP task context.
    """
    def __init__(self):
        self.logger = Logger.get_logger("NLPProblemDefiner")
        
    def define_problem(self, metadata: Dict[str, Any]) -> NLPProblemDefinition:
        """
        Defines what the NLP engine should do.
        """
        # In a real system, this would be dynamic.
        # Here we fix it to Document Clustering/Similiarity for Housing.
        
        problem = NLPProblemDefinition(
            nlp_task="document_similarity_and_extraction",
            text_source="real_estate_descriptions.csv",
            goal="Identify themes and similar property listings."
        )
        
        self.logger.info(f"NLP Problem Defined: {problem}")
        return problem

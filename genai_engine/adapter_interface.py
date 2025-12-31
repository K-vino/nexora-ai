from abc import ABC, abstractmethod
from typing import Dict, Any

class GenAIAdapter(ABC):
    """Interface for GenAI interactions."""
    
    @abstractmethod
    def generate_narrative(self, context: Dict[str, Any]) -> str:
        """Create a text narrative from data context."""
        pass

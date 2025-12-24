from abc import ABC, abstractmethod
from typing import Any, Dict

class ReportGenerator(ABC):
    """
    Abstract Base Class for Report Generation.
    Responsibile for formatting analysis results into consumable documents.
    """

    @abstractmethod
    def generate_report(self, data: Dict[str, Any], output_path: str) -> str:
        """
        Creates a report from the provided data.
        
        Args:
            data (Dict[str, Any]): The content to include (metrics, plots, narratives).
            output_path (str): Where to save the report.
            
        Returns:
            str: The absolute path to the generated report.
        """
        pass

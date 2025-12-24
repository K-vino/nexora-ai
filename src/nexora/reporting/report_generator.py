import json
from pathlib import Path
from typing import Dict, Any
from nexora.core.config import Config
from nexora.core.logger import Logger

class ReportGenerator:
    """
    Generates artifacts from the analysis pipeline.
    """
    
    def __init__(self):
        self.logger = Logger.get_logger("ReportGenerator")
        
    def save_report(self, run_id: str, data: Dict[str, Any]):
        """Saves analysis results to a JSON file in artifacts."""
        try:
            filename = f"report_{run_id}.json"
            output_path = Config.ARTIFACTS_PATH / filename
            
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=4)
                
            self.logger.info(f"Report saved to {output_path}")
            return output_path
        except Exception as e:
            self.logger.error(f"Failed to save report: {e}")

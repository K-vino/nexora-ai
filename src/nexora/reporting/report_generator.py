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

    def generate_html_report(self, run_id: str, data: Dict[str, Any]):
        """Generates a human-readable HTML report."""
        try:
            from jinja2 import Template
            import datetime
            
            template_path = Path(__file__).parent / "report_template.html"
            
            if not template_path.exists():
                self.logger.warning("HTML template not found. Skipping HTML report.")
                return None
                
            with open(template_path, 'r') as f:
                template_str = f.read()
                
            template = Template(template_str)
            
            # Add timestamp if not present
            if "timestamp" not in data:
                data["timestamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
            html_content = template.render(**data)
            
            filename = f"report_{run_id}.html"
            output_path = Config.ARTIFACTS_PATH / filename
            
            with open(output_path, 'w') as f:
                f.write(html_content)
                
            self.logger.info(f"HTML Report saved to {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Failed to generate HTML report: {e}")
            return None

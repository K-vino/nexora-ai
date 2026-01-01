import os
from datetime import datetime
from utils.logging import Logger

class ReportWriter:
    """
    Writes the final NEXORA AI Intelligence Report to disk.
    """
    def __init__(self, output_dir="reports"):
        self.logger = Logger.get_logger("ReportWriter")
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def save_report(self, content: str, report_type="analysis"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"nexora_{report_type}_{timestamp}.txt"
        path = os.path.join(self.output_dir, filename)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
            
        self.logger.info(f"Report saved to: {path}")
        return path

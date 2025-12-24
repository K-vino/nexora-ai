from pydantic import BaseModel
from typing import Dict, Any, Literal

class PipelineRequest(BaseModel):
    source_path: str
    target_column: str
    task: Literal["regression", "classification"]
    algorithm: Literal["rf", "linear", "logistic"] = "rf"

class PipelineResponse(BaseModel):
    run_id: str
    status: str
    metrics: Dict[str, float]
    narrative: str
    report_path: str

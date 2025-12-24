from fastapi import APIRouter, HTTPException, BackgroundTasks
from nexora.web.schemas import PipelineRequest, PipelineResponse
from nexora.orchestration.pipeline import NexoraPipeline
from nexora.core.exceptions import NexoraError
import logging

router = APIRouter()
logger = logging.getLogger("API")

@router.post("/run", response_model=PipelineResponse)
async def run_pipeline(request: PipelineRequest):
    """
    Executes the Nexora AI pipeline synchronously.
    Real-world app would use BackgroundTasks or Celery.
    """
    logger.info(f"Received pipeline request: {request}")
    
    pipeline = NexoraPipeline()
    
    try:
        # Delegate to the core engine
        result = pipeline.run(
            source=request.source_path,
            target=request.target_column,
            task=request.task,
            algo=request.algorithm
        )
        
        return PipelineResponse(
            run_id=result["run_id"],
            status=result["status"],
            metrics=result["metrics"],
            narrative=result["narrative"],
            report_path=result["report_path"]
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NexoraError as e:
        raise HTTPException(status_code=400, detail=f"Pipeline Error: {str(e)}")
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Execution Error")

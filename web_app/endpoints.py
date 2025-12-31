from fastapi import APIRouter, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.responses import FileResponse
from web_app.schemas import PipelineRequest, PipelineResponse
from nexora.orchestration.pipeline import NexoraPipeline
from utils.config import Config
from utils.exceptions import NexoraError
import logging
import shutil
import pandas as pd
from pathlib import Path

router = APIRouter()
logger = logging.getLogger("API")

@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    """
    Uploads a dataset and returns its path and columns.
    """
    try:
        # Save file to raw data directory
        file_location = Config.RAW_DATA_PATH / file.filename
        file_location.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Read columns for UI dropdown
        df = pd.read_csv(file_location, nrows=5)
        columns = df.columns.tolist()
        
        return {
            "filename": file.filename,
            "path": str(file_location.absolute()),
            "columns": columns
        }
    except Exception as e:
        logger.error(f"Upload failed: {e}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

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
            report_path=result["report_path"],
            html_report_path=result.get("html_report_path")
        )
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NexoraError as e:
        raise HTTPException(status_code=400, detail=f"Pipeline Error: {str(e)}")
    except Exception as e:
        logger.error(f"Internal Server Error: {e}")
        raise HTTPException(status_code=500, detail="Internal Execution Error")

@router.get("/artifacts/{filename}")
async def get_artifact(filename: str):
    """
    Serves generated artifacts (HTML reports, JSON, images).
    """
    file_path = Config.ARTIFACTS_PATH / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Artifact not found")
        
    return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')

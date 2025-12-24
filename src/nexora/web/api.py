from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from nexora.web.endpoints import router as api_router
import os

from nexora.core.config import Config

app = FastAPI(title="Nexora AI Web Adapter", version="1.0")

# Mount static files
static_dir = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Mount artifacts
app.mount("/api/artifacts", StaticFiles(directory=str(Config.ARTIFACTS_PATH)), name="artifacts")

# Templates
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

# Register API routes
app.include_router(api_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Renders the main UI."""
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from notebooklm import NotebookLMClient
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notebooklm-bridge")

app = FastAPI(title="NotebookLM Remote Bridge v2")

# --- Security ---
API_KEY = os.environ.get("BRIDGE_API_KEY", "your-secret-key-here")
api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

async def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
    return api_key

# --- Client Management (Singleton-ish) ---
_cached_client = None

async def get_client():
    global _cached_client
    if _cached_client is None:
        logger.info("Initializing new NotebookLMClient and fetching tokens...")
        _cached_client = await NotebookLMClient.from_storage()
    return _cached_client

# --- Models ---
class AskRequest(BaseModel):
    notebook_id: str
    query: str

class GenerateRequest(BaseModel):
    notebook_id: str
    artifact_type: str
    instructions: str = ""

# --- Endpoints ---

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "api_key_required": API_KEY != "your-secret-key-here"}

@app.post("/ask", dependencies=[Depends(get_api_key)])
async def ask_notebook(req: AskRequest):
    try:
        client = await get_client()
        result = await client.chat.ask(req.notebook_id, req.query)
        return {
            "answer": result.answer,
            "references": [
                {"source_id": r.source_id, "text": r.cited_text} 
                for r in result.references
            ]
        }
    except Exception as e:
        logger.error(f"Error in /ask: {e}")
        # If auth error, clear cache so it retries on next call
        if "Authentication" in str(e):
            global _cached_client
            _cached_client = None
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate", dependencies=[Depends(get_api_key)])
async def generate_artifact(req: GenerateRequest):
    try:
        client = await get_client()
        # Mapping artifact types to client methods
        method_map = {
            "audio": client.artifacts.generate_audio,
            "video": client.artifacts.generate_video,
            "quiz": client.artifacts.generate_quiz,
            "slides": client.artifacts.generate_slide_deck,
        }
        
        if req.artifact_type not in method_map:
            raise HTTPException(status_code=400, detail=f"Unsupported artifact type: {req.artifact_type}")
            
        status = await method_map[req.artifact_type](req.notebook_id, instructions=req.instructions)
        return {"task_id": status.task_id, "status": "started"}
    except Exception as e:
        logger.error(f"Error in /generate: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # Important: Setting reload=False when using singleton-ish client
    uvicorn.run(app, host="0.0.0.0", port=8000)

from fastapi import FastAPI, Request, Body
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Dict, Any, Optional
from services.service import notion_service
from models.model import CreateNotionPageRequest, YouTubeTranscriptRequest

app = FastAPI()

@app.get("/notion/oauth/start")
async def notion_oauth_start(request: Request):
    auth_url = notion_service.generate_oauth_url(request)
    return RedirectResponse(url=auth_url)

@app.get("/notion/oauth/callback")
async def notion_oauth_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code:
        return JSONResponse({"error": "Missing authorization code"}, status_code=400)
    
    state_params = notion_service.decode_state_params(state) if state else {}
    
    success, result = await notion_service.exchange_code_for_token(code)
    
    if success:
        return JSONResponse(result)
    else:
        status_code = 400 if "OAuth token exchange failed" in result.get("error", "") else 500
        return JSONResponse(result, status_code=status_code)

@app.post("/notion/pages/create")
async def create_notion_page(request: CreateNotionPageRequest):
    success, result, status_code = await notion_service.create_page(
        request=request
    )
    
    return JSONResponse(result, status_code=status_code)

@app.post("/youtube/transcript")
async def process_youtube_transcript(request: YouTubeTranscriptRequest):
    try:
        result = await notion_service.process_youtube_transcript(request)
        return JSONResponse(result)
            
    except Exception as e:
        return JSONResponse({
            "success": False,
            "error": "Transcript processing failed",
            "details": {"exception": str(e)}
        }, status_code=500)



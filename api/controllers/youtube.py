from fastapi.responses import JSONResponse
from models.model import YouTubeTranscriptRequest
from services.service import notion_service
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

class YouTubeController:
    def __init__(self):
        self.notion_service = notion_service
    
    async def process_youtube_transcript(self, request: YouTubeTranscriptRequest):
        """Handle YouTube transcript processing"""
        try:
            result = await self.notion_service.process_youtube_transcript(request)
            return JSONResponse(result)
                
        except Exception as e:
            return JSONResponse({
                "success": False,
                "error": "Transcript processing failed",
                "details": {"exception": str(e)}
            }, status_code=500)


# Create an instance to be used by routers
youtube_controller = YouTubeController()
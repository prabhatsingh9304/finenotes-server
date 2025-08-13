from fastapi import APIRouter
from controllers.youtube import youtube_controller
from models.model import YouTubeTranscriptRequest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


# YouTube routes
router = APIRouter(prefix="/youtube", tags=["youtube"])

@router.post("/transcript")
async def process_youtube_transcript(request: YouTubeTranscriptRequest):
    return await youtube_controller.process_youtube_transcript(request)

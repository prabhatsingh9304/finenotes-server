from pydantic import BaseModel
from typing import Dict, Any, Optional, List

class CreateNotionPageRequest(BaseModel):
    access_token: str
    parent: Dict[str, Any] 
    properties: Dict[str, Any]
    children: Optional[List[Dict[str, Any]]] = None
    icon: Optional[Dict[str, Any]] = None
    cover: Optional[Dict[str, Any]] = None


class YouTubeTranscriptRequest(BaseModel):
    video_url: Optional[str] = None
    video_id: Optional[str] = None
    transcript: Optional[str] = None


class NotionOAuthResponse(BaseModel):
    success: bool = True
    access_token: Optional[str] = None
    token_type: Optional[str] = None
    bot_id: Optional[str] = None
    workspace_name: Optional[str] = None
    workspace_icon: Optional[str] = None
    workspace_id: Optional[str] = None
    owner: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class CreateNotionPageResponse(BaseModel):
    success: bool = True
    page_id: Optional[str] = None
    url: Optional[str] = None
    created_time: Optional[str] = None
    properties: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class TranscriptSegment(BaseModel):
    start_time: int
    end_time: Optional[int] = None
    text: str
    timestamp: str


class YouTubeTranscriptResponse(BaseModel):
    success: bool = True
    segments_processed: Optional[int] = None
    error: Optional[str] = None
    details: Optional[Dict[str, Any]] = None

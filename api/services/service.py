import httpx
import os
import sys
import base64
from typing import Dict, Any, Optional, Tuple
from fastapi import Request
from dotenv import load_dotenv
from models.model import YouTubeTranscriptRequest, CreateNotionPageRequest

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
from utils.transcript import TranscriptParser
load_dotenv()

class NotionService:
    def __init__(self):
        self.client_id = os.getenv("NOTION_CLIENT_ID")
        self.client_secret = os.getenv("NOTION_CLIENT_SECRET")
        self.redirect_uri = os.getenv("NOTION_REDIRECT_URI")
    
    def generate_oauth_url(self, request: Request) -> str:
        state_params = {}
        for key, value in request.query_params.items():
            state_params[key] = value
        
        state = base64.urlsafe_b64encode(str(state_params).encode()).decode()
        
        auth_url = f"https://api.notion.com/v1/oauth/authorize?client_id={self.client_id}&response_type=code&owner=user&redirect_uri={self.redirect_uri}&state={state}"
        
        return auth_url
    
    def decode_state_params(self, state: str) -> Dict[str, str]:
        state_params = {}
        if state:
            try:
                decoded_state = base64.urlsafe_b64decode(state.encode()).decode()
                cleaned_state = decoded_state.strip("{}").replace("'", "\"")
                for item in cleaned_state.split(", "):
                    if ": " in item:
                        k, v = item.split(": ", 1)
                        state_params[k.strip("'")] = v.strip("'")
            except Exception:
                pass
        return state_params
    
    async def exchange_code_for_token(self, code: str) -> Tuple[bool, Dict[str, Any]]:
        async with httpx.AsyncClient() as client:
            try:
                credentials = f"{self.client_id}:{self.client_secret}"
                base64_credentials = base64.b64encode(credentials.encode()).decode()
                
                response = await client.post(
                    "https://api.notion.com/v1/oauth/token",
                    json={
                        "grant_type": "authorization_code",
                        "code": code,
                        "redirect_uri": self.redirect_uri,
                    },
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Basic {base64_credentials}"
                    }
                )

                token_data = response.json()

                if "access_token" not in token_data:
                    return False, {"error": "OAuth token exchange failed", "details": token_data}
                
                return True, token_data

            except Exception as e:
                return False, {"error": "Token exchange failed", "exception": str(e)}
    
    async def create_page(
        self,
        request: CreateNotionPageRequest
    ) -> Tuple[bool, Dict[str, Any], int]:
        async with httpx.AsyncClient() as client:
            try:
                request_body = {
                    "parent": request.parent,
                    "properties": request.properties
                }
                
                if request.children is not None:
                    request_body["children"] = request.children
                if request.icon is not None:
                    request_body["icon"] = request.icon
                if request.cover is not None:
                    request_body["cover"] = request.cover
                
                response = await client.post(
                    "https://api.notion.com/v1/pages",
                    json=request_body,
                    headers={
                        "Authorization": f"Bearer {request.access_token}",
                        "Notion-Version": "2022-06-28",
                        "Content-Type": "application/json"
                    }
                )
                
                return True, response.json(), response.status_code
                
            except Exception as e:
                return False, {"error": "Failed to create page", "exception": str(e)}, 500

    async def process_youtube_transcript(self, request: YouTubeTranscriptRequest) -> Dict[str, Any]:
        if request.transcript:
            try:
                parser = TranscriptParser(request.transcript)
                interval_map = parser.parse_transcript_to_map()
            except Exception as e:
                return {
                    "success": False,
                    "error": "Failed to parse transcript",
                    "exception": str(e)
                }
            
            return {
                "success": True,
                "segments_processed": len(interval_map)
            }
        else:
            return {
                "success": False,
                "error": "Either transcript, video_url, or video_id must be provided"
            }


# Create a singleton instance for easy importing
notion_service = NotionService()

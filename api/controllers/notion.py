from fastapi import Request
from fastapi.responses import JSONResponse, RedirectResponse
from services.service import notion_service
from models.model import CreateNotionPageRequest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))


class NotionController:
    def __init__(self):
        self.notion_service = notion_service
    
    async def oauth_start(self, request: Request):
        """Handle OAuth start request"""
        auth_url = self.notion_service.generate_oauth_url(request)
        return RedirectResponse(url=auth_url)
    
    async def oauth_callback(self, request: Request):
        """Handle OAuth callback"""
        code = request.query_params.get("code")
        state = request.query_params.get("state")

        if not code:
            return JSONResponse({"error": "Missing authorization code"}, status_code=400)
        
        state_params = self.notion_service.decode_state_params(state) if state else {}
        
        success, result = await self.notion_service.exchange_code_for_token(code)
        
        if success:
            return JSONResponse(result)
        else:
            status_code = 400 if "OAuth token exchange failed" in result.get("error", "") else 500
            return JSONResponse(result, status_code=status_code)
    
    async def create_page(self, request: CreateNotionPageRequest):
        """Handle create notion page request"""
        success, result, status_code = await self.notion_service.create_page(
            request=request
        )
        
        return JSONResponse(result, status_code=status_code)
    

# Create an instance to be used by routers
notion_controller = NotionController()

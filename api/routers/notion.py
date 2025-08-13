from fastapi import APIRouter, Request
from controllers.notion import notion_controller
from models.model import CreateNotionPageRequest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

router = APIRouter(prefix="/notion", tags=["notion"])

@router.get("/oauth/start")
async def notion_oauth_start(request: Request):
    return await notion_controller.oauth_start(request)

@router.get("/oauth/callback")
async def notion_oauth_callback(request: Request):
    return await notion_controller.oauth_callback(request)

@router.post("/pages/create")
async def create_notion_page(request: CreateNotionPageRequest):
    return await notion_controller.create_page(request)


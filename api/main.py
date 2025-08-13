from fastapi import FastAPI
from routers.notion import router as notion_router
from routers.youtube import router as youtube_router

app = FastAPI()

app.include_router(notion_router)
app.include_router(youtube_router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "FineNotes Server API"}



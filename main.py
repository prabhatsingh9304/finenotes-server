#!/usr/bin/env python3
"""
FineNotes Server - Main Entry Point
"""

if __name__ == "__main__":
    import uvicorn
    from api.main import app
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 
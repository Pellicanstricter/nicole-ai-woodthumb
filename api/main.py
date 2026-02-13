"""
Nicole FastAPI Application
Main entry point for the API
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import os
from .config import settings
from .chat import router as chat_router
from .email import router as email_router
from .dashboard import router as dashboard_router

# Initialize FastAPI app
app = FastAPI(
    title="Nicole API",
    description="AI Customer Service Agent for Wood Thumb",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://woodthumb.com",
        "https://www.woodthumb.com",
        "https://nicole-ai-woodthumb-production.up.railway.app",
        "http://localhost:3000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router, prefix="/api", tags=["chat"])
app.include_router(email_router, prefix="/api", tags=["email"])
app.include_router(dashboard_router, tags=["dashboard"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Nicole",
        "version": "1.0.0",
        "status": "running",
        "environment": settings.environment
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint for monitoring"""
    return {
        "status": "healthy",
        "api_key_configured": bool(settings.anthropic_api_key),
        "environment": settings.environment
    }


@app.get("/api/knowledge")
async def knowledge_info():
    """Returns knowledge base metadata"""
    try:
        with open('knowledge/woodthumb.md', 'r') as f:
            content = f.read()
            word_count = len(content.split())

        return {
            "status": "loaded",
            "word_count": word_count,
            "last_updated": "2024-02-13"  # Update this when knowledge base changes
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"status": "error", "detail": str(e)}
        )


# Mount static files for widget and dashboard (if serving from same app)
if os.path.exists("widget"):
    app.mount("/widget", StaticFiles(directory="widget"), name="widget")

if os.path.exists("dashboard"):
    app.mount("/dashboard", StaticFiles(directory="dashboard", html=True), name="dashboard")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=(settings.environment == "development")
    )

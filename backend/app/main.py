import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from fastapi import FastAPI
from core.config import settings
from core.security import setup_cors
from api.api_v1 import api_router

# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Full-Stack AI Application with Groq Integration",
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc"  # Alternative documentation
)

# Setup CORS for frontend connection
setup_cors(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "AI FullStack API is running!",
        "docs": "/docs",
        "version": settings.app_version
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
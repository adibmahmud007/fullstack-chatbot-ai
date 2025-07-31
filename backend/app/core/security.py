from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
import os

def setup_cors(app: FastAPI) -> None:
    """
    CORS setup for production and development
    """
    # Production allowed origins
    allowed_origins = [
        settings.frontend_url,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000"
    ]
    
    # Add production domains
    if os.getenv("RENDER"):
        allowed_origins.extend([
            "https://*.onrender.com",
            "https://*.vercel.app",
            "https://*.netlify.app"
        ])
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
        expose_headers=["*"]
    )
    
    print(f"🔒 CORS configured for: {', '.join(allowed_origins[:3])}...")
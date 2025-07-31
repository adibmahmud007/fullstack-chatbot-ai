from fastapi import APIRouter
from core.config import settings

router = APIRouter()

@router.get("/")
def read_root():
    """
    Root endpoint - API health check
    """
    return {
        "message": f"Welcome to {settings.app_name}!",
        "version": settings.app_version,
        "status": "running"
    }

@router.get("/health")
def health_check():
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version
    }

@router.get("/greet/{name}")
def greet_user(name: str):
    """
    Personalized greeting endpoint
    """
    return {
        "greeting": f"Hello {name}! Welcome to our AI platform!",
        "app_name": settings.app_name
    }
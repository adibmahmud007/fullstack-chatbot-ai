from fastapi import APIRouter
from api.endpoints import basic, ai_chat

# Main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    basic.router, 
    tags=["Basic Endpoints"]
)

api_router.include_router(
    ai_chat.router,
    prefix="/ai",
    tags=["AI Chat"]
)
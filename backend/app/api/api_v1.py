from fastapi import APIRouter
from api.endpoints import basic, ai_chat, legal_advisor

# Main API router
api_router = APIRouter()

# Include basic endpoints
api_router.include_router(
    basic.router, 
    tags=["Basic Endpoints"]
)

# Include AI chat endpoints
api_router.include_router(
    ai_chat.router,
    prefix="/ai",
    tags=["AI Chat"]
)

# Include Bangladesh Legal Advisory endpoints
api_router.include_router(
    legal_advisor.router,
    prefix="/legal",
    tags=["🏛️ Bangladesh Legal Advisory"]
)
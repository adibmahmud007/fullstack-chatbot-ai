from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    """
    Request model for AI chat
    """
    message: str = Field(..., min_length=1, max_length=2000, description="User message")
    max_tokens: Optional[int] = Field(default=1000, ge=10, le=2000, description="Maximum response tokens")
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=1.0, description="Response creativity")

class ChatResponse(BaseModel):
    """
    Response model for AI chat
    """
    user_message: str
    ai_response: str
    model: str
    tokens_used: Optional[int] = None
    status: str

class ErrorResponse(BaseModel):
    """
    Error response model
    """
    message: str
    error_type: str
    status: str = "error"
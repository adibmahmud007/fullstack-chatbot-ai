from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse # pyright: ignore[reportMissingImports]
from models.schemas import ChatRequest, ChatResponse, ErrorResponse
from services.groq_service import groq_service
import json
import asyncio

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(request: ChatRequest):
    """
    Chat with AI - Get complete response at once
    """
    try:
        # Generate AI response
        result = await groq_service.generate_response(
            message=request.message,
            max_tokens=request.max_tokens
        )
        
        if result["status"] == "error":
            raise HTTPException(status_code=500, detail=result["error"])
        
        return ChatResponse(
            user_message=request.message,
            ai_response=result["response"],
            model=result["model"],
            tokens_used=result["tokens_used"],
            status="success"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate AI response: {str(e)}"
        )

@router.post("/chat/stream")
async def chat_with_ai_stream(request: ChatRequest):
    """
    Chat with AI - Get streaming response (typing effect)
    """
    async def generate_stream():
        try:
            async for chunk in groq_service.generate_streaming_response(request.message):
                # Format as Server-Sent Events
                yield f"data: {json.dumps({'chunk': chunk, 'status': 'streaming'})}\n\n"
            
            # Send completion signal
            yield f"data: {json.dumps({'chunk': '', 'status': 'completed'})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'error': str(e), 'status': 'error'})}\n\n"
    
    return StreamingResponse(
        generate_stream(),
        media_type="text/plain",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )

@router.get("/models")
async def get_available_models():
    """
    Get list of available AI models
    """
    return {
        "models": [
            {
                "id": "llama3-8b-8192",
                "name": "Llama 3 8B",
                "description": "Fast and efficient model",
                "max_tokens": 8192
            }
        ],
        "default_model": "llama3-8b-8192"
    }
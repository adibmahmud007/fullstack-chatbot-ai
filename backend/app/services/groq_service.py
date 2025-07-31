from groq import Groq
from core.config import settings
from typing import Optional, AsyncGenerator
import json

class GroqService:
    def __init__(self):
        """
        Initialize Groq client with API key from settings
        """
        if not settings.groq_api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=settings.groq_api_key)
        self.model = "llama3-8b-8192"  # Free fast model
    
    async def generate_response(self, message: str, max_tokens: int = 1000) -> dict:
        """
        Generate AI response from user message
        """
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant. Provide clear, concise, and helpful responses."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                model=self.model,
                max_tokens=max_tokens,
                temperature=0.7,  # Creativity level (0-1)
                stream=False  # Get complete response at once
            )
            
            # Extract response
            ai_response = chat_completion.choices[0].message.content
            
            return {
                "response": ai_response,
                "model": self.model,
                "tokens_used": chat_completion.usage.total_tokens,
                "status": "success"
            }
            
        except Exception as e:
            return {
                "response": "Sorry, I'm having trouble processing your request right now.",
                "error": str(e),
                "status": "error"
            }
    
    async def generate_streaming_response(self, message: str) -> AsyncGenerator[str, None]:
        """
        Generate streaming AI response (like ChatGPT typing effect)
        """
        try:
            # Call Groq API with streaming
            stream = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant."
                    },
                    {
                        "role": "user",
                        "content": message
                    }
                ],
                model=self.model,
                max_tokens=1000,
                temperature=0.7,
                stream=True  # Enable streaming
            )
            
            # Yield each chunk as it comes
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            yield f"Error: {str(e)}"

# Global service instance
groq_service = GroqService()
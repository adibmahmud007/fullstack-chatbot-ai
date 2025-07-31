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

# Create FastAPI application with production settings
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    🏛️ **Bangladesh Legal AI Assistant**
    
    একটি সম্পূর্ণ আইনি সহায়তা সিস্টেম যা বাংলাদেশের আইন অনুযায়ী পরামর্শ প্রদান করে।
    
    **Features:**
    - 🤖 AI-powered legal advice in Bengali & English
    - ⚖️ Bangladesh-specific legal knowledge  
    - 📋 Step-by-step legal procedures
    - 📞 Emergency legal contacts
    - 📚 Legal education and tips
    
    **Disclaimer:** এই সিস্টেম শুধুমাত্র তথ্যগত উদ্দেশ্যে। নির্দিষ্ট আইনি সমস্যার জন্য অভিজ্ঞ আইনজীবীর পরামর্শ নিন।
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "Bangladesh Legal AI",
        "url": "https://github.com/adibmahmud007/fullstack-chatbot-ai",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    }
)

# Setup CORS for production
setup_cors(app)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint with API information
@app.get("/")
def read_root():
    return {
        "message": "🏛️ Bangladesh Legal AI Assistant API",
        "version": settings.app_version,
        "status": "running",
        "documentation": "/docs",
        "features": [
            "AI Legal Advice",
            "Bangladesh Law Explanations", 
            "Legal Procedures",
            "Emergency Contacts",
            "Bilingual Support (Bengali + English)"
        ],
        "endpoints": {
            "legal_advice": "/api/v1/legal/legal-advice",
            "legal_categories": "/api/v1/legal/legal-categories",
            "emergency_contacts": "/api/v1/legal/emergency-contacts",
            "ai_chat": "/api/v1/ai/chat"
        }
    }

# Health check for production monitoring
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "environment": "production" if os.getenv("RENDER") else "development"
    }

# Production server setup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.host,
        port=settings.port,
        reload=False  # Production এ reload False
    )
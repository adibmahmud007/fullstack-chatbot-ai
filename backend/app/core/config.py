from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

# Get the directory where this config.py file is located
current_file = Path(__file__)
app_dir = current_file.parent.parent  # Go up to /app/ directory
backend_dir = app_dir.parent  # Go up to /backend/ directory
env_file_path = backend_dir / ".env"

class Settings(BaseSettings):
    # App Settings
    app_name: str = "Bangladesh Legal AI Assistant"
    app_version: str = "1.0.0"
    debug: bool = False  # Production এ False
    
    # API Keys
    groq_api_key: Optional[str] = None
    
    # CORS Settings - Production domains add করবো
    frontend_url: str = "http://localhost:3000"
    allowed_hosts: list = ["localhost", "127.0.0.1", "*.onrender.com", "*.vercel.app"]
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    # Production settings
    host: str = "0.0.0.0"
    port: int = int(os.getenv("PORT", 8000))
    
    class Config:
        env_file = str(env_file_path) if env_file_path.exists() else None
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Production environment check
        if os.getenv("RENDER"):
            print("🚀 Running in Render production environment")
            self.debug = False
            self.allowed_hosts.extend(["*.onrender.com"])
        else:
            # Debug information for local development
            print(f"🔍 Looking for .env file at: {env_file_path}")
            print(f"📁 .env file exists: {env_file_path.exists() if env_file_path else False}")
        
        # Validate critical settings
        if not self.groq_api_key:
            print("⚠️  WARNING: GROQ_API_KEY not found")
            if not os.getenv("RENDER"):
                print("💡 Please add your Groq API key to .env file to enable AI features")
        else:
            print(f"✅ GROQ_API_KEY loaded successfully")

# Global settings instance
settings = Settings()
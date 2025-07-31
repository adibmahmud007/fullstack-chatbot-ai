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
    app_name: str = "AI FullStack Project"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # API Keys
    groq_api_key: Optional[str] = None
    
    # CORS Settings
    frontend_url: str = "http://localhost:3000"
    allowed_hosts: list = ["localhost", "127.0.0.1"]
    
    # Database
    database_url: str = "sqlite:///./app.db"
    
    class Config:
        env_file = str(env_file_path)
        case_sensitive = False
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Debug information
        print(f"🔍 Looking for .env file at: {env_file_path}")
        print(f"📁 .env file exists: {env_file_path.exists()}")
        
        # Validate critical settings
        if not self.groq_api_key:
            print("⚠️  WARNING: GROQ_API_KEY not found in .env file")
            print("💡 Please add your Groq API key to .env file to enable AI features")
        else:
            print(f"✅ GROQ_API_KEY loaded successfully (ends with: ...{self.groq_api_key[-4:]})")

# Global settings instance
settings = Settings()
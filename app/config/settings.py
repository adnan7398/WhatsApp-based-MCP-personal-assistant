import os
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # WhatsApp Business API Configuration
    whatsapp_access_token: str = os.getenv("WHATSAPP_ACCESS_TOKEN", "")
    whatsapp_phone_number_id: str = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")
    whatsapp_verify_token: str = os.getenv("WHATSAPP_VERIFY_TOKEN", "")
    
    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    
    # Email Configuration (SMTP)
    smtp_server: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port: int = int(os.getenv("SMTP_PORT", "587"))
    smtp_username: str = os.getenv("SMTP_USERNAME", "")
    smtp_password: str = os.getenv("SMTP_PASSWORD", "")
    
    # Database Configuration
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./data/whatsapp_hub.db")
    
    # Server Configuration
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # Meeting Configuration
    google_meet_email: str = os.getenv("GOOGLE_MEET_EMAIL", "")
    google_meet_password: str = os.getenv("GOOGLE_MEET_PASSWORD", "")
    
    # Audio Configuration
    audio_device_index: int = int(os.getenv("AUDIO_DEVICE_INDEX", "0"))
    sample_rate: int = int(os.getenv("SAMPLE_RATE", "16000"))
    
    class Config:
        env_file = ".env"

settings = Settings()

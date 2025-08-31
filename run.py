#!/usr/bin/env python3
"""
WhatsApp Control Hub - Startup Script
"""

import uvicorn
from app.config.settings import settings

if __name__ == "__main__":
    print("🚀 Starting WhatsApp Control Hub...")
    print(f"📡 Server will be available at: http://{settings.host}:{settings.port}")
    print(f"🔗 Webhook URL: http://{settings.host}:{settings.port}/webhook")
    print("📖 API Documentation: http://localhost:8000/docs")
    print("\n⚠️  Make sure to:")
    print("   1. Copy env.example to .env and configure your settings")
    print("   2. Set up ngrok for webhook exposure: ngrok http 8000")
    print("   3. Configure WhatsApp Business API webhook URL")
    print("\n" + "="*50)
    
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level="info"
    )

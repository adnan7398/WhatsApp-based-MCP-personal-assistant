from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import logging
import json
from typing import Dict, Any

from app.config.settings import settings
from app.core.telegram_client import telegram_client
from app.core.command_router import command_router
from app.modules.reminder_scheduler import reminder_scheduler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/whatsapp_hub.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Telegram Control Hub",
    description="A comprehensive Telegram bot for productivity and automation",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Telegram Control Hub is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/webhook")
async def verify_webhook():
    """Verify webhook for Telegram Bot API"""
    logger.info("Telegram webhook verification request")
    
    # Get bot info to verify token
    bot_info = telegram_client.get_me()
    if bot_info.get("ok"):
        logger.info("Telegram webhook verified successfully")
        return {"status": "ok", "bot_info": bot_info.get("result", {})}
    
    logger.warning("Telegram webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook_handler(request: Request):
    """Handle incoming webhook messages from Telegram"""
    try:
        body = await request.json()
        logger.info(f"Received Telegram webhook: {json.dumps(body, indent=2)}")
        
        # Process the webhook message
        message_data = telegram_client.process_webhook_message(body)
        
        if message_data:
            chat_id = message_data.get("chat_id")
            message_text = message_data.get("text", "")
            message_type = message_data.get("message_type")
            username = message_data.get("username", "")
            
            logger.info(f"Processing message from {username} (chat_id: {chat_id}): {message_text}")
            
            # Handle text messages
            if message_type == "text" and message_text:
                response = command_router.handle_message(chat_id, message_text)
                
                # Send response back to Telegram
                result = telegram_client.send_text_message(chat_id, response)
                logger.info(f"Response sent: {result}")
            
            # Handle voice messages
            elif message_type == "voice":
                # TODO: Implement voice message processing
                response = "🎤 Voice message received! Processing..."
                telegram_client.send_text_message(chat_id, response)
            
            # Handle other message types
            else:
                response = f"Received {message_type} message. Text commands are supported."
                telegram_client.send_text_message(chat_id, response)
        
        return JSONResponse(content={"status": "ok"})
        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        return JSONResponse(
            content={"error": str(e)},
            status_code=500
        )

@app.get("/status")
async def get_status():
    """Get application status and configuration"""
    return {
        "status": "running",
        "telegram_configured": bool(settings.telegram_bot_token),
        "openai_configured": bool(settings.openai_api_key),
        "email_configured": bool(settings.smtp_username and settings.smtp_password),
        "available_commands": list(command_router.commands.keys())
    }

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting Telegram Control Hub...")
    # Start the reminder scheduler
    reminder_scheduler.start_scheduler()
    logger.info("Reminder scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down Telegram Control Hub...")
    # Stop the reminder scheduler
    reminder_scheduler.stop_scheduler()
    logger.info("Reminder scheduler stopped")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )

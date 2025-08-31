from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import JSONResponse
import logging
import json
from typing import Dict, Any

from app.config.settings import settings
from app.core.whatsapp_client import whatsapp_client
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
    title="WhatsApp Control Hub",
    description="A comprehensive WhatsApp bot for productivity and automation",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "WhatsApp Control Hub is running!",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = None,
    hub_verify_token: str = None,
    hub_challenge: str = None
):
    """Verify webhook for WhatsApp Business API"""
    logger.info(f"Webhook verification request: mode={hub_mode}, token={hub_verify_token}")
    
    if hub_mode and hub_verify_token and hub_challenge:
        challenge = whatsapp_client.verify_webhook(hub_mode, hub_verify_token, hub_challenge)
        if challenge:
            logger.info("Webhook verified successfully")
            return Response(content=challenge, media_type="text/plain")
    
    logger.warning("Webhook verification failed")
    raise HTTPException(status_code=403, detail="Verification failed")

@app.post("/webhook")
async def webhook_handler(request: Request):
    """Handle incoming webhook messages from WhatsApp"""
    try:
        body = await request.json()
        logger.info(f"Received webhook: {json.dumps(body, indent=2)}")
        
        # Process the webhook message
        message_data = whatsapp_client.process_webhook_message(body)
        
        if message_data:
            from_number = message_data.get("from")
            message_text = message_data.get("text", "")
            message_type = message_data.get("type")
            
            logger.info(f"Processing message from {from_number}: {message_text}")
            
            # Handle text messages
            if message_type == "text" and message_text:
                response = command_router.handle_message(from_number, message_text)
                
                # Send response back to WhatsApp
                result = whatsapp_client.send_text_message(from_number, response)
                logger.info(f"Response sent: {result}")
            
            # Handle voice messages
            elif message_type == "audio":
                # TODO: Implement voice message processing
                response = "🎤 Voice message received! Processing..."
                whatsapp_client.send_text_message(from_number, response)
            
            # Handle other message types
            else:
                response = f"Received {message_type} message. Text commands are supported."
                whatsapp_client.send_text_message(from_number, response)
        
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
        "whatsapp_configured": bool(settings.whatsapp_access_token),
        "openai_configured": bool(settings.openai_api_key),
        "email_configured": bool(settings.smtp_username and settings.smtp_password),
        "available_commands": list(command_router.commands.keys())
    }

@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("Starting WhatsApp Control Hub...")
    # Start the reminder scheduler
    reminder_scheduler.start_scheduler()
    logger.info("Reminder scheduler started")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("Shutting down WhatsApp Control Hub...")
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

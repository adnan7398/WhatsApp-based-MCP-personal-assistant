import requests
import json
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)

class TelegramClient:
    def __init__(self):
        self.bot_token = settings.telegram_bot_token
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
        
    def send_text_message(self, chat_id: str, message: str) -> Dict[str, Any]:
        """Send a text message via Telegram Bot API"""
        url = f"{self.base_url}/sendMessage"
        
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"  # Support basic HTML formatting
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Message sent successfully to chat {chat_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message: {e}")
            return {"error": str(e)}
    
    def send_media_message(self, chat_id: str, media_url: str, media_type: str = "photo") -> Dict[str, Any]:
        """Send a media message via Telegram Bot API"""
        url = f"{self.base_url}/send{media_type.capitalize()}"
        
        data = {
            "chat_id": chat_id,
            media_type: media_url
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Media message sent successfully to chat {chat_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send media message: {e}")
            return {"error": str(e)}
    
    def send_document(self, chat_id: str, document_url: str, caption: str = "") -> Dict[str, Any]:
        """Send a document via Telegram Bot API"""
        url = f"{self.base_url}/sendDocument"
        
        data = {
            "chat_id": chat_id,
            "document": document_url,
            "caption": caption
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Document sent successfully to chat {chat_id}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send document: {e}")
            return {"error": str(e)}
    
    def get_me(self) -> Dict[str, Any]:
        """Get bot information"""
        url = f"{self.base_url}/getMe"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to get bot info: {e}")
            return {"error": str(e)}
    
    def set_webhook(self, webhook_url: str) -> Dict[str, Any]:
        """Set webhook URL for the bot"""
        url = f"{self.base_url}/setWebhook"
        
        data = {
            "url": webhook_url
        }
        
        try:
            response = requests.post(url, json=data)
            response.raise_for_status()
            logger.info(f"Webhook set successfully: {webhook_url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to set webhook: {e}")
            return {"error": str(e)}
    
    def delete_webhook(self) -> Dict[str, Any]:
        """Delete webhook for the bot"""
        url = f"{self.base_url}/deleteWebhook"
        
        try:
            response = requests.post(url)
            response.raise_for_status()
            logger.info("Webhook deleted successfully")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to delete webhook: {e}")
            return {"error": str(e)}
    
    def process_webhook_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming webhook messages from Telegram"""
        try:
            if "message" not in data:
                return None
            
            message = data["message"]
            chat = message.get("chat", {})
            from_user = message.get("from", {})
            
            # Extract message content
            text = message.get("text", "")
            voice = message.get("voice")
            document = message.get("document")
            photo = message.get("photo")
            
            return {
                "chat_id": str(chat.get("id")),
                "user_id": str(from_user.get("id")),
                "username": from_user.get("username", ""),
                "first_name": from_user.get("first_name", ""),
                "last_name": from_user.get("last_name", ""),
                "timestamp": message.get("date"),
                "text": text,
                "voice": voice,
                "document": document,
                "photo": photo,
                "message_type": "text" if text else "voice" if voice else "document" if document else "photo" if photo else "unknown"
            }
        except (KeyError, IndexError) as e:
            logger.error(f"Error processing webhook message: {e}")
        
        return None

# Global Telegram client instance
telegram_client = TelegramClient()

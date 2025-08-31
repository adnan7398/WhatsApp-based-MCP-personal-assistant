import requests
import json
import logging
from typing import Dict, Any, Optional
from app.config.settings import settings

logger = logging.getLogger(__name__)

class WhatsAppClient:
    def __init__(self):
        self.access_token = settings.whatsapp_access_token
        self.phone_number_id = settings.whatsapp_phone_number_id
        self.base_url = "https://graph.facebook.com/v18.0"
        
    def send_text_message(self, to: str, message: str) -> Dict[str, Any]:
        """Send a text message via WhatsApp Business API"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Message sent successfully to {to}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send message: {e}")
            return {"error": str(e)}
    
    def send_media_message(self, to: str, media_url: str, media_type: str = "image") -> Dict[str, Any]:
        """Send a media message via WhatsApp Business API"""
        url = f"{self.base_url}/{self.phone_number_id}/messages"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to,
            "type": media_type,
            media_type: {"link": media_url}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            logger.info(f"Media message sent successfully to {to}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send media message: {e}")
            return {"error": str(e)}
    
    def verify_webhook(self, mode: str, token: str, challenge: str) -> Optional[str]:
        """Verify webhook for WhatsApp Business API"""
        if mode == "subscribe" and token == settings.whatsapp_verify_token:
            logger.info("Webhook verified successfully")
            return challenge
        return None
    
    def process_webhook_message(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Process incoming webhook messages from WhatsApp"""
        try:
            entry = data.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [])
            
            if messages:
                message = messages[0]
                return {
                    "from": message.get("from"),
                    "timestamp": message.get("timestamp"),
                    "type": message.get("type"),
                    "text": message.get("text", {}).get("body", ""),
                    "media": message.get("image") or message.get("audio") or message.get("document")
                }
        except (KeyError, IndexError) as e:
            logger.error(f"Error processing webhook message: {e}")
        
        return None

# Global WhatsApp client instance
whatsapp_client = WhatsAppClient()

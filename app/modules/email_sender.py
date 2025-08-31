import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
from app.config.settings import settings

logger = logging.getLogger(__name__)

class EmailSender:
    def __init__(self):
        self.smtp_server = settings.smtp_server
        self.smtp_port = settings.smtp_port
        self.username = settings.smtp_username
        self.password = settings.smtp_password
        
    def send_email(self, to_email: str, subject: str, body: str, from_name: str = None) -> Dict[str, Any]:
        """Send an email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = f"{from_name or 'WhatsApp Bot'} <{self.username}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add body
            msg.attach(MIMEText(body, 'plain'))
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            logger.info(f"Email sent successfully to {to_email}")
            return {
                "success": True,
                "message": f"Email sent to {to_email}",
                "subject": subject
            }
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def send_html_email(self, to_email: str, subject: str, html_body: str, from_name: str = None) -> Dict[str, Any]:
        """Send an HTML email via SMTP"""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{from_name or 'WhatsApp Bot'} <{self.username}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Add HTML body
            html_part = MIMEText(html_body, 'html')
            msg.attach(html_part)
            
            # Connect to SMTP server
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            
            # Send email
            text = msg.as_string()
            server.sendmail(self.username, to_email, text)
            server.quit()
            
            logger.info(f"HTML email sent successfully to {to_email}")
            return {
                "success": True,
                "message": f"HTML email sent to {to_email}",
                "subject": subject
            }
            
        except Exception as e:
            logger.error(f"Failed to send HTML email: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """Test SMTP connection"""
        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.quit()
            return True
        except Exception as e:
            logger.error(f"SMTP connection test failed: {e}")
            return False

# Global email sender instance
email_sender = EmailSender()

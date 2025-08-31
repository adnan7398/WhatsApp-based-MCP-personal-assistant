import re
import logging
from typing import Dict, Any, List, Optional, Callable
from app.core.whatsapp_client import whatsapp_client

logger = logging.getLogger(__name__)

class CommandRouter:
    def __init__(self):
        self.commands: Dict[str, Callable] = {}
        self.help_text = """
🤖 WhatsApp Control Hub Commands:

📧 Email Commands:
• email <to> <subject> <body> - Send email
• email boss "Update" "Project done" - Send to boss

📝 Todo Commands:
• todo add <task> - Add new task
• todo list - Show all tasks
• todo done <id> - Mark task as done

⏰ Reminder Commands:
• remind <time> <message> - Set reminder
• remind 18:30 "Join standup"

🎥 Meeting Commands:
• meeting join <url> - Join meeting
• meeting record - Start recording

🎤 Voice Commands:
• Send voice note for voice commands

Type 'help' for this message.
        """
        self._register_default_commands()
    
    def _register_default_commands(self):
        """Register default command handlers"""
        self.register_command("help", self._help_command)
        self.register_command("ping", self._ping_command)
        self.register_command("todo", self._todo_command)
        self.register_command("email", self._email_command)
        self.register_command("remind", self._remind_command)
        self.register_command("meeting", self._meeting_command)
    
    def register_command(self, command: str, handler: Callable):
        """Register a new command handler"""
        self.commands[command] = handler
        logger.info(f"Registered command: {command}")
    
    def parse_command(self, message: str) -> Optional[Dict[str, Any]]:
        """Parse a message and extract command information"""
        message = message.strip()
        if not message:
            return None
        
        # Split message into parts
        parts = message.split()
        if not parts:
            return None
        
        command = parts[0].lower()
        args = parts[1:] if len(parts) > 1 else []
        
        return {
            "command": command,
            "args": args,
            "full_message": message
        }
    
    def handle_message(self, from_number: str, message: str) -> str:
        """Handle incoming message and return response"""
        try:
            parsed = self.parse_command(message)
            if not parsed:
                return "Please send a valid command. Type 'help' for available commands."
            
            command = parsed["command"]
            args = parsed["args"]
            
            if command in self.commands:
                return self.commands[command](from_number, args, parsed)
            else:
                return f"Unknown command: {command}. Type 'help' for available commands."
                
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            return "Sorry, an error occurred while processing your command."
    
    def _help_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle help command"""
        return self.help_text
    
    def _ping_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle ping command"""
        return "pong 🏓"
    
    def _todo_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle todo commands"""
        if not args:
            return "Usage: todo <add|list|done> [task|id]"
        
        subcommand = args[0].lower()
        
        if subcommand == "add":
            if len(args) < 2:
                return "Usage: todo add <task>"
            task = " ".join(args[1:])
            # TODO: Implement todo storage
            return f"✅ Added task: {task}"
        
        elif subcommand == "list":
            # TODO: Implement todo listing
            return "📝 Your tasks:\n1. Buy milk\n2. Call boss\n3. Review project"
        
        elif subcommand == "done":
            if len(args) < 2:
                return "Usage: todo done <id>"
            task_id = args[1]
            # TODO: Implement todo completion
            return f"✅ Marked task {task_id} as done"
        
        else:
            return f"Unknown todo subcommand: {subcommand}"
    
    def _email_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle email commands"""
        if len(args) < 3:
            return "Usage: email <to> <subject> <body>"
        
        to_email = args[0]
        subject = args[1]
        body = " ".join(args[2:])
        
        # TODO: Implement email sending
        logger.info(f"Email command: to={to_email}, subject={subject}, body={body}")
        return f"📧 Email sent to {to_email}\nSubject: {subject}\nBody: {body}"
    
    def _remind_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle reminder commands"""
        if len(args) < 2:
            return "Usage: remind <time> <message>"
        
        time_str = args[0]
        message = " ".join(args[1:])
        
        # TODO: Implement reminder scheduling
        logger.info(f"Reminder set: {time_str} - {message}")
        return f"⏰ Reminder set for {time_str}: {message}"
    
    def _meeting_command(self, from_number: str, args: List[str], parsed: Dict[str, Any]) -> str:
        """Handle meeting commands"""
        if not args:
            return "Usage: meeting <join|record> [url]"
        
        subcommand = args[0].lower()
        
        if subcommand == "join":
            if len(args) < 2:
                return "Usage: meeting join <url>"
            url = args[1]
            # TODO: Implement meeting joining
            return f"🎥 Joining meeting: {url}"
        
        elif subcommand == "record":
            # TODO: Implement meeting recording
            return "🎙️ Starting meeting recording..."
        
        else:
            return f"Unknown meeting subcommand: {subcommand}"

# Global command router instance
command_router = CommandRouter()

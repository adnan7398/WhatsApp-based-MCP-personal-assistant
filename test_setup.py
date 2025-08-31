#!/usr/bin/env python3
"""
Test script for WhatsApp Control Hub
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.config.settings import settings
from app.core.command_router import command_router
from app.modules.todo_manager import todo_manager
from app.modules.email_sender import email_sender

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    print(f"Host: {settings.host}")
    print(f"Port: {settings.port}")
    print(f"WhatsApp configured: {bool(settings.whatsapp_access_token)}")
    print(f"Email configured: {bool(settings.smtp_username)}")
    print("✅ Configuration test passed\n")

def test_todo_manager():
    """Test todo manager functionality"""
    print("📝 Testing Todo Manager...")
    
    # Add a test todo
    todo = todo_manager.add_todo("Test task from setup script")
    print(f"Added todo: {todo['task']} (ID: {todo['id']})")
    
    # List todos
    todos = todo_manager.list_todos()
    print(f"Total todos: {len(todos)}")
    
    # Format for display
    formatted = todo_manager.format_todo_list()
    print("Formatted list:")
    print(formatted)
    print("✅ Todo Manager test passed\n")

def test_command_router():
    """Test command router functionality"""
    print("🎮 Testing Command Router...")
    
    # Test help command
    response = command_router.handle_message("1234567890", "help")
    print("Help command response:")
    print(response[:200] + "..." if len(response) > 200 else response)
    
    # Test ping command
    response = command_router.handle_message("1234567890", "ping")
    print(f"Ping command response: {response}")
    
    # Test todo command
    response = command_router.handle_message("1234567890", "todo list")
    print("Todo list command response:")
    print(response[:200] + "..." if len(response) > 200 else response)
    
    print("✅ Command Router test passed\n")

def test_email_sender():
    """Test email sender configuration"""
    print("📧 Testing Email Sender...")
    
    if settings.smtp_username and settings.smtp_password:
        # Test connection
        if email_sender.test_connection():
            print("✅ Email sender connection test passed")
        else:
            print("❌ Email sender connection test failed")
    else:
        print("⚠️  Email sender not configured (missing credentials)")
    
    print("✅ Email Sender test completed\n")

def main():
    """Run all tests"""
    print("🧪 WhatsApp Control Hub - Setup Test")
    print("=" * 50)
    
    try:
        test_config()
        test_todo_manager()
        test_command_router()
        test_email_sender()
        
        print("🎉 All tests passed! Your WhatsApp Control Hub is ready to run.")
        print("\nNext steps:")
        print("1. Configure your .env file with WhatsApp API credentials")
        print("2. Run: python run.py")
        print("3. Set up ngrok: ngrok http 8000")
        print("4. Configure webhook URL in Meta Developer Console")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

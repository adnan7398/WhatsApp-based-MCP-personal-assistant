#!/usr/bin/env python3
"""
Setup script for WhatsApp Control Hub
"""

import os
import shutil
from pathlib import Path

def create_env_file():
    """Create .env file from template"""
    env_example = Path("env.example")
    env_file = Path(".env")
    
    if env_file.exists():
        print("⚠️  .env file already exists. Skipping creation.")
        return
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your configuration")
    else:
        print("❌ env.example file not found")

def create_directories():
    """Create necessary directories"""
    directories = ["data", "logs"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}")

def check_python_version():
    """Check Python version"""
    import sys
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing requirements...")
    os.system("pip install -r requirements.txt")
    print("✅ Requirements installed")

def main():
    """Main setup function"""
    print("🚀 WhatsApp Control Hub Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Create directories
    create_directories()
    
    # Create .env file
    create_env_file()
    
    # Install requirements
    install_requirements()
    
    print("\n🎉 Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your configuration:")
    print("   - WhatsApp Business API credentials")
    print("   - Email SMTP settings")
    print("   - OpenAI API key (optional)")
    print("\n2. Test the setup:")
    print("   python test_setup.py")
    print("\n3. Start the server:")
    print("   python run.py")
    print("\n4. Set up ngrok for webhook:")
    print("   ngrok http 8000")
    print("\n5. Configure webhook URL in Meta Developer Console")

if __name__ == "__main__":
    main()

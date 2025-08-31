# WhatsApp Control Hub 🤖

A comprehensive WhatsApp bot for productivity and automation that transforms your WhatsApp into a powerful command center.

## 🚀 Features

### Phase 1: WhatsApp Integration ✅
- Meta WhatsApp Business API integration
- Webhook server for receiving messages
- Basic ping/pong functionality

### Phase 2: Command Router ✅
- Custom command parser
- Support for multiple command types
- Help system with command documentation

### Phase 3: Productivity Modules (In Progress)
- Email integration via SMTP
- TODO manager with JSON storage
- Reminder system with scheduling

### Phase 4: Meeting Attender + Transcriber (Planned)
- Automatic Google Meet/Zoom joining
- Audio capture and transcription
- Meeting summaries

### Phase 5: AI Enhancements (Planned)
- Auto-summarize meetings
- Voice input processing
- Knowledge memory system

### Phase 6: Dashboard (Planned)
- Web dashboard for management
- Transcript viewing
- Bot action logs

## 🛠️ Tech Stack

- **Backend**: Python FastAPI
- **WhatsApp API**: Meta WhatsApp Business Cloud API
- **Database**: SQLite (with MongoDB option)
- **Meeting Automation**: Selenium/Playwright
- **Transcription**: OpenAI Whisper
- **AI**: OpenAI GPT for summarization
- **Development**: ngrok for webhook exposure

## 📋 Prerequisites

- Python 3.8+
- Meta Developer Account
- WhatsApp Business API access
- OpenAI API key (for AI features)
- ngrok (for development)

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd whatsapp-control-hub
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp env.example .env
# Edit .env with your configuration
```

Required environment variables:
- `WHATSAPP_ACCESS_TOKEN`: Your Meta WhatsApp Business API token
- `WHATSAPP_PHONE_NUMBER_ID`: Your WhatsApp phone number ID
- `WHATSAPP_VERIFY_TOKEN`: Custom webhook verification token
- `OPENAI_API_KEY`: OpenAI API key (for AI features)

### 3. Setup WhatsApp Business API

1. Go to [Meta Developers](https://developers.facebook.com/)
2. Create a new app
3. Add WhatsApp product
4. Get your access token and phone number ID
5. Configure webhook URL (use ngrok in development)

### 4. Start the Server

```bash
python run.py
```

### 5. Expose with ngrok (Development)

```bash
ngrok http 8000
```

Use the ngrok URL as your webhook URL in Meta Developer Console.

## 📱 Usage

Once configured, send commands to your WhatsApp bot:

### Basic Commands
- `help` - Show available commands
- `ping` - Test bot connectivity

### Email Commands
- `email boss@company.com "Update" "Project completed"`

### Todo Commands
- `todo add Buy groceries`
- `todo list`
- `todo done 1`

### Reminder Commands
- `remind 18:30 "Join standup"`

### Meeting Commands
- `meeting join https://meet.google.com/xyz`
- `meeting record`

## 🔧 Development

### Project Structure

```
whatsapp-control-hub/
├── app/
│   ├── config/          # Configuration settings
│   ├── core/            # Core functionality
│   ├── modules/         # Feature modules
│   └── utils/           # Utility functions
├── data/                # Data storage
├── logs/                # Application logs
├── requirements.txt     # Python dependencies
├── run.py              # Startup script
└── README.md           # This file
```

### Adding New Commands

1. Add command handler to `app/core/command_router.py`
2. Register the command in `_register_default_commands()`
3. Update help text

### Testing

```bash
# Test the server
curl http://localhost:8000/

# Test webhook verification
curl "http://localhost:8000/webhook?hub.mode=subscribe&hub.verify_token=YOUR_TOKEN&hub.challenge=CHALLENGE"
```

## 🔒 Security

- Store sensitive data in environment variables
- Use HTTPS in production
- Validate webhook signatures
- Implement rate limiting

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the logs in `logs/` directory

---

**Happy automating! 🎉**

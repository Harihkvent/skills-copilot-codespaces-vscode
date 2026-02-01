# Astra — Voice-First Agentic Assistant

Astra is a modular voice-first AI assistant built with open-source components. It performs multi-agent reasoning, executes whitelisted tools (send email, run scripts, search the web), and keeps persistent memory.

## 🐳 Run Everything in Docker (Recommended)

**No need to install PostgreSQL, Redis, or Ollama locally!** Everything runs in Docker containers.

**🚀 Quick Start:**
```bash
git clone https://github.com/Harihkvent/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode
cp .env.example .env
docker-compose up --build
```

**That's it!** All dependencies (PostgreSQL, Redis, Ollama) run in containers.

**📖 Complete Docker Guide:** See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed instructions.

## 📚 Other Setup Options

**Want more control?** See [LOCAL_SETUP.md](LOCAL_SETUP.md) for manual setup.

**Automated scripts:**
- Linux/Mac: `./setup.sh`
- Windows: `setup.bat`

## ✨ Key Features

- 🔐 **User Authentication** - Register, login with JWT tokens
- 🤖 **Multi-Agent System** - Planner, Critic, Executor workflow
- 🛠️ **Tool Execution** - Mail sending, web search, system commands
- 📅 **Reminder Scheduler** - Cron-based reminders with APScheduler
- 💾 **Persistent Memory** - PostgreSQL + pgvector for conversations
- 🌐 **Web Interface** - Beautiful HTML client for easy interaction
- 🔍 **Real Web Search** - DuckDuckGo integration, no API key needed
- 📊 **Audit Trail** - Complete logging of all actions

## 🚀 Tech Stack

**All running in Docker containers:**
- **Backend**: Python 3.11+ + FastAPI
- **Database**: PostgreSQL + pgvector (ankane/pgvector image)
- **Cache**: Redis 7 Alpine
- **LLM**: Ollama (runs locally in Docker, no API keys!)
- **Auth**: JWT tokens with OAuth2
- **Scheduler**: APScheduler for background tasks
- **Client**: HTML/CSS/JavaScript (future: Electron + React)

**Docker Services:**
- `astra-postgres` - PostgreSQL with vector extension
- `astra-redis` - Redis cache
- `astra-ollama` - Local LLM (Llama2, Mistral, etc.)
- `astra-api` - FastAPI backend

## 📁 Project Structure

```
astra/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── agents/      # Agent implementations (Planner, Critic, Executor)
│   │   ├── api/         # API endpoints (voice, command, auth, reminders)
│   │   ├── core/        # Core configurations
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic (orchestrator, scheduler)
│   │   ├── tools/       # Tool implementations (mail, search)
│   │   └── main.py      # FastAPI application entry point
│   ├── Dockerfile
│   ├── requirements.txt
│   └── test_comprehensive.py
├── client/              # Web client interface
│   ├── index.html       # Single-page web app
│   └── README.md
├── logs/                # Application logs
├── docker-compose.yml   # Docker orchestration
├── .env.example         # Environment variables template
└── README.md
```

## 🎯 Quickstart (dev)

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Web browser (for client)

### 1. Clone repository
```bash
git clone https://github.com/Harihkvent/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode
```

### 2. Configure environment
Copy `.env.example` to `.env` and fill in your credentials:
```bash
cp .env.example .env
# Edit .env with your SMTP credentials and other settings
```

### 3. Start services with Docker Compose
```bash
docker compose up --build
```

This will start:
- PostgreSQL with pgvector extension (port 5432)
- Redis (port 6379)
- FastAPI backend (port 8000)

### 4. Access the API
The API will be available at: http://localhost:8000

API Documentation (Swagger): http://localhost:8000/docs

### 5. Use the Web Client
Open `client/index.html` in your browser to access the web interface:
```bash
open client/index.html  # macOS
xdg-open client/index.html  # Linux
start client/index.html  # Windows
```

Then:
1. Click "Register" to create an account
2. Login with your credentials
3. Start chatting with Astra!
```

Then:
1. Click "Register" to create an account
2. Login with your credentials
3. Start chatting with Astra!

## 📖 API Endpoints

### Health & Documentation
```bash
# Health check
curl http://localhost:8000/health

# API docs (Swagger UI)
open http://localhost:8000/docs
```

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "secure123"
  }'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=john&password=secure123"
```

### Commands (requires authentication)
```bash
# Voice Command
curl -X POST http://localhost:8000/api/v1/voice \
  -H "Content-Type: application/json" \
  -H "Authorization: ******" \
  -d '{
    "user_id": "user_123",
    "transcript": "Search for Python tutorials",
    "locale": "en-US"
  }'

# Direct Command
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -H "Authorization: ******" \
  -d '{
    "user_id": "user_123",
    "command": "search for artificial intelligence"
  }'
```

### Reminders (requires authentication)
```bash
# Create reminder
curl -X POST http://localhost:8000/api/v1/reminders \
  -H "Content-Type: application/json" \
  -H "Authorization: ******" \
  -d '{
    "text": "Team meeting",
    "schedule": "0 9 * * 1-5",
    "next_run": "2026-02-03T09:00:00"
  }'

# List reminders
curl http://localhost:8000/api/v1/reminders \
  -H "Authorization: ******"
```

## ⚙️ Configuration

Edit `.env` file with the following keys:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SMTP_*`: SMTP configuration for email sending
- `LLM_PROVIDER`: Choose `local` or `krutrim`
- `KRUTRIM_API_KEY`: API key if using Krutrim
- `SECRET_KEY`: JWT secret for authentication

## 🔧 Development

### Run tests
```bash
cd backend
pytest test_comprehensive.py -v
```

### Run linting
```bash
cd backend
flake8 app/
black app/ --check
```

### Database migrations
```bash
cd backend
alembic upgrade head
```

## Architecture

Astra follows a multi-agent architecture:
1. **STT Service**: Converts voice to text (Whisper/Vosk)
2. **API Gateway**: FastAPI receives requests
3. **Agent Orchestrator**: Coordinates multiple agents
   - **Perception**: Parses and normalizes input
   - **Memory**: Retrieves relevant context
   - **Planner**: Creates execution plan
   - **Critic**: Validates safety and permissions
   - **Executor**: Executes approved actions
4. **Tool Executor**: Runs whitelisted tools
5. **Memory Service**: Stores conversation and facts
6. **TTS Service**: Converts text to speech

## Security & Permissions

- All destructive actions require explicit user confirmation
- Tool execution is sandboxed by default
- All actions are logged in the audit trail
- JWT-based authentication for API access
- Per-tool permission scopes

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

MIT

## Roadmap

See [project.md](project.md) for detailed roadmap and milestones.

### Week 1 — MVP
- [x] Initialize repo and Docker Compose
- [x] Basic FastAPI server structure
- [ ] STT pipeline integration
- [ ] User authentication
- [ ] Simple memory table

### Week 2 — Tools & LLM
- [ ] mail.send tool (SMTP)
- [ ] LLM adapter (local or Krutrim)
- [ ] Planner + tool call execution

### Week 3 — Safety & UI
- [ ] Critic & confirmation flow
- [ ] Electron client with push-to-talk
- [ ] Logs & action audit

See [project.md](project.md) for complete feature list and architecture details.

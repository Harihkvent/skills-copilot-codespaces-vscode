# Astra — Voice-First Agentic Assistant

Astra is a modular voice-first AI assistant built with open-source components. It performs multi-agent reasoning, executes whitelisted tools (send email, run scripts, search the web), and keeps persistent memory.

## Key features
- Voice input (Whisper / Vosk)
- LLM-based planning (Krutrim or local LLM)
- Tool execution (mail, file, system commands)
- Memory (Postgres + pgvector)
- Multi-agent workflow (Planner / Critic / Executor)

## Tech stack
- Python + FastAPI
- PostgreSQL + pgvector
- Redis for queues
- Whisper / Vosk for STT
- Coqui TTS for speech
- Local LLM via Ollama / llama.cpp (or Krutrim API)
- Electron + React for desktop UI

## Project Structure

```
astra/
├── backend/              # FastAPI backend application
│   ├── app/
│   │   ├── agents/      # Agent implementations (Planner, Critic, Executor)
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core configurations
│   │   ├── models/      # Database models
│   │   ├── services/    # Business logic services
│   │   ├── tools/       # Tool implementations
│   │   └── main.py      # FastAPI application entry point
│   ├── Dockerfile
│   └── requirements.txt
├── client/              # Electron + React desktop client (future)
├── logs/                # Application logs
├── docker-compose.yml   # Docker orchestration
├── .env.example         # Environment variables template
└── README.md
```

## Quickstart (dev)

### Prerequisites
- Docker and Docker Compose
- Python 3.11+ (for local development)
- Node.js 18+ (for client, optional)

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

### 5. (Optional) Run Electron client
```bash
cd client
npm install
npm run dev
```

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Voice Command
```bash
curl -X POST http://localhost:8000/api/v1/voice \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "transcript": "Astra, send mail to Ravi saying I will join tomorrow",
    "locale": "en-IN"
  }'
```

### Direct Command
```bash
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "command": "send email to ravi@example.com"
  }'
```

## Configuration

Edit `.env` file with the following keys:
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SMTP_*`: SMTP configuration for email sending
- `LLM_PROVIDER`: Choose `local` or `krutrim`
- `KRUTRIM_API_KEY`: API key if using Krutrim
- `SECRET_KEY`: JWT secret for authentication

## Development

### Run tests
```bash
cd backend
pytest
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

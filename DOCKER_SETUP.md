# 🐳 Complete Docker Setup Guide

This guide shows how to run **everything** through Docker - no need to install PostgreSQL, Redis, or Ollama locally. Everything runs in containers!

---

## 📦 What's Included in Docker

The docker-compose.yml includes all dependencies:

1. **PostgreSQL with pgvector** - Database for users, messages, memories
2. **Redis** - Cache and queue management
3. **Ollama** - Local LLM for AI responses (no API keys needed!)
4. **FastAPI Backend** - The Astra API server

**Everything communicates through Docker's internal network!**

---

## 🚀 Quick Start (Complete Docker Setup)

### Prerequisites

**Only Docker is needed!** No PostgreSQL, Redis, or Python installation required.

- **Docker Desktop** (includes Docker and Docker Compose)
  - Windows: [Download](https://www.docker.com/products/docker-desktop)
  - Mac: [Download](https://www.docker.com/products/docker-desktop)
  - Linux: [Install Docker Engine](https://docs.docker.com/engine/install/)

### Step 1: Clone Repository

```bash
git clone https://github.com/Harihkvent/skills-copilot-codespaces-vscode.git
cd skills-copilot-codespaces-vscode
```

### Step 2: Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# (Optional) Edit .env to set SMTP credentials for email sending
# All database/Redis/Ollama URLs are pre-configured for Docker!
```

**Default configuration works out of the box!** The .env.example has:
- ✅ Database URL pointing to `postgres` container
- ✅ Redis URL pointing to `redis` container
- ✅ Ollama URL pointing to `ollama` container

### Step 3: Start All Services

```bash
# Build and start everything
docker-compose up --build

# Or run in background (detached mode)
docker-compose up --build -d
```

**What happens:**
1. Downloads Docker images (first time only)
2. Builds the FastAPI backend
3. Starts PostgreSQL with pgvector extension
4. Starts Redis
5. Starts Ollama for local LLM
6. Starts the API server
7. All services wait for dependencies to be healthy

**First run takes 2-5 minutes** (downloading images). Subsequent runs take ~30 seconds.

### Step 4: Download LLM Model (First Time)

After Ollama starts, download a model:

```bash
# Download Llama 2 (3.8GB, recommended)
docker exec -it astra-ollama ollama pull llama2

# Or a smaller model for testing
docker exec -it astra-ollama ollama pull llama2:7b

# Or Mistral (smaller, faster)
docker exec -it astra-ollama ollama pull mistral
```

**This only needs to be done once!** The model is stored in a Docker volume.

### Step 5: Verify Everything is Running

```bash
# Check all containers are running
docker-compose ps

# Should show 4 services:
# - astra-postgres (healthy)
# - astra-redis (healthy)
# - astra-ollama (healthy)
# - astra-api (running)

# Test the API
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","service":"Astra API",...}
```

### Step 6: Open Web Client

```bash
# Open the web interface
open client/index.html  # Mac
xdg-open client/index.html  # Linux
start client/index.html  # Windows

# Or just double-click client/index.html
```

Then:
1. Click **"Register"**
2. Create an account
3. Login
4. Start chatting with Astra!

---

## 📊 Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network                            │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  PostgreSQL  │  │    Redis     │  │   Ollama     │     │
│  │  + pgvector  │  │              │  │   (LLM)      │     │
│  │  :5432       │  │  :6379       │  │  :11434      │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│         │                  │                  │              │
│         └──────────────────┼──────────────────┘              │
│                            │                                 │
│                    ┌───────▼────────┐                       │
│                    │   FastAPI      │                       │
│                    │   Backend      │                       │
│                    │   :8000        │                       │
│                    └───────┬────────┘                       │
└────────────────────────────┼──────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   Web Client    │
                    │   (Browser)     │
                    └─────────────────┘
```

**All services communicate via Docker's internal network!**
- No need to install PostgreSQL locally
- No need to install Redis locally
- No need to install Ollama locally
- Everything is isolated and containerized

---

## 🛠️ Common Docker Commands

### View Logs

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api
docker-compose logs -f postgres
docker-compose logs -f ollama
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
docker-compose restart ollama
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (CAUTION: deletes database!)
docker-compose down -v
```

### Access Containers

```bash
# Access API container shell
docker exec -it astra-api bash

# Access PostgreSQL
docker exec -it astra-postgres psql -U astra -d astra_db

# Access Redis CLI
docker exec -it astra-redis redis-cli

# Access Ollama
docker exec -it astra-ollama bash
```

### Database Operations

```bash
# Connect to PostgreSQL
docker exec -it astra-postgres psql -U astra -d astra_db

# Run SQL query
docker exec -it astra-postgres psql -U astra -d astra_db -c "SELECT * FROM users;"

# Backup database
docker exec astra-postgres pg_dump -U astra astra_db > backup.sql

# Restore database
cat backup.sql | docker exec -i astra-postgres psql -U astra -d astra_db
```

### Ollama Operations

```bash
# List available models
docker exec -it astra-ollama ollama list

# Pull a new model
docker exec -it astra-ollama ollama pull mistral

# Remove a model
docker exec -it astra-ollama ollama rm llama2

# Test Ollama directly
docker exec -it astra-ollama ollama run llama2 "Hello!"
```

---

## 🔧 Configuration

### Using Different LLM Models

Edit `.env`:

```bash
# Use Mistral instead of Llama2
LOCAL_LLM_MODEL=mistral

# Use a specific version
LOCAL_LLM_MODEL=llama2:13b
```

Then pull the model:

```bash
docker exec -it astra-ollama ollama pull mistral
```

### Memory and Resource Limits

Edit `docker-compose.yml` to set resource limits:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        limits:
          cpus: '4'
          memory: 8G
```

### Port Changes

If ports conflict, edit `docker-compose.yml`:

```yaml
services:
  api:
    ports:
      - "8080:8000"  # Change host port from 8000 to 8080
```

---

## 🐛 Troubleshooting

### Issue: "Cannot connect to Docker daemon"

**Solution:**
```bash
# Start Docker Desktop (Windows/Mac)
# Or start Docker service (Linux)
sudo systemctl start docker
```

### Issue: "Port already in use"

**Solution:**
```bash
# Find what's using the port
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Change port in docker-compose.yml or kill the process
```

### Issue: "Ollama service unhealthy"

**Solution:**
```bash
# Ollama takes time to start (up to 40s)
# Check logs
docker-compose logs ollama

# Restart if needed
docker-compose restart ollama
```

### Issue: "Database connection failed"

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps postgres

# View logs
docker-compose logs postgres

# Restart
docker-compose restart postgres
```

### Issue: "Out of disk space"

**Solution:**
```bash
# Clean up unused Docker resources
docker system prune -a

# Remove unused volumes
docker volume prune
```

### Issue: "Ollama model not found"

**Solution:**
```bash
# Pull the model
docker exec -it astra-ollama ollama pull llama2

# Verify it's downloaded
docker exec -it astra-ollama ollama list
```

---

## 📊 Docker Volumes

Docker volumes persist data even when containers are stopped:

```bash
# List volumes
docker volume ls

# Inspect volume
docker volume inspect skills-copilot-codespaces-vscode_postgres_data

# Backup volume
docker run --rm -v skills-copilot-codespaces-vscode_postgres_data:/data -v $(pwd):/backup ubuntu tar czf /backup/postgres-backup.tar.gz /data

# Remove volumes (CAUTION: deletes all data!)
docker-compose down -v
```

**Volumes:**
- `postgres_data` - Database files
- `redis_data` - Redis data
- `ollama_data` - Downloaded LLM models

---

## 🚀 Production Deployment

For production, use these docker-compose overrides:

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  api:
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
    environment:
      - DEBUG=false
    restart: always

  postgres:
    restart: always
    
  redis:
    restart: always
    
  ollama:
    restart: always
```

Run with:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## ✅ Verification Checklist

After setup, verify everything:

- [ ] `docker-compose ps` shows 4 services running
- [ ] `curl http://localhost:8000/health` returns healthy
- [ ] `docker exec -it astra-ollama ollama list` shows downloaded models
- [ ] Web client opens in browser
- [ ] Can register a new user
- [ ] Can login
- [ ] Can send commands and get responses

---

## 🎯 Summary

**What you get with Docker setup:**

✅ **No local installations needed** - Everything runs in containers
✅ **Complete isolation** - Services don't interfere with your system
✅ **Easy cleanup** - Just `docker-compose down`
✅ **Reproducible** - Same setup on any machine
✅ **Scalable** - Easy to add more services
✅ **Production-ready** - Same setup for dev and prod

**Single command to start everything:**
```bash
docker-compose up --build
```

**No PostgreSQL, Redis, or Ollama installation required!**

---

## 📞 Need Help?

- Check logs: `docker-compose logs -f`
- Health check: `curl http://localhost:8000/health`
- View containers: `docker-compose ps`
- Access container: `docker exec -it astra-api bash`

**Everything runs through Docker!** 🐳

---

**Last Updated**: February 1, 2026
**Docker Compose Version**: 3.8
**Status**: Production Ready ✅

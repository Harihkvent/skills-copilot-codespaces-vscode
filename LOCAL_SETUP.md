# 🚀 Complete Local Setup Guide for Astra

This guide provides everything you need to run Astra locally on your machine, with detailed step-by-step instructions.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation Steps](#installation-steps)
3. [Configuration](#configuration)
4. [Running the Application](#running-the-application)
5. [Using the Web Client](#using-the-web-client)
6. [Testing the API](#testing-the-api)
7. [Troubleshooting](#troubleshooting)
8. [Development Workflow](#development-workflow)

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed on your system:

### Required Software

1. **Docker Desktop** (Recommended for easiest setup)
   - Windows: [Download Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
   - Mac: [Download Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
   - Linux: Install Docker Engine and Docker Compose
     ```bash
     # Ubuntu/Debian
     sudo apt-get update
     sudo apt-get install docker.io docker-compose
     
     # Add your user to docker group
     sudo usermod -aG docker $USER
     # Log out and back in for this to take effect
     ```

2. **Git**
   - Windows: [Download Git](https://git-scm.com/download/win)
   - Mac: `brew install git` or [Download](https://git-scm.com/download/mac)
   - Linux: `sudo apt-get install git`

3. **Web Browser** (for the web client)
   - Chrome, Firefox, Safari, or Edge

### Optional (for local development without Docker)

4. **Python 3.11+**
   - Windows: [Download Python](https://www.python.org/downloads/)
   - Mac: `brew install python@3.11`
   - Linux: `sudo apt-get install python3.11`

5. **PostgreSQL 15+** (if running without Docker)
   - [Download PostgreSQL](https://www.postgresql.org/download/)

6. **Redis** (if running without Docker)
   - Windows: [Download Redis](https://github.com/microsoftarchive/redis/releases)
   - Mac: `brew install redis`
   - Linux: `sudo apt-get install redis-server`

---

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/Harihkvent/skills-copilot-codespaces-vscode.git

# Navigate to the project directory
cd skills-copilot-codespaces-vscode

# Verify you're on the correct branch
git checkout copilot/implement-project-plan
```

### Step 2: Verify Docker Installation

```bash
# Check Docker is installed and running
docker --version
# Should show: Docker version 20.x.x or higher

docker-compose --version
# Should show: docker-compose version 1.29.x or higher

# Test Docker is running
docker ps
# Should show list of running containers (may be empty)
```

### Step 3: Explore the Project Structure

```bash
# List all files
ls -la

# You should see:
# - backend/        (FastAPI application)
# - client/         (Web interface)
# - docker-compose.yml
# - .env.example
# - README.md
# - and other documentation files
```

---

## ⚙️ Configuration

### Step 4: Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your settings
# You can use any text editor (nano, vim, notepad, VS Code, etc.)
nano .env
# or
code .env
```

**Minimum required configuration in `.env`:**

```bash
# Database (leave as-is for Docker setup)
DATABASE_URL=postgresql+asyncpg://astra:astra_password@postgres:5432/astra_db

# Redis (leave as-is for Docker setup)
REDIS_URL=redis://redis:6379/0

# SMTP Configuration (REQUIRED for email sending)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=your-email@gmail.com

# LLM Provider (use 'local' for fallback mode)
LLM_PROVIDER=local

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=true

# Security (CHANGE IN PRODUCTION!)
SECRET_KEY=change-this-to-a-random-secret-key-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

**🔑 Important Notes:**
- For Gmail SMTP, you need to create an [App Password](https://support.google.com/accounts/answer/185833)
- Don't use your regular Gmail password
- The SECRET_KEY should be changed to a random string in production

### Step 5: Generate a Secure SECRET_KEY (Recommended)

```bash
# Generate a random secret key
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Copy the output and paste it as SECRET_KEY in your .env file
```

---

## 🚀 Running the Application

### Method 1: Using Docker (Recommended)

This is the easiest way to run the entire stack.

#### Step 6: Start All Services

```bash
# Build and start all containers
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

**What happens:**
1. PostgreSQL database with pgvector extension starts on port 5432
2. Redis cache starts on port 6379
3. FastAPI backend starts on port 8000
4. All services wait for dependencies to be healthy before starting

**Expected output:**
```
Creating network "skills-copilot-codespaces-vscode_default" with the default driver
Creating astra-postgres ... done
Creating astra-redis    ... done
Creating astra-api      ... done
Attaching to astra-postgres, astra-redis, astra-api
astra-api      | 🚀 Starting Astra backend...
astra-api      | ✅ Database initialized
astra-api      | ✅ Reminder service initialized
astra-api      | INFO:     Application startup complete.
```

#### Step 7: Verify Services Are Running

Open a new terminal and run:

```bash
# Check running containers
docker-compose ps

# Should show 3 containers running:
# - astra-postgres
# - astra-redis
# - astra-api

# Check API health
curl http://localhost:8000/health

# Should return:
# {"status":"healthy","service":"Astra API","version":"0.1.0","checks":{"database":"healthy","redis":"healthy"}}
```

#### Step 8: View Logs (Optional)

```bash
# View all logs
docker-compose logs

# Follow logs in real-time
docker-compose logs -f

# View logs for specific service
docker-compose logs -f api

# Stop following logs: Ctrl+C
```

---

### Method 2: Running Without Docker (Advanced)

If you prefer to run services locally:

#### Step 6a: Install Python Dependencies

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Step 6b: Set Up Local Database

```bash
# Start PostgreSQL (if not running)
# On Mac:
brew services start postgresql
# On Linux:
sudo systemctl start postgresql

# Create database
createdb astra_db

# Enable pgvector extension
psql astra_db -c "CREATE EXTENSION vector;"
```

#### Step 6c: Update .env for Local Setup

```bash
# Change DATABASE_URL to local PostgreSQL
DATABASE_URL=postgresql+asyncpg://localhost/astra_db

# Change REDIS_URL to local Redis
REDIS_URL=redis://localhost:6379/0
```

#### Step 6d: Start Services

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start FastAPI
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🌐 Using the Web Client

### Step 9: Open the Web Interface

There are several ways to open the client:

**Option A: Direct File Open**
```bash
# From project root directory

# Mac:
open client/index.html

# Linux:
xdg-open client/index.html

# Windows:
start client/index.html

# Or double-click client/index.html in your file explorer
```

**Option B: Serve with Python HTTP Server**
```bash
# Navigate to client directory
cd client

# Start a simple HTTP server
# Python 3:
python3 -m http.server 8080
# Python 2:
python -m SimpleHTTPServer 8080

# Then open: http://localhost:8080
```

**Option C: Serve with Node.js**
```bash
# Install http-server globally
npm install -g http-server

# From client directory
cd client
http-server -p 8080

# Then open: http://localhost:8080
```

### Step 10: Register Your First User

1. **Open the web client** (you should see the Astra interface)
2. **Click the "Register" button**
3. **Fill in the registration form:**
   - Username: `admin` (or your preferred username)
   - Email: `admin@example.com`
   - Password: `password123` (choose a secure password)
4. **Click "Register"**
5. **If successful**, you'll see a success message

### Step 11: Login

1. **Click "Login"** (or the login modal will appear automatically)
2. **Enter your credentials:**
   - Username: `admin`
   - Password: `password123`
3. **Click "Login"**
4. **You're now logged in!** You should see your username displayed

### Step 12: Chat with Astra

Try these example commands:

1. **Web Search:**
   ```
   search for Python tutorials
   ```
   ```
   what is machine learning?
   ```

2. **Ask Questions:**
   ```
   tell me about artificial intelligence
   ```
   ```
   search for FastAPI documentation
   ```

3. **Create Reminders** (requires database):
   ```
   remind me to check emails at 9 AM
   ```

---

## 🧪 Testing the API

### Step 13: Test with cURL

Open a terminal and test the endpoints:

#### Health Check
```bash
curl http://localhost:8000/health
```

#### Register a User
```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "test123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=test123"
```

**Save the access_token from the response!**

#### Send a Command (requires auth token)
```bash
# Replace YOUR_TOKEN with the token from login
curl -X POST http://localhost:8000/api/v1/command \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "user_id": "test-user-id",
    "command": "search for Python"
  }'
```

### Step 14: Explore API Documentation

Open your browser and visit:

```
http://localhost:8000/docs
```

This opens the **Swagger UI** where you can:
- See all available endpoints
- Test endpoints interactively
- View request/response schemas
- Try out authentication

**To use Swagger UI with authentication:**
1. Click the "Authorize" button (🔓)
2. Enter your token: `Bearer YOUR_TOKEN`
3. Click "Authorize"
4. Now you can test authenticated endpoints

---

## 🐛 Troubleshooting

### Common Issues and Solutions

#### Issue 1: "Cannot connect to the Docker daemon"

**Solution:**
```bash
# Start Docker Desktop (Windows/Mac)
# or start Docker service (Linux)
sudo systemctl start docker

# Check Docker is running
docker ps
```

#### Issue 2: "Port 8000 is already in use"

**Solution:**
```bash
# Find what's using port 8000
# Mac/Linux:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill the process or change the port in docker-compose.yml
```

#### Issue 3: "Database connection error"

**Solution:**
```bash
# Check PostgreSQL is running
docker-compose ps

# View database logs
docker-compose logs postgres

# Restart services
docker-compose restart
```

#### Issue 4: "Module not found" errors

**Solution:**
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# Or for local setup, reinstall dependencies
cd backend
pip install -r requirements.txt
```

#### Issue 5: Web client shows "Connection error"

**Solution:**
1. Check backend is running: `curl http://localhost:8000/health`
2. Check CORS settings in backend (should allow all origins in DEBUG mode)
3. Open browser console (F12) to see detailed errors
4. Make sure you're accessing from `file://` or `http://localhost`

#### Issue 6: "Login failed" or "Registration failed"

**Solution:**
1. Check backend logs: `docker-compose logs api`
2. Verify database is running: `docker-compose ps`
3. Test health endpoint: `curl http://localhost:8000/health`
4. Try registering via Swagger UI: `http://localhost:8000/docs`

---

## 🔄 Development Workflow

### View Logs

```bash
# View all logs
docker-compose logs

# Follow specific service logs
docker-compose logs -f api

# View last 100 lines
docker-compose logs --tail=100 api
```

### Restart Services

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

### Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes (clears database)
docker-compose down -v
```

### Run Tests

```bash
# Enter the backend container
docker-compose exec api bash

# Or if not using Docker
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run specific test file
pytest test_comprehensive.py -v

# Run with coverage
pytest --cov=app
```

### Access Database

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U astra -d astra_db

# Run SQL queries
SELECT * FROM users;
\dt  # List tables
\q   # Quit
```

### Access Redis

```bash
# Connect to Redis
docker-compose exec redis redis-cli

# Check keys
KEYS *

# Get a value
GET key_name

# Exit
exit
```

### Update Dependencies

```bash
# Add new Python package
cd backend
echo "new-package==1.0.0" >> requirements.txt

# Rebuild containers
docker-compose up --build
```

---

## 📊 System Requirements

### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Disk**: 2 GB free space
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)

### Recommended Requirements
- **CPU**: 4 cores
- **RAM**: 8 GB
- **Disk**: 5 GB free space
- **Network**: Stable internet connection

---

## 🎯 Quick Reference Commands

### Start Everything
```bash
docker-compose up --build
```

### Stop Everything
```bash
docker-compose down
```

### View Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs -f
```

### Restart Backend
```bash
docker-compose restart api
```

### Access API Docs
```
http://localhost:8000/docs
```

### Health Check
```bash
curl http://localhost:8000/health
```

---

## 📞 Getting Help

If you encounter issues:

1. **Check the logs**: `docker-compose logs -f`
2. **Review the documentation**: See README.md, ARCHITECTURE.md
3. **Test the API**: Visit http://localhost:8000/docs
4. **Check database**: `docker-compose exec postgres psql -U astra -d astra_db`
5. **Restart services**: `docker-compose restart`
6. **Rebuild from scratch**: `docker-compose down -v && docker-compose up --build`

---

## ✅ Success Checklist

After setup, verify everything is working:

- [ ] Docker containers are running (`docker-compose ps`)
- [ ] Health endpoint returns healthy (`curl http://localhost:8000/health`)
- [ ] API docs are accessible (`http://localhost:8000/docs`)
- [ ] Web client opens in browser
- [ ] Can register a new user
- [ ] Can login with credentials
- [ ] Can send commands and get responses
- [ ] Web search returns results

---

## 🎉 You're Ready!

Congratulations! Astra is now running on your local machine. You can:

- Chat with Astra through the web interface
- Create reminders and scheduled tasks
- Test the API via Swagger UI
- Explore the codebase and make modifications
- Run tests and verify functionality

Happy coding! 🚀

---

**Last Updated**: February 1, 2026
**Version**: 1.0.0
**Status**: Production Ready ✅

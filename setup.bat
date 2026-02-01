@echo off
REM Astra Quick Setup Script for Windows
REM This script automates the local setup process

echo ================================================================
echo         Astra Quick Setup Script for Windows
echo ================================================================
echo.

REM Check Docker
echo Step 1: Checking prerequisites...
echo.

docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker is not installed!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [OK] Docker is installed

docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker Compose is not installed!
    pause
    exit /b 1
)
echo [OK] Docker Compose is installed

docker ps >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker daemon is not running!
    echo Please start Docker Desktop
    pause
    exit /b 1
)
echo [OK] Docker daemon is running

echo.
echo Step 2: Setting up environment...
echo.

if exist .env (
    echo [INFO] .env file already exists
    set /p OVERWRITE="Do you want to overwrite it? (y/N): "
    if /i "%OVERWRITE%"=="y" (
        copy /y .env.example .env >nul
        echo [OK] Created new .env file from .env.example
    ) else (
        echo [INFO] Keeping existing .env file
    )
) else (
    copy .env.example .env >nul
    echo [OK] Created .env file from .env.example
)

echo [INFO] Please edit .env file and set your SMTP credentials
echo [INFO] You can generate a secure SECRET_KEY with Python:
echo        python -c "import secrets; print(secrets.token_urlsafe(32))"
echo.

echo Step 3: Building Docker containers...
echo.
echo [INFO] This may take a few minutes on first run...

docker-compose up --build -d
if %errorlevel% neq 0 (
    echo [ERROR] Failed to build containers
    pause
    exit /b 1
)
echo [OK] Docker containers built and started

echo.
echo Step 4: Waiting for services to be ready...
echo.

timeout /t 10 /nobreak >nul
echo [INFO] Checking if backend is ready...

REM Simple wait loop
set COUNT=0
:WAIT_LOOP
if %COUNT% GEQ 30 goto TIMEOUT
timeout /t 2 /nobreak >nul
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 goto READY
set /a COUNT+=1
echo .
goto WAIT_LOOP

:TIMEOUT
echo [ERROR] Services failed to start within 60 seconds
echo Check logs with: docker-compose logs
pause
exit /b 1

:READY
echo [OK] Backend is ready!

echo.
echo Step 5: Testing the installation...
echo.

curl -s http://localhost:8000/health
echo.
echo [OK] Health check completed

echo.
echo Running services:
docker-compose ps

echo.
echo ================================================================
echo         Setup Complete!
echo ================================================================
echo.
echo [OK] Astra is now running!
echo.
echo Quick Links:
echo   - API: http://localhost:8000
echo   - API Docs (Swagger): http://localhost:8000/docs
echo   - Health Check: http://localhost:8000/health
echo.
echo To use the Web Client:
echo   1. Open: client\index.html in your browser
echo   2. Register a new account
echo   3. Login and start chatting!
echo.
echo Useful Commands:
echo   - View logs: docker-compose logs -f
echo   - Stop services: docker-compose down
echo   - Restart: docker-compose restart
echo.
echo [INFO] See LOCAL_SETUP.md for detailed documentation
echo.
pause

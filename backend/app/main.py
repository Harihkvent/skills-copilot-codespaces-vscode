"""
Astra Backend Application
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.api import voice, command, health, auth, reminders
from app.core.config import settings
from app.core.database import init_db
from app.services.reminder_service import init_reminder_service, shutdown_reminder_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events
    """
    # Startup
    print("🚀 Starting Astra backend...")
    await init_db()
    print("✅ Database initialized")
    await init_reminder_service()
    print("✅ Reminder service initialized")
    yield
    # Shutdown
    print("👋 Shutting down Astra backend...")
    await shutdown_reminder_service()
    print("✅ Reminder service shut down")


app = FastAPI(
    title="Astra API",
    description="Voice-First Agentic Assistant API",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
# TODO: Restrict CORS origins in production to specific domains
cors_origins = ["*"] if settings.DEBUG else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(voice.router, prefix="/api/v1", tags=["Voice"])
app.include_router(command.router, prefix="/api/v1", tags=["Command"])
app.include_router(reminders.router, prefix="/api/v1", tags=["Reminders"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "Astra API",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
    }

"""API module initialization"""
from app.api import health, voice, command, auth, reminders

__all__ = ["health", "voice", "command", "auth", "reminders"]

"""
Health check API endpoint
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db
import redis.asyncio as redis
from app.core.config import settings

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint
    Returns the status of the API and its dependencies
    """
    health_status = {
        "status": "healthy",
        "service": "Astra API",
        "version": "0.1.0",
        "checks": {}
    }
    
    # Check database connection
    try:
        await db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis connection
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.close()
        health_status["checks"]["redis"] = "healthy"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    return health_status


@router.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint
    """
    return {"status": "ready"}

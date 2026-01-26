"""
Voice command API endpoint
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.schemas import VoiceCommandRequest, VoiceCommandResponse
from app.services.orchestrator import AgentOrchestrator

router = APIRouter()


@router.post("/voice", response_model=VoiceCommandResponse)
async def process_voice_command(
    request: VoiceCommandRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Process a voice command from STT
    
    This endpoint receives transcribed text from the STT service
    and processes it through the agent orchestrator.
    """
    try:
        # Create orchestrator instance
        orchestrator = AgentOrchestrator(db)
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Process the command through orchestrator
        result = await orchestrator.process_command(
            user_id=request.user_id,
            transcript=request.transcript,
            context_id=request.context_id,
            task_id=task_id
        )
        
        return VoiceCommandResponse(
            status="accepted",
            task_id=task_id,
            estimated_ops=result.get("estimated_ops", []),
            message=result.get("message", "Command received and processing")
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process voice command: {str(e)}"
        )

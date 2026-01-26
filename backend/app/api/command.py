"""
Command API endpoint
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.core.database import get_db
from app.schemas import CommandRequest, CommandResponse
from app.services.orchestrator import AgentOrchestrator

router = APIRouter()


@router.post("/command", response_model=CommandResponse)
async def process_command(
    request: CommandRequest,
    db: AsyncSession = Depends(get_db)
):
    """
    Process a direct text command
    
    This endpoint receives natural language commands directly
    without going through STT.
    """
    try:
        # Create orchestrator instance
        orchestrator = AgentOrchestrator(db)
        
        # Generate task ID
        task_id = str(uuid.uuid4())
        
        # Process the command
        result = await orchestrator.process_command(
            user_id=request.user_id,
            transcript=request.command,
            context_id=request.context_id,
            task_id=task_id
        )
        
        return CommandResponse(
            status="success",
            task_id=task_id,
            result=result,
            message="Command processed successfully"
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process command: {str(e)}"
        )

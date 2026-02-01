"""
Reminder API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List
import uuid

from app.core.database import get_db
from app.models import Reminder, User
from app.api.auth import get_current_user
from app.services.reminder_service import reminder_service
from pydantic import BaseModel

router = APIRouter()


class ReminderCreate(BaseModel):
    text: str
    schedule: str  # Cron expression or ISO datetime
    next_run: datetime


class ReminderResponse(BaseModel):
    id: str
    text: str
    schedule: str
    next_run: datetime
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


@router.post("/reminders", response_model=ReminderResponse, status_code=status.HTTP_201_CREATED)
async def create_reminder(
    reminder_data: ReminderCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new reminder
    """
    reminder = Reminder(
        user_id=current_user.id,
        text=reminder_data.text,
        schedule=reminder_data.schedule,
        next_run=reminder_data.next_run,
        is_active=True
    )
    
    db.add(reminder)
    await db.commit()
    await db.refresh(reminder)
    
    # Add to scheduler
    try:
        await reminder_service.add_reminder(
            reminder_id=str(reminder.id),
            user_id=str(current_user.id),
            text=reminder.text,
            schedule=reminder.schedule,
            next_run=reminder.next_run
        )
    except Exception as e:
        # Rollback if scheduler fails
        await db.delete(reminder)
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to schedule reminder: {str(e)}"
        )
    
    return reminder


@router.get("/reminders", response_model=List[ReminderResponse])
async def list_reminders(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    active_only: bool = True
):
    """
    List all reminders for the current user
    """
    stmt = select(Reminder).where(Reminder.user_id == current_user.id)
    
    if active_only:
        stmt = stmt.where(Reminder.is_active == True)
    
    stmt = stmt.order_by(Reminder.next_run)
    result = await db.execute(stmt)
    reminders = result.scalars().all()
    
    return reminders


@router.delete("/reminders/{reminder_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_reminder(
    reminder_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a reminder
    """
    stmt = select(Reminder).where(
        Reminder.id == reminder_id,
        Reminder.user_id == current_user.id
    )
    result = await db.execute(stmt)
    reminder = result.scalar_one_or_none()
    
    if not reminder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reminder not found"
        )
    
    # Remove from scheduler
    await reminder_service.remove_reminder(reminder_id)
    
    # Delete from database
    await db.delete(reminder)
    await db.commit()
    
    return None

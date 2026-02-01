"""
Pydantic schemas for API request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


# User schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    is_active: bool
    
    class Config:
        from_attributes = True


# Voice command schemas
class VoiceCommandRequest(BaseModel):
    user_id: str
    transcript: str
    locale: str = "en-US"
    context_id: Optional[str] = None


class VoiceCommandResponse(BaseModel):
    status: str
    task_id: str
    estimated_ops: List[str] = []
    message: Optional[str] = None


# Command schemas
class CommandRequest(BaseModel):
    user_id: str
    command: str
    context_id: Optional[str] = None


class CommandResponse(BaseModel):
    status: str
    task_id: str
    result: Optional[Dict[str, Any]] = None
    message: Optional[str] = None


# Tool call schemas
class ToolCall(BaseModel):
    tool: str
    args: Dict[str, Any]


class ToolResult(BaseModel):
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


# Agent response schemas
class PlannerResponse(BaseModel):
    intent: str
    confidence: float
    requires_confirmation: bool = False
    tool_calls: List[ToolCall] = []
    reasoning: Optional[str] = None


class CriticResponse(BaseModel):
    approved: bool
    reasoning: str
    warnings: List[str] = []


# Message schemas
class MessageCreate(BaseModel):
    user_id: UUID
    role: str
    text: str
    context_id: Optional[str] = None
    metadata: Dict[str, Any] = {}


class MessageResponse(BaseModel):
    id: UUID
    user_id: UUID
    role: str
    text: str
    created_at: datetime
    
    class Config:
        from_attributes = True


# Memory schemas
class MemoryCreate(BaseModel):
    user_id: UUID
    text: str
    tags: List[str] = []
    metadata: Dict[str, Any] = {}


class MemoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    text: str
    tags: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Action log schemas
class ActionLogCreate(BaseModel):
    user_id: UUID
    action_type: str
    payload: Dict[str, Any]
    confirmed_by_user: bool = False


class ActionLogResponse(BaseModel):
    id: UUID
    user_id: UUID
    action_type: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

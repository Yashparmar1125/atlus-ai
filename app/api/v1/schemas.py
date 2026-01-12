"""
Pydantic schemas for API request/response validation.
"""

from pydantic import BaseModel, Field, validator
from typing import Optional, Dict, Any
from datetime import datetime


class ChatRequestSchema(BaseModel):
    """Request schema for chat endpoint."""
    message: str = Field(..., min_length=1, max_length=5000, description="User message")
    session_id: Optional[str] = Field(None, description="Optional session identifier")
    user_id: Optional[str] = Field("default_user", description="User identifier for long-term memory")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional metadata")
    
    @validator('message')
    def message_not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('message cannot be empty')
        return v.strip()


class ChatResponseData(BaseModel):
    """Response data structure."""
    response: str = Field(..., description="Agent-generated response")
    session_id: Optional[str] = Field(None, description="Session identifier")
    execution_time: float = Field(..., description="Execution time in seconds")
    request_id: Optional[str] = Field(None, description="Request identifier")


class ChatResponseSchema(BaseModel):
    """Response schema for chat endpoint."""
    success: bool = Field(..., description="Request success status")
    data: ChatResponseData = Field(..., description="Response data")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() + "Z"
        }


class ErrorResponseSchema(BaseModel):
    """Error response schema."""
    success: bool = Field(False, description="Request success status")
    error: Dict[str, Any] = Field(..., description="Error details")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    request_id: Optional[str] = Field(None, description="Request identifier")


class SessionCreateRequestSchema(BaseModel):
    """Request schema for session creation."""
    user_id: Optional[str] = Field("default_user", description="User identifier")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Optional session metadata")


class SessionCreateData(BaseModel):
    """Session creation response data."""
    session_id: str = Field(..., description="Created session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: str = Field(..., description="Session creation timestamp (ISO 8601)")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class SessionCreateResponseSchema(BaseModel):
    """Response schema for session creation."""
    success: bool = Field(True, description="Request success status")
    data: SessionCreateData = Field(..., description="Session data")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class SessionInfoData(BaseModel):
    """Session information data."""
    session_id: str = Field(..., description="Session identifier")
    user_id: str = Field(..., description="User identifier")
    created_at: str = Field(..., description="Session creation timestamp")
    last_activity: str = Field(..., description="Last activity timestamp")
    is_active: bool = Field(..., description="Session active status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")
    memory: Dict[str, Any] = Field(..., description="Memory statistics")


class SessionInfoResponseSchema(BaseModel):
    """Response schema for session info."""
    success: bool = Field(True, description="Request success status")
    data: SessionInfoData = Field(..., description="Session information")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")


class ContinueSessionData(BaseModel):
    """Continue session response data."""
    session_id: str = Field(..., description="Session identifier to continue")
    user_id: str = Field(..., description="User identifier")
    created_at: str = Field(..., description="Session creation timestamp")
    last_activity: str = Field(..., description="Last activity timestamp")
    is_active: bool = Field(..., description="Session active status")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Session metadata")


class ContinueSessionResponseSchema(BaseModel):
    """Response schema for continue session."""
    success: bool = Field(True, description="Request success status")
    data: ContinueSessionData = Field(..., description="Session data")
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")

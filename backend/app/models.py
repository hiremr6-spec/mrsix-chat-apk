from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat messages"""
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat messages"""
    reply: str
    source: str
    brand: str
    access_level: str
    timestamp: datetime
    message_id: str


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    brand: str
    engine: str
    access_policy: str
    capabilities: Dict[str, bool]
    timestamp: datetime
    version: str


class Mister6StatusResponse(BaseModel):
    """Mister 6 status response"""
    name: str
    status: str
    access_policy: str
    capabilities: Dict[str, bool]
    message: str
    timestamp: datetime


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    status_code: int
    timestamp: datetime
    request_id: Optional[str] = None

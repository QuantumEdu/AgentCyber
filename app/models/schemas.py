from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AgentRequest(BaseModel):
    """Base model for agent requests"""
    query: str
    context: Optional[str] = None


class AgentResponse(BaseModel):
    """Base model for agent responses"""
    agent_name: str
    response: str
    timestamp: datetime
    confidence: Optional[float] = None


class SecurityEvent(BaseModel):
    """Model for security events"""
    event_id: str
    severity: str  # low, medium, high, critical
    description: str
    source: str
    timestamp: datetime


class ThreatAnalysis(BaseModel):
    """Model for threat analysis results"""
    threat_level: str  # low, medium, high, critical
    indicators: List[str]
    recommendations: List[str]
    analysis: str


class IncidentResponse(BaseModel):
    """Model for incident response actions"""
    response_id: str
    actions: List[str]
    status: str  # pending, in_progress, completed
    priority: str  # low, medium, high, critical

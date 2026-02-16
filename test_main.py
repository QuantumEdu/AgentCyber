"""
Basic tests for AgentCyber system
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "AgentCyber - Multi-Agent System"
    assert data["version"] == "1.0.0"
    assert len(data["agents"]) == 3
    assert data["status"] == "operational"


def test_health_endpoint():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["agents_active"] == 3


def test_security_agent_endpoint():
    """Test the security agent endpoint"""
    response = client.post(
        "/agent/security",
        json={
            "query": "Test security event",
            "context": "Test context"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "agent_name" in data
    assert "response" in data
    assert "timestamp" in data
    assert data["agent_name"] == "Security Monitor Agent"


def test_analysis_agent_endpoint():
    """Test the analysis agent endpoint"""
    response = client.post(
        "/agent/analysis",
        json={
            "query": "Test threat analysis",
            "context": "Test context"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "agent_name" in data
    assert "response" in data
    assert "timestamp" in data
    assert data["agent_name"] == "Threat Analysis Agent"


def test_response_agent_endpoint():
    """Test the response agent endpoint"""
    response = client.post(
        "/agent/response",
        json={
            "query": "Test incident response",
            "context": "Test context"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "agent_name" in data
    assert "response" in data
    assert "timestamp" in data
    assert data["agent_name"] == "Incident Response Agent"


def test_full_analysis_endpoint():
    """Test the full multi-agent analysis endpoint"""
    response = client.post(
        "/agent/full-analysis",
        json={
            "query": "Test full analysis",
            "context": "Test context"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "query" in data
    assert "security_assessment" in data
    assert "threat_analysis" in data
    assert "response_plan" in data
    assert data["query"] == "Test full analysis"


def test_invalid_request():
    """Test invalid request to agent endpoint"""
    response = client.post(
        "/agent/security",
        json={}
    )
    assert response.status_code == 422  # Validation error

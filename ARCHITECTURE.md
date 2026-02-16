# AgentCyber - Architecture Documentation

## System Overview

AgentCyber is a multi-agent cybersecurity system that leverages artificial intelligence to provide comprehensive security analysis. The system consists of three specialized agents that work collaboratively to analyze, assess, and respond to security threats.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    FastAPI Application                       │
│                    (app/main.py)                            │
└─────────────────┬───────────────────────────────────────────┘
                  │
    ┌─────────────┼──────────────┐
    │             │              │
    ▼             ▼              ▼
┌────────┐   ┌──────────┐   ┌────────────┐
│Security│   │Analysis  │   │ Response   │
│ Agent  │   │ Agent    │   │  Agent     │
└───┬────┘   └────┬─────┘   └─────┬──────┘
    │             │               │
    └─────────────┼───────────────┘
                  │
                  ▼
         ┌────────────────┐
         │  Google Gemini │
         │   AI Model     │
         └────────────────┘
```

## Component Details

### 1. FastAPI Application (app/main.py)
- Handles HTTP requests
- Routes requests to appropriate agents
- Manages CORS and middleware
- Provides OpenAPI documentation

**Endpoints:**
- `GET /` - System information
- `GET /health` - Health check
- `POST /agent/security` - Security monitoring
- `POST /agent/analysis` - Threat analysis
- `POST /agent/response` - Incident response
- `POST /agent/full-analysis` - Complete multi-agent analysis

### 2. Security Monitor Agent (app/agents/security_agent.py)
**Purpose:** First line of defense, monitors and classifies security events

**Capabilities:**
- Event classification (normal, suspicious, threat, confirmed threat)
- Severity assessment (low, medium, high, critical)
- Initial indicator detection
- Real-time threat detection

**Output:**
- Security assessment report
- Confidence score
- Immediate concerns

### 3. Threat Analysis Agent (app/agents/analysis_agent.py)
**Purpose:** Deep dive analysis of detected threats

**Capabilities:**
- Threat classification and categorization
- Attack vector identification
- Impact assessment
- Pattern recognition
- Correlation with known threats

**Output:**
- Detailed threat analysis
- Technical assessment
- Mitigation strategies
- Confidence score

### 4. Incident Response Agent (app/agents/response_agent.py)
**Purpose:** Actionable response planning and remediation

**Capabilities:**
- Incident response plan generation
- Containment strategies
- Investigation procedures
- Eradication steps
- Recovery planning
- Prevention recommendations

**Output:**
- Complete response plan
- Prioritized action items
- Timeline and priorities
- Confidence score

## Data Flow

### Single Agent Request
```
Client Request → FastAPI → Specific Agent → Google AI → Response → Client
```

### Multi-Agent Analysis
```
Client Request → FastAPI
                   ↓
              Security Agent → Assessment
                   ↓
              Analysis Agent → Detailed Analysis
                   ↓
              Response Agent → Action Plan
                   ↓
              Combined Response → Client
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | High-performance REST API |
| AI Model | Google Gemini Pro | Natural language understanding and generation |
| Validation | Pydantic | Data validation and serialization |
| Server | Uvicorn | ASGI server |
| Testing | Pytest | Unit and integration testing |

## Configuration

The system uses environment variables for configuration:

```
GOOGLE_API_KEY - Required for AI model access
```

## Security Considerations

1. **API Key Protection**: Google API key stored in environment variables
2. **Input Validation**: Pydantic models validate all inputs
3. **Error Handling**: Graceful error handling prevents information leakage
4. **CORS**: Configurable CORS for secure API access

## Scalability

The system is designed for scalability:
- Stateless agents enable horizontal scaling
- Async/await for concurrent request handling
- FastAPI's high performance for multiple requests
- Modular design for easy agent addition

## Future Enhancements

Potential improvements:
- Database integration for event logging
- Real-time WebSocket notifications
- Agent learning from historical data
- Custom model fine-tuning
- Multi-language support
- Integration with SIEM systems

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models.schemas import AgentRequest, AgentResponse
from app.agents.security_agent import SecurityAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.response_agent import ResponseAgent
from app.utils.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Multi-agent cybersecurity system with 3 specialized agents"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
security_agent = SecurityAgent()
analysis_agent = AnalysisAgent()
response_agent = ResponseAgent()


@app.get("/")
async def root():
    """Root endpoint with system information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.VERSION,
        "agents": [
            settings.SECURITY_AGENT_NAME,
            settings.ANALYSIS_AGENT_NAME,
            settings.RESPONSE_AGENT_NAME
        ],
        "status": "operational"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agents_active": 3,
        "google_api_configured": bool(settings.GOOGLE_API_KEY)
    }


@app.post("/agent/security", response_model=AgentResponse)
async def security_analysis(request: AgentRequest):
    """
    Security monitoring and threat detection
    
    This agent monitors security events and detects potential threats.
    """
    try:
        response = await security_agent.process(request.query, request.context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Security agent error: {str(e)}")


@app.post("/agent/analysis", response_model=AgentResponse)
async def threat_analysis(request: AgentRequest):
    """
    Deep threat analysis and pattern recognition
    
    This agent performs comprehensive analysis of threats and security patterns.
    """
    try:
        response = await analysis_agent.process(request.query, request.context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis agent error: {str(e)}")


@app.post("/agent/response", response_model=AgentResponse)
async def incident_response(request: AgentRequest):
    """
    Incident response and remediation planning
    
    This agent generates incident response plans and remediation actions.
    """
    try:
        response = await response_agent.process(request.query, request.context)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Response agent error: {str(e)}")


@app.post("/agent/full-analysis", response_model=dict)
async def full_analysis(request: AgentRequest):
    """
    Complete multi-agent analysis
    
    Runs all three agents in sequence for comprehensive security analysis.
    """
    try:
        # Run security agent first
        security_response = await security_agent.process(request.query, request.context)
        
        # Use security response as context for analysis agent
        analysis_response = await analysis_agent.process(
            request.query, 
            f"Security assessment: {security_response.response}"
        )
        
        # Use both previous responses for response agent
        combined_context = f"Security: {security_response.response}\n\nAnalysis: {analysis_response.response}"
        response_plan = await response_agent.process(request.query, combined_context)
        
        return {
            "query": request.query,
            "security_assessment": security_response,
            "threat_analysis": analysis_response,
            "response_plan": response_plan
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis error: {str(e)}")

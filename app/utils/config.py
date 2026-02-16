import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings"""
    APP_NAME: str = "AgentCyber - Multi-Agent System"
    VERSION: str = "1.0.0"
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    
    # Agent configurations
    SECURITY_AGENT_NAME: str = "Security Monitor Agent"
    ANALYSIS_AGENT_NAME: str = "Threat Analysis Agent"
    RESPONSE_AGENT_NAME: str = "Incident Response Agent"


settings = Settings()

from abc import ABC, abstractmethod
from datetime import datetime
import google.generativeai as genai
from app.utils.config import settings
from app.models.schemas import AgentResponse


class BaseAgent(ABC):
    """Base class for all agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.model = None
        if settings.GOOGLE_API_KEY:
            genai.configure(api_key=settings.GOOGLE_API_KEY)
            self.model = genai.GenerativeModel('gemini-pro')
    
    @abstractmethod
    async def process(self, query: str, context: str = None) -> AgentResponse:
        """Process a query and return a response"""
        pass
    
    async def _generate_response(self, prompt: str) -> str:
        """Generate a response using Google's Gemini model"""
        if not self.model:
            return "Error: Google API key not configured"
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def _create_response(self, response_text: str, confidence: float = None) -> AgentResponse:
        """Create a standardized agent response"""
        return AgentResponse(
            agent_name=self.name,
            response=response_text,
            timestamp=datetime.now(),
            confidence=confidence
        )

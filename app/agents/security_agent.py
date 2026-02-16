from app.agents.base_agent import BaseAgent
from app.models.schemas import AgentResponse
from app.utils.config import settings


class SecurityAgent(BaseAgent):
    """Agent for monitoring and detecting security threats"""
    
    def __init__(self):
        super().__init__(settings.SECURITY_AGENT_NAME)
    
    async def process(self, query: str, context: str = None) -> AgentResponse:
        """
        Process security-related queries and detect potential threats
        
        Args:
            query: The security query or event to analyze
            context: Optional additional context
            
        Returns:
            AgentResponse with security analysis
        """
        prompt = f"""You are a cybersecurity monitoring agent. Analyze the following security event or query:

Query: {query}

{f'Context: {context}' if context else ''}

Provide a security assessment including:
1. Event classification (normal activity, suspicious, potential threat, confirmed threat)
2. Severity level (low, medium, high, critical)
3. Key indicators observed
4. Immediate concerns

Keep your response clear, concise, and actionable."""

        response_text = await self._generate_response(prompt)
        
        # Calculate confidence based on response characteristics
        confidence = self._calculate_confidence(response_text)
        
        return self._create_response(response_text, confidence)
    
    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score based on response characteristics"""
        # Simple heuristic: longer, more detailed responses have higher confidence
        if "critical" in response.lower():
            return 0.95
        elif "high" in response.lower():
            return 0.85
        elif "medium" in response.lower():
            return 0.75
        else:
            return 0.65

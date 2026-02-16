from app.agents.base_agent import BaseAgent
from app.models.schemas import AgentResponse
from app.utils.config import settings


class ResponseAgent(BaseAgent):
    """Agent for incident response and remediation actions"""
    
    def __init__(self):
        super().__init__(settings.RESPONSE_AGENT_NAME)
    
    async def process(self, query: str, context: str = None) -> AgentResponse:
        """
        Generate incident response plans and remediation actions
        
        Args:
            query: The incident or threat requiring response
            context: Optional analysis or threat context
            
        Returns:
            AgentResponse with response recommendations
        """
        prompt = f"""You are a cybersecurity incident response agent. Create a response plan for the following:

Query: {query}

{f'Context: {context}' if context else ''}

Provide an incident response plan including:
1. Immediate containment actions
2. Investigation steps
3. Eradication procedures
4. Recovery steps
5. Prevention measures for the future
6. Priority level and timeline

Format your response as a clear, actionable plan."""

        response_text = await self._generate_response(prompt)
        
        # Calculate confidence based on plan completeness
        confidence = self._calculate_confidence(response_text)
        
        return self._create_response(response_text, confidence)
    
    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score based on plan completeness"""
        # Heuristic based on action-oriented keywords
        action_keywords = ["containment", "investigation", "eradication", "recovery", "prevention"]
        keyword_count = sum(1 for keyword in action_keywords if keyword in response.lower())
        
        base_confidence = 0.65
        return min(0.95, base_confidence + (keyword_count * 0.06))

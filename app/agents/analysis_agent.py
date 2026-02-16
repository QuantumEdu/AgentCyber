from app.agents.base_agent import BaseAgent
from app.models.schemas import AgentResponse
from app.utils.config import settings


class AnalysisAgent(BaseAgent):
    """Agent for deep threat analysis and pattern recognition"""
    
    def __init__(self):
        super().__init__(settings.ANALYSIS_AGENT_NAME)
    
    async def process(self, query: str, context: str = None) -> AgentResponse:
        """
        Perform deep analysis of threats and security patterns
        
        Args:
            query: The threat or pattern to analyze
            context: Optional security event context
            
        Returns:
            AgentResponse with detailed threat analysis
        """
        prompt = f"""You are a cybersecurity threat analysis agent. Perform a deep analysis of the following:

Query: {query}

{f'Context: {context}' if context else ''}

Provide a comprehensive analysis including:
1. Threat classification and type
2. Attack vectors and techniques
3. Potential impact and scope
4. Similar known threats or patterns
5. Recommended mitigation strategies

Be thorough and technical in your analysis."""

        response_text = await self._generate_response(prompt)
        
        # Calculate confidence based on analysis depth
        confidence = self._calculate_confidence(response_text)
        
        return self._create_response(response_text, confidence)
    
    def _calculate_confidence(self, response: str) -> float:
        """Calculate confidence score based on analysis depth"""
        # Heuristic based on response detail and technical terms
        technical_terms = ["attack", "vulnerability", "exploit", "vector", "mitigation"]
        term_count = sum(1 for term in technical_terms if term in response.lower())
        
        base_confidence = 0.6
        return min(0.95, base_confidence + (term_count * 0.07))

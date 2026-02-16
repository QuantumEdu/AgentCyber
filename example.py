#!/usr/bin/env python3
"""
Example script to demonstrate AgentCyber usage
"""
import asyncio
from app.agents.security_agent import SecurityAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.response_agent import ResponseAgent


async def main():
    """Run example queries through all three agents"""
    
    # Initialize agents
    security_agent = SecurityAgent()
    analysis_agent = AnalysisAgent()
    response_agent = ResponseAgent()
    
    # Example security event (system supports multiple languages)
    query = "Multiple failed login attempts from the same IP address within 5 minutes"
    context = "IP: 192.168.1.100, Target user: admin"
    
    print("=" * 80)
    print("AGENTCYBER - MULTI-AGENT CYBERSECURITY SYSTEM")
    print("=" * 80)
    print(f"\nQuery: {query}")
    print(f"Context: {context}")
    print("\n" + "=" * 80)
    
    # Agent 1: Security Assessment
    print("\n[1] SECURITY AGENT - Initial Assessment")
    print("-" * 80)
    security_response = await security_agent.process(query, context)
    print(f"Agente: {security_response.agent_name}")
    print(f"Timestamp: {security_response.timestamp}")
    print(f"Confianza: {security_response.confidence:.2%}" if security_response.confidence else "")
    print(f"\nRespuesta:\n{security_response.response}")
    
    # Agent 2: Threat Analysis
    print("\n" + "=" * 80)
    print("\n[2] ANALYSIS AGENT - Deep Analysis")
    print("-" * 80)
    analysis_context = f"Previous security assessment: {security_response.response[:200]}..."
    analysis_response = await analysis_agent.process(query, analysis_context)
    print(f"Agente: {analysis_response.agent_name}")
    print(f"Timestamp: {analysis_response.timestamp}")
    print(f"Confianza: {analysis_response.confidence:.2%}" if analysis_response.confidence else "")
    print(f"\nRespuesta:\n{analysis_response.response}")
    
    # Agent 3: Incident Response
    print("\n" + "=" * 80)
    print("\n[3] RESPONSE AGENT - Action Plan")
    print("-" * 80)
    response_context = f"Previous analysis: {analysis_response.response[:200]}..."
    response_plan = await response_agent.process(query, response_context)
    print(f"Agente: {response_plan.agent_name}")
    print(f"Timestamp: {response_plan.timestamp}")
    print(f"Confianza: {response_plan.confidence:.2%}" if response_plan.confidence else "")
    print(f"\nRespuesta:\n{response_plan.response}")
    
    print("\n" + "=" * 80)
    print("COMPLETE ANALYSIS FINISHED")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

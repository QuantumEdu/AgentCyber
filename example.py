#!/usr/bin/env python3
"""
Example script to demonstrate AgentCyber usage
"""
import asyncio
import sys
sys.path.insert(0, '/home/runner/work/AgentCyber/AgentCyber')

from app.agents.security_agent import SecurityAgent
from app.agents.analysis_agent import AnalysisAgent
from app.agents.response_agent import ResponseAgent


async def main():
    """Run example queries through all three agents"""
    
    # Initialize agents
    security_agent = SecurityAgent()
    analysis_agent = AnalysisAgent()
    response_agent = ResponseAgent()
    
    # Example security event
    query = "Múltiples intentos de acceso fallidos desde la misma IP en 5 minutos"
    context = "IP: 192.168.1.100, Usuario objetivo: admin"
    
    print("=" * 80)
    print("AGENTCYBER - SISTEMA MULTIAGENTE DE CIBERSEGURIDAD")
    print("=" * 80)
    print(f"\nConsulta: {query}")
    print(f"Contexto: {context}")
    print("\n" + "=" * 80)
    
    # Agent 1: Security Assessment
    print("\n[1] AGENTE DE SEGURIDAD - Evaluación inicial")
    print("-" * 80)
    security_response = await security_agent.process(query, context)
    print(f"Agente: {security_response.agent_name}")
    print(f"Timestamp: {security_response.timestamp}")
    print(f"Confianza: {security_response.confidence:.2%}" if security_response.confidence else "")
    print(f"\nRespuesta:\n{security_response.response}")
    
    # Agent 2: Threat Analysis
    print("\n" + "=" * 80)
    print("\n[2] AGENTE DE ANÁLISIS - Análisis profundo")
    print("-" * 80)
    analysis_context = f"Evaluación de seguridad previa: {security_response.response[:200]}..."
    analysis_response = await analysis_agent.process(query, analysis_context)
    print(f"Agente: {analysis_response.agent_name}")
    print(f"Timestamp: {analysis_response.timestamp}")
    print(f"Confianza: {analysis_response.confidence:.2%}" if analysis_response.confidence else "")
    print(f"\nRespuesta:\n{analysis_response.response}")
    
    # Agent 3: Incident Response
    print("\n" + "=" * 80)
    print("\n[3] AGENTE DE RESPUESTA - Plan de acción")
    print("-" * 80)
    response_context = f"Análisis previo: {analysis_response.response[:200]}..."
    response_plan = await response_agent.process(query, response_context)
    print(f"Agente: {response_plan.agent_name}")
    print(f"Timestamp: {response_plan.timestamp}")
    print(f"Confianza: {response_plan.confidence:.2%}" if response_plan.confidence else "")
    print(f"\nRespuesta:\n{response_plan.response}")
    
    print("\n" + "=" * 80)
    print("ANÁLISIS COMPLETO FINALIZADO")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(main())

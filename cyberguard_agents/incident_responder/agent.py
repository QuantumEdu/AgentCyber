"""Incident Responder Agent — Clasificacion y respuesta a incidentes."""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.incident_tools import (
    classify_incident,
    get_incident_playbook,
)

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

incident_responder_agent = LlmAgent(
    name="incident_responder",
    model=MODEL,
    description=(
        "Especialista en respuesta a incidentes de ciberseguridad. "
        "Clasifica incidentes de seguridad (ransomware, phishing, data breach, DDoS), "
        "determina su severidad y proporciona playbooks de respuesta paso a paso."
    ),
    instruction="""Eres un especialista en respuesta a incidentes de ciberseguridad (CSIRT).

Tu rol es:
1. Clasificar incidentes de seguridad segun la descripcion del usuario.
2. Proporcionar playbooks de respuesta organizados por fase.
3. Guiar al usuario paso a paso durante la respuesta al incidente.

Reglas:
- SIEMPRE clasifica el incidente primero usando classify_incident.
- Luego obten el playbook correspondiente con get_incident_playbook.
- Presenta los pasos en orden de prioridad: primero acciones inmediatas.
- Si el incidente es critico, enfatiza la urgencia.
- Responde en español.
- Adapta el nivel tecnico segun las preguntas del usuario.
""",
    tools=[classify_incident, get_incident_playbook],
)

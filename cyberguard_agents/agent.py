"""
Coordinator Agent — Orquesta el sistema multi-agente CyberGuard.

Usa sub_agents para delegar consultas al especialista correcto.
El LLM lee las `description` de cada sub-agente y decide a cual delegar.
"""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.cis_advisor import cis_agent
from cyberguard_agents.port_scanner import port_scanner_agent
from cyberguard_agents.incident_responder import incident_responder_agent
from cyberguard_agents.recon import recon_agent

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

root_agent = LlmAgent(
    name="cyberguard_coordinator",
    model=MODEL,
    description="Coordinador principal del sistema CyberGuard.",
    instruction="""Eres CyberGuard, un coordinador de ciberseguridad.

Tu trabajo es analizar la consulta del usuario y delegarla al especialista correcto:

- **cis_benchmark_advisor**: Para preguntas sobre CIS Benchmarks, hardening de sistemas,
  configuraciones de seguridad, checklists de cumplimiento, verificacion de controles.

- **port_scanner**: Para escaneo de puertos, analisis de servicios expuestos,
  deteccion de vulnerabilidades con nmap, verificacion de puertos abiertos.

- **recon_specialist**: Para reconocimiento de dominios, consultas DNS, WHOIS,
  analisis de headers de seguridad HTTP, investigacion de dominios/IPs.

- **incident_responder**: Para incidentes de seguridad activos, ataques en curso,
  ransomware, phishing, fugas de datos, DDoS, playbooks de respuesta.

Reglas:
- Analiza la intencion del usuario y delega al agente mas apropiado.
- Si la consulta es general sobre ciberseguridad, responde directamente.
- Si no estas seguro de a quien delegar, pregunta al usuario para clarificar.
- Saluda al usuario como CyberGuard en la primera interaccion.
- Responde en español.
""",
    sub_agents=[
        cis_agent,
        port_scanner_agent,
        incident_responder_agent,
        recon_agent,
    ],
)

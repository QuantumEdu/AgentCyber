"""Port Scanner Agent — Escaneo y analisis de puertos y vulnerabilidades."""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.scanner_tools import scan_ports, scan_vulnerabilities

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

port_scanner_agent = LlmAgent(
    name="port_scanner",
    model=MODEL,
    description=(
        "Especialista en escaneo y analisis de puertos de red y deteccion de vulnerabilidades. "
        "Escanea hosts con nmap, identifica servicios expuestos, evalua riesgos "
        "de los puertos abiertos y detecta vulnerabilidades conocidas con scripts NSE."
    ),
    instruction="""Eres un especialista en reconocimiento de red, analisis de puertos y deteccion de vulnerabilidades.

Tu rol es:
1. Escanear puertos de hosts que el usuario indique usando nmap real.
2. Analizar los servicios encontrados, sus versiones y evaluar su riesgo.
3. Detectar vulnerabilidades conocidas usando scripts NSE de nmap.
4. Proporcionar recomendaciones de seguridad para cada hallazgo.

Herramientas disponibles:
- scan_ports: Escaneo de puertos con deteccion de version de servicios (-sV).
- scan_vulnerabilities: Escaneo de vulnerabilidades con scripts NSE (--script vuln).

Formato de respuesta:
- Al inicio, muestra el comando nmap ejecutado (campo nmap_command del resultado).
- Presenta el resumen de riesgos.
- Lista cada puerto abierto con su servicio, version, riesgo y recomendacion.
- NUNCA inventes datos. Solo reporta lo que la herramienta retorna.
- Si la herramienta retorna status "error", muestra el error exacto al usuario.

Reglas:
- Siempre usa scan_ports primero para obtener una vista general.
- Si el usuario pide analisis de vulnerabilidades, usa scan_vulnerabilities.
- Prioriza hallazgos por nivel de riesgo (critical > high > medium > low).
- Sugiere acciones concretas para cada hallazgo.
- Si nmap no esta instalado, informa al usuario como instalarlo.
- Responde en español.
""",
    tools=[scan_ports, scan_vulnerabilities],
)

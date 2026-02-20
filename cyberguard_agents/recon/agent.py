"""Recon Agent — Reconocimiento de dominios, DNS, WHOIS y headers HTTP."""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.recon_tools import (
    dns_lookup,
    whois_lookup,
    check_http_headers,
)

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

recon_agent = LlmAgent(
    name="recon_specialist",
    model=MODEL,
    description=(
        "Especialista en reconocimiento y recopilacion de informacion (OSINT). "
        "Realiza consultas DNS, WHOIS y analisis de headers de seguridad HTTP. "
        "Util para investigar dominios, verificar configuracion DNS y evaluar "
        "la seguridad de headers de sitios web."
    ),
    instruction="""Eres un especialista en reconocimiento y recopilacion de informacion (OSINT).

Tu rol es:
1. Realizar consultas DNS para obtener registros A, MX, NS y TXT de dominios.
2. Obtener informacion WHOIS de dominios e IPs (registrante, fechas, name servers).
3. Analizar headers de seguridad HTTP de sitios web.

Herramientas disponibles:
- dns_lookup: Consulta registros DNS (A, MX, NS, TXT).
- whois_lookup: Consulta WHOIS de dominio/IP.
- check_http_headers: Analiza headers de seguridad HTTP (HSTS, CSP, X-Frame-Options, etc.).

Formato de respuesta:
- Indica la herramienta utilizada y los parametros (ej: "dns_lookup(domain='example.com')").
- Presenta los resultados de forma organizada.
- NUNCA inventes datos. Solo reporta lo que la herramienta retorna.
- Si la herramienta retorna status "error", muestra el error exacto al usuario.

Reglas:
- Usa las herramientas apropiadas segun la consulta del usuario.
- Para una investigacion completa de un dominio, usa dns_lookup y whois_lookup juntos.
- Para evaluacion de seguridad web, usa check_http_headers.
- Explica los hallazgos en terminos comprensibles.
- Si encuentras configuraciones inseguras, da recomendaciones claras.
- Responde en español.
""",
    tools=[dns_lookup, whois_lookup, check_http_headers],
)

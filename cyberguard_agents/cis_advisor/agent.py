"""
CIS Benchmark Advisor Agent.

Usa OpenRouter via LiteLLM para acceder a modelos LLM.
"""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.cis_tools import (
    check_cis_benchmark,
    get_hardening_checklist,
    run_cis_check,
)

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

cis_agent = LlmAgent(
    name="cis_benchmark_advisor",
    model=MODEL,
    description=(
        "Especialista en CIS Benchmarks para Linux y Windows. "
        "Consulta controles especificos, proporciona checklists de hardening, "
        "ejecuta verificaciones reales en el sistema local, "
        "y da recomendaciones de remediacion basadas en los estandares CIS."
    ),
    instruction="""Eres un experto en CIS Benchmarks y hardening de sistemas.

Tu rol es:
1. Ayudar a los usuarios a entender y aplicar controles de seguridad CIS.
2. Proporcionar comandos de verificacion y pasos de remediacion.
3. Ejecutar verificaciones reales de controles CIS en el sistema local.
4. Dar recomendaciones priorizadas segun el nivel del benchmark (Level 1 = esencial, Level 2 = avanzado).

Herramientas disponibles:
- check_cis_benchmark: Consulta detalles de un control CIS especifico.
- get_hardening_checklist: Lista controles de hardening filtrados por OS y categoria.
- run_cis_check: Ejecuta el comando de verificacion real en el sistema local.

Formato de respuesta:
- Al usar run_cis_check, muestra el comando ejecutado (campo check_command) y su resultado (stdout/stderr).
- Indica claramente si el control paso o no (campo passed).
- NUNCA inventes datos. Solo reporta lo que la herramienta retorna.
- Si la herramienta retorna status "error", muestra el error exacto al usuario.

Reglas:
- Siempre usa las herramientas disponibles para consultar benchmarks reales, NO inventes controles.
- Si el usuario no especifica OS, pregunta cual sistema operativo necesita.
- Usa run_cis_check cuando el usuario quiera verificar si un control se cumple en su sistema.
- Responde en español.
- Se conciso pero completo en las remediaciones.
- Incluye siempre el comando de verificacion cuando sea relevante.
""",
    tools=[check_cis_benchmark, get_hardening_checklist, run_cis_check],
)

# Agentes de IA Aplicados a Ciberseguridad
### Google ADK · OpenRouter · FastAPI · CyberGuard Multi-Agent System

> **Stack:** Python · Google ADK · LiteLLM · OpenRouter · FastAPI
> **Nivel:** Básico-Intermedio · Audiencia: Técnica y Semi-técnica
> **Fecha:** Febrero 2026

---

# SECCIÓN 1: FUNDAMENTOS DE AGENTES DE IA

---

## Slide 01 — ¿Qué es un Agente de IA?

Un **agente de IA** es un sistema que percibe su entorno, razona y ejecuta acciones de forma autónoma para cumplir un objetivo.

A diferencia de un LLM estándar (que solo genera texto), un agente puede:

| Capacidad | LLM clásico | Agente de IA |
|-----------|:-----------:|:------------:|
| Responder preguntas | ✅ | ✅ |
| Usar herramientas externas | ❌ | ✅ |
| Ejecutar acciones en el mundo | ❌ | ✅ |
| Mantener estado entre turnos | ❌ | ✅ |
| Delegar a otros agentes | ❌ | ✅ |
| Tomar decisiones iterativas | ❌ | ✅ |

> **Analogía:** Un LLM es como un libro de referencia. Un agente es como un consultor que lee el libro, llama a quien corresponde y te entrega el informe.

---

## Slide 02 — Contexto, Memoria y Herramientas

Un agente opera con tres pilares fundamentales:

```
┌──────────────────────────────────────────────────────┐
│                    AGENTE DE IA                      │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────┐  │
│  │   CONTEXTO  │  │   MEMORIA    │  │ HERRAMIENTAS│  │
│  │             │  │              │  │  (Tools)    │  │
│  │ System      │  │ Historial de │  │ • APIs      │  │
│  │ prompt /    │  │ conversación │  │ • Scripts   │  │
│  │ Instruction │  │ (Session)    │  │ • DBs       │  │
│  │             │  │              │  │ • Subagentes│  │
│  └─────────────┘  └──────────────┘  └─────────────┘  │
│                          │                           │
│                      LLM como                        │
│                    "cerebro" central                 │
└──────────────────────────────────────────────────────┘
```

- **Contexto (instruction):** Define el rol, restricciones y comportamiento del agente. Es su "personalidad".
- **Memoria (session):** Historial de la conversación. Permite coherencia multi-turno.
- **Herramientas (tools):** Funciones reales que el agente puede invocar: buscar, calcular, conectarse a sistemas.

---

## Slide 03 — Flujo de Trabajo: El Loop ReAct

Los agentes modernos siguen el patrón **ReAct** *(Reasoning + Acting)*:

```
  ┌─────────────────────────────────────────────────┐
  │  Usuario: "Escanea los puertos de 192.168.1.1"  │
  └────────────────────┬────────────────────────────┘
                       │
                  ┌────▼─────┐
                  │  PENSAR  │  El LLM analiza la solicitud
                  │ (Reason) │  y decide qué acción tomar
                  └────┬─────┘
                       │
                  ┌────▼─────┐
                  │  ACTUAR  │  Invoca herramienta:
                  │  (Act)   │  scan_ports("192.168.1.1")
                  └────┬─────┘
                       │
                  ┌────▼─────┐
                  │ OBSERVAR │  Recibe resultado del
                  │(Observe) │  escaneo (puertos abiertos)
                  └────┬─────┘
                       │
              ¿Necesita más pasos?
               /              \
             SÍ               NO
              │                │
         Vuelve a          ┌───▼────┐
          PENSAR           │RESPONDE│
                           └────────┘
```

Este ciclo se repite hasta que el agente considera que tiene suficiente información para responder al usuario.

---

# SECCIÓN 2: GOOGLE AGENT DEVELOPMENT KIT (ADK)

---

## Slide 04 — ¿Qué es Google ADK?

**Agent Development Kit (ADK)** es un framework open-source de Google para construir sistemas agentivos en Python. Ofrece estructura profesional sin YAML ni configuraciones mágicas.

### Características principales

- **Code-First:** Todo se define en Python puro.
- **Model-Agnostic:** Gemini nativo + cualquier LLM vía **LiteLLM** (OpenAI, Anthropic, Ollama, OpenRouter...).
- **Multi-Agente por diseño:** Jerarquías coordinador → sub-agentes con routing automático por LLM.
- **Tools nativas:** Funciones Python normales se convierten en herramientas del agente.
- **Session & State:** Gestión de conversaciones y estado entre turnos lista para usar.
- **FastAPI integrado:** `get_fast_api_app()` expone agentes como API REST en segundos.
- **Web UI incluida:** `adk web` levanta una interfaz de desarrollo visual.

> **Repositorio oficial:** [github.com/google/adk-python](https://github.com/google/adk-python)
> **Documentación:** [google.github.io/adk-docs](https://google.github.io/adk-docs/)

---

## Slide 05 — ADK vs Otras Alternativas

| Aspecto | **ADK** | LangChain | CrewAI |
|---------|---------|-----------|--------|
| Enfoque | Software engineering | Chaining / RAG | Role-playing |
| Curva de aprendizaje | **Baja** | Alta | Media |
| Multi-agente | **Nativo (jerárquico)** | LangGraph separado | Nativo (secuencial) |
| Deployment | **FastAPI integrado** | Manual | Manual |
| Model flexibility | **LiteLLM built-in** | Sí | Limitado |
| Web UI de desarrollo | **`adk web` incluido** | No | No |
| Configuración | **Python puro** | Python + YAML | Python + decoradores |

### ¿Cuándo usar ADK?

- Sistemas multi-agente con routing inteligente entre especialistas.
- Proyectos donde el modelo LLM puede cambiar (o usar distintos por agente).
- Cuando se necesita deploy rápido como API REST.
- Proyectos de ciberseguridad, automatización, asistentes especializados.

---

# SECCIÓN 3: MANOS AL CÓDIGO

---

## Slide 06 — Instalación y Configuración del Entorno

### Requisitos previos

- Python 3.10+
- Cuenta en [openrouter.ai](https://openrouter.ai/) *(tienen modelos gratuitos para pruebas)*

### Paso a paso

```bash
# 1. Crear el proyecto
mkdir mi-agente && cd mi-agente

# 2. Entorno virtual
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
# .venv\Scripts\activate         # Windows

# 3. Instalar ADK con soporte LiteLLM
pip install google-adk[litellm] fastapi uvicorn[standard] python-dotenv
```

### Configurar API Key

```bash
# Archivo .env (NUNCA subir al repositorio)
OPENROUTER_API_KEY=sk-or-v1-TU_KEY_AQUI
GOOGLE_GENAI_USE_VERTEXAI=0
```

### Estructura mínima que ADK espera

```
mi_agente/
├── .env
├── requirements.txt
└── mi_agente/
    ├── __init__.py    # debe exportar root_agent
    └── agent.py       # define root_agent
```

> ADK busca una variable llamada **`root_agent`** en `__init__.py` o `agent.py` del paquete del agente.

---

## Slide 07 — Estructura Básica de un Agente en Código

Un agente ADK mínimo funcional:

```python
# mi_agente/agent.py
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

# Función Python → Tool del agente
def saludar(nombre: str) -> dict:
    """
    Saluda al usuario por su nombre.

    Args:
        nombre: El nombre de la persona a saludar.

    Returns:
        dict: Mensaje de saludo.
    """
    return {"mensaje": f"Hola, {nombre}! Soy tu agente."}


# Configuración del LLM
MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

# Definición del agente
root_agent = LlmAgent(
    name="mi_agente",              # Identificador único
    model=MODEL,                   # LLM que usará
    description="Agente de demostración.",
    instruction="Eres un asistente amigable. Responde en español.",
    tools=[saludar],               # Herramientas disponibles
)
```

```python
# mi_agente/__init__.py
from .agent import root_agent
```

---

## Slide 08 — Configurar el LLM con LiteLLM

ADK soporta múltiples proveedores a través de **LiteLLM**, usando un formato de nombre unificado.

```python
from google.adk.models.lite_llm import LiteLlm

# ── OpenRouter (acceso a múltiples modelos) ──────────────
MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",   # Recomendado
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

# ── Alternativas con OpenRouter ──────────────────────────
# "openrouter/anthropic/claude-sonnet-4"          # Claude
# "openrouter/openai/gpt-4o-mini"                 # OpenAI
# "openrouter/google/gemma-2-9b-it:free"          # Gratuito para pruebas

# ── Gemini directo (Google AI Studio) ───────────────────
# MODEL = "gemini-2.5-flash"
# (requiere GOOGLE_API_KEY en .env)

# ── Ollama (modelos locales) ─────────────────────────────
# MODEL = LiteLlm(model="ollama/llama3.2", api_base="http://localhost:11434")
```

### Modelos recomendados en OpenRouter

| Modelo | Costo aprox. | Tool Calling | Caso de uso |
|--------|:------------:|:------------:|-------------|
| `gemma-2-9b-it:free` | Gratis | Limitado | Pruebas básicas |
| `gemini-2.5-flash` | ~$0.15/1M tokens | Sí | Producción / mejor ratio |
| `gpt-4o-mini` | ~$0.15/1M tokens | Sí | Bueno para tools |
| `claude-sonnet-4` | ~$3/1M tokens | Sí | Máxima calidad |

---

## Slide 09 — Invocar el Agente con Runner

El **Runner** es el motor de ejecución de ADK. Recibe el mensaje, lo pasa al agente, gestiona las llamadas a tools y devuelve el stream de eventos.

```python
import asyncio
from dotenv import load_dotenv
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mi_agente import root_agent

async def main():
    # Servicio de sesiones (en memoria para desarrollo)
    session_service = InMemorySessionService()

    # Crear sesión (mantiene el historial de conversación)
    session = await session_service.create_session(
        app_name="demo",
        user_id="usuario_01",
        session_id="sesion_01",
    )

    # Motor de ejecución
    runner = Runner(
        agent=root_agent,
        app_name="demo",
        session_service=session_service,
    )

    # Construir mensaje en formato ADK
    mensaje = types.Content(
        role="user",
        parts=[types.Part(text="Saluda a María")]
    )

    # Ejecutar y procesar el stream de eventos
    async for evento in runner.run_async(
        user_id="usuario_01",
        session_id="sesion_01",
        new_message=mensaje,
    ):
        if evento.is_final_response():
            print(evento.content.parts[0].text)

asyncio.run(main())
```

---

## Slide 10 — ADK Web UI: El Presentador Visual

ADK incluye una interfaz web de desarrollo que permite interactuar con el agente, visualizar el flujo de delegación y las llamadas a tools.

### Cómo levantar el Web UI

```bash
# Desde el directorio PADRE del paquete del agente
# (donde está la carpeta mi_agente/)
adk web
```

Abre tu navegador en `http://localhost:8000`

```
┌─────────────────────────────────────────────────────┐
│  ADK Developer UI  ·  localhost:8000                 │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Agente: [  mi_agente  ▾ ]                          │
│                                                      │
│  ┌──────────────────────────────────────────────┐    │
│  │ 🤖 Hola! ¿En qué puedo ayudarte?            │    │
│  │                                              │    │
│  │ 👤 Saluda a María                            │    │
│  │                                              │    │
│  │ 🔧 Tool call: saludar(nombre="María")        │    │
│  │ 📦 Tool response: {mensaje: "Hola, María!"}  │    │
│  │                                              │    │
│  │ 🤖 ¡Hola, María! Soy tu agente.             │    │
│  └──────────────────────────────────────────────┘    │
│                                                      │
│  [Escribe tu mensaje aquí...]          [Enviar]      │
└─────────────────────────────────────────────────────┘
```

> Ideal para desarrollo y depuración: muestra tool calls, delegaciones entre agentes y el estado de la sesión en tiempo real.

---

## Slide 11 — Invocación vía cURL (ADK nativo)

ADK también expone una API interna cuando se usa `adk api_server`.

### Levantar el API server nativo de ADK

```bash
adk api_server
# Escucha en http://localhost:8000
```

### Crear sesión y enviar mensaje con cURL

```bash
# 1. Crear sesión
curl -X POST http://localhost:8000/apps/mi_agente/users/user01/sessions \
  -H "Content-Type: application/json" \
  -d '{"state": {}}'

# Respuesta: {"id": "abc-123", ...}

# 2. Enviar mensaje a la sesión
curl -X POST http://localhost:8000/run \
  -H "Content-Type: application/json" \
  -d '{
    "app_name": "mi_agente",
    "user_id": "user01",
    "session_id": "abc-123",
    "new_message": {
      "role": "user",
      "parts": [{"text": "Saluda a María"}]
    }
  }'
```

> Para un endpoint productivo y personalizable, se recomienda construir el servidor con **FastAPI** (sección siguiente).

---

# SECCIÓN 4: FASTAPI COMO ENDPOINT

---

## Slide 12 — ¿Por Qué FastAPI? — Ventajas

FastAPI es el framework web Python más adecuado para exponer agentes ADK como servicios REST.

### Ventajas clave

| Característica | Beneficio concreto |
|---------------|-------------------|
| **Async nativo** | Compatible al 100% con `runner.run_async()` de ADK sin workarounds |
| **Pydantic integrado** | Validación y serialización automática de request/response |
| **Swagger automático** | Documentación interactiva en `/docs` lista para compartir |
| **Alto rendimiento** | Basado en Starlette + Uvicorn, comparable a Node.js |
| **CORS integrado** | Permite consumo desde frontends web con middleware simple |
| **Ecosistema maduro** | Auth, rate limiting, middleware, logging — todo disponible |
| **ADK lo usa internamente** | `get_fast_api_app()` de ADK genera FastAPI; la integración es natural |

---

## Slide 13 — ¿Por Qué FastAPI? — Flujo de Integración

### Flujo completo: cliente → FastAPI → ADK → agente

```
Cliente (browser / app / cURL)
        │
        │  POST /chat
        │  {"message": "Escanea 192.168.1.1", "user_id": "sec"}
        ▼
┌──────────────────────────────┐
│       FastAPI Endpoint       │
│  @app.post("/chat")          │
│  async def chat(req):        │
└──────────────┬───────────────┘
               │  runner.run_async(user_id, session_id, mensaje)
               ▼
┌──────────────────────────────┐
│          ADK Runner          │
│  gestiona sesión y eventos   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│        root_agent (LLM)      │
│   decide → delega → tools    │
└──────────────┬───────────────┘
               │  evento.is_final_response()
               ▼
┌──────────────────────────────┐
│     FastAPI Response         │
│  {"response": "...",         │
│   "session_id": "uuid"}      │
└──────────────────────────────┘
```

> El patrón `async for evento in runner.run_async(...)` es la clave: FastAPI y ADK comparten el mismo event loop asyncio, por eso la integración es transparente.

---

## Slide 14 — Servidor FastAPI — Setup y Modelo

### main.py — Configuración inicial y modelo Pydantic

```python
import os, uuid
from dotenv import load_dotenv
load_dotenv()                          # cargar .env ANTES de importar agentes

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from mi_agente import root_agent

# ── Session y Runner ─────────────────────────────────────
session_service = InMemorySessionService()   # en memoria (dev)
runner = Runner(
    agent=root_agent,
    app_name="demo",
    session_service=session_service,
)

# ── Modelos Pydantic ─────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default"
    session_id: str | None = None    # None = nueva sesión automática

# ── App FastAPI ──────────────────────────────────────────
app = FastAPI(title="Mi Agente API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])
```

---

## Slide 15 — Servidor FastAPI — Endpoint y Prueba con cURL

### Endpoint /chat y arranque del servidor

```python
@app.post("/chat")
async def chat(req: ChatRequest):
    sid = req.session_id or str(uuid.uuid4())
    session = await session_service.get_session("demo", req.user_id, sid)
    if not session:
        await session_service.create_session("demo", req.user_id, sid)

    msg = types.Content(role="user", parts=[types.Part(text=req.message)])
    respuesta = ""
    async for evento in runner.run_async(req.user_id, sid, msg):
        if evento.is_final_response():
            respuesta = evento.content.parts[0].text
    return {"response": respuesta, "session_id": sid}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Levantar el servidor

```bash
python main.py
# o con recarga automática en desarrollo:
uvicorn main:app --host 0.0.0.0 --port 8080 --reload
```

### Llamar con cURL

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Saluda a María", "user_id": "demo"}'

# {"response": "¡Hola, María! Soy tu agente.", "session_id": "uuid-xxx"}
```

> Documentación Swagger interactiva disponible en `http://localhost:8080/docs`

---

# SECCIÓN 5: CYBERGUARD — SISTEMA MULTI-AGENTE DE CIBERSEGURIDAD

---

## Slide 16 — La Necesidad: El Problema Actual

Los equipos de seguridad enfrentan retos que superan la capacidad humana individual:

- **Volumen:** Miles de alertas, logs y vulnerabilidades diarias imposibles de revisar una a una.
- **Especialización dispersa:** Un mismo profesional no puede dominar CIS Benchmarks + análisis forense + OSINT + respuesta a incidentes simultáneamente.
- **Velocidad de respuesta:** Los ataques se propagan en minutos; los playbooks manuales tardan horas.
- **Acceso limitado:** El conocimiento especializado en seguridad es caro y escaso para equipos pequeños.

### La oportunidad

```
ANTES (flujo manual)              DESPUÉS (con CyberGuard)
─────────────────────             ──────────────────────────
Alerta de incidente               Alerta de incidente
     │                                  │
     ▼                                  ▼
Analista revisa logs          Agente clasifica en segundos
(30-120 minutos)              (< 30 segundos)
     │                                  │
     ▼                                  ▼
Escala con otro especialista    Delega al sub-agente
(horas / días)                  especializado automáticamente
```

---

## Slide 17 — CyberGuard: Características y Funcionalidades

**CyberGuard** es un sistema multi-agente de ciberseguridad construido sobre Google ADK, con LLM vía OpenRouter y expuesto como API REST con FastAPI.

### Características principales

- **Multi-agente con routing inteligente:** El coordinador delega automáticamente al especialista correcto, sin reglas manuales de enrutado.
- **4 especialistas independientes:** Cada sub-agente tiene su propio contexto, instrucciones y herramientas.
- **Herramientas reales:** DNS lookup, WHOIS, análisis de headers HTTP, verificación de controles CIS en el sistema local.
- **Multi-LLM:** Cada agente puede usar un modelo diferente (optimizar costo vs. calidad por tarea).
- **Conversación contextual:** Sesiones con memoria de historial multi-turno.
- **API REST lista:** Endpoint `/chat` para integración con cualquier sistema, SIEM, o frontend.

### Funcionalidades por dominio

| Dominio | Funcionalidad |
|---------|--------------|
| Hardening | CIS Benchmarks Linux/Windows, checklists, verificación real en el sistema |
| Red | Escaneo de puertos, análisis de servicios expuestos y evaluación de riesgo |
| OSINT | DNS lookup, WHOIS, análisis de headers de seguridad HTTP |
| Incidentes | Clasificación automática, severidad, playbooks Ransomware/Phishing/DDoS/Breach |

---

## Slide 18 — CyberGuard: Alcances del Sistema

### ¿Qué puede hacer CyberGuard?

- Consultar CIS Benchmarks para Linux y Windows (controles Level 1 y Level 2).
- Ejecutar verificaciones de controles CIS directamente en el sistema local (`run_cis_check`).
- Proporcionar checklists de hardening filtrados por categoría (SSH, Firewall, Filesystem...).
- Realizar reconocimiento pasivo de dominios: registros DNS (A, MX, NS, TXT), WHOIS e información de registro.
- Analizar y calificar (A-F) los headers de seguridad HTTP de cualquier sitio web.
- Escanear puertos de un host y evaluar el riesgo de cada servicio expuesto.
- Clasificar incidentes de seguridad (ransomware, phishing, data breach, DDoS) y determinar su severidad.
- Entregar playbooks de respuesta completos organizados por fase: acciones inmediatas, contención, recuperación y post-incidente.
- Mantener memoria de conversación multi-turno por sesión de usuario.
- Extenderse sin modificar el coordinador: nuevos agentes y tools se agregan de forma modular.

> **CyberGuard** no reemplaza al analista; **amplifica sus capacidades** y le da velocidad de respuesta.

---

## Slide 19 — CyberGuard: Limitaciones y Roadmap

### Limitaciones actuales (Proof of Concept)

- El escaneo de puertos es **simulado** — no ejecuta nmap real; los resultados son ilustrativos.
- La base de CIS Benchmarks es **parcial** — subset representativo, no el catálogo completo CIS.
- Las sesiones son **en memoria** (`InMemorySessionService`) — se pierden al reiniciar el servidor.
- **Sin autenticación** en los endpoints — se debe agregar antes de exponer en producción.
- Requiere conexión a internet para consultas DNS/WHOIS y para llamar al LLM vía OpenRouter.

### Roadmap de extensión natural

```
v1 — PoC (actual)       v2 — Producción           v3 — Avanzado
─────────────────        ──────────────────────     ──────────────────────
Simulación puertos   →   nmap real (python-nmap) →  CVE lookup en NVD/OSV
CIS parcial          →   CIS completo (JSON/API)  →  Remediación automática
InMemory session     →   PostgreSQL session        →  Embeddings + RAG
Sin auth             →   API Key + OAuth2          →  RBAC por rol
1 LLM global         →   LLM por agente (mixto)   →  Fine-tuned domain model
```

---

## Slide 20 — Arquitectura del Sistema — Diagrama

```
┌─────────────────────────────────────────────────────────────┐
│               Cliente (cURL / App / SIEM)                   │
│             POST /chat  {"message": "..."}                  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│                   FastAPI Server :8080                       │
│          Runner  ←→  InMemorySessionService                  │
└────────────────────────────┬────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────┐
│           cyberguard_coordinator  (root_agent)               │
│       LLM analiza consulta → delega al especialista          │
└─────────┬─────────────┬──────────────┬──────────┬───────────┘
          │             │              │          │
┌─────────▼────┐ ┌──────▼──────┐ ┌────▼──────┐ ┌─▼─────────────┐
│cis_benchmark │ │port_scanner │ │ incident  │ │recon_specialist│
│   _advisor   │ │             │ │_responder │ │               │
│              │ │             │ │           │ │               │
│ check_cis    │ │ scan_ports  │ │ classify  │ │ dns_lookup    │
│ get_hardening│ │             │ │ _incident │ │ whois_lookup  │
│ run_cis_check│ │             │ │ get_play  │ │ check_http    │
│              │ │             │ │ book      │ │ _headers      │
└──────────────┘ └─────────────┘ └───────────┘ └───────────────┘
                             │
             LLM: Gemini 2.5 Flash vía OpenRouter (LiteLLM)
```

---

## Slide 21 — Arquitectura del Sistema — Estructura de Archivos

```
cyberguard_agents/
├── __init__.py                      # Exporta root_agent
├── agent.py                         # Coordinator (root_agent)
│
├── cis_advisor/
│   ├── __init__.py                  # from .agent import cis_agent
│   └── agent.py                     # cis_benchmark_advisor
│
├── port_scanner/
│   ├── __init__.py
│   └── agent.py                     # port_scanner_agent
│
├── incident_responder/
│   ├── __init__.py
│   └── agent.py                     # incident_responder_agent
│
├── recon/
│   ├── __init__.py
│   └── agent.py                     # recon_specialist
│
└── tools/
    ├── cis_tools.py        # check_cis_benchmark, get_hardening_checklist, run_cis_check
    ├── scanner_tools.py    # scan_ports
    ├── incident_tools.py   # classify_incident, get_incident_playbook
    └── recon_tools.py      # dns_lookup, whois_lookup, check_http_headers
```

```
proyecto/
├── .env                    # API keys (nunca al repo)
├── .env.example            # plantilla pública
├── requirements.txt        # google-adk[extensions], fastapi, uvicorn...
├── main.py                 # FastAPI server
├── cyberguard_agents/      # paquete ADK (arriba)
└── tests/
    └── test_agents.py      # pruebas básicas con Runner
```

---

## Slide 22 — Los 4 Sub-Agentes — Coordinador y Especialistas

### Coordinador — `cyberguard_coordinator`

El LLM del coordinador lee las `description` de cada sub-agente y decide a quién delegar. No hay reglas manuales de enrutado.

```python
root_agent = LlmAgent(
    name="cyberguard_coordinator",
    model=MODEL,
    instruction="Eres CyberGuard, un coordinador de ciberseguridad...",
    sub_agents=[
        cis_agent,
        port_scanner_agent,
        incident_responder_agent,
        recon_agent,
    ],
)
```

### Los 4 especialistas

| Sub-agente | Trigger típico | Tools disponibles |
|------------|---------------|-------------------|
| `cis_benchmark_advisor` | "¿Controles SSH de Linux?" | `check_cis_benchmark`, `get_hardening_checklist`, `run_cis_check` |
| `port_scanner` | "Escanea los puertos de 192.168.1.1" | `scan_ports` |
| `incident_responder` | "Tenemos archivos cifrados en el servidor" | `classify_incident`, `get_incident_playbook` |
| `recon_specialist` | "Investiga el dominio ejemplo.com" | `dns_lookup`, `whois_lookup`, `check_http_headers` |

---

## Slide 23 — Los 4 Sub-Agentes — Flujo de Delegación

### ¿Cómo decide el coordinador a quién delegar?

El LLM compara el mensaje del usuario con la `description` de cada sub-agente:

```
cis_agent.description =
  "Especialista en CIS Benchmarks para Linux y Windows.
   Consulta controles específicos, proporciona checklists de hardening..."

port_scanner_agent.description =
  "Especialista en escaneo y análisis de puertos de red.
   Escanea hosts, identifica servicios expuestos y evalúa riesgos..."

incident_responder_agent.description =
  "Especialista en respuesta a incidentes de ciberseguridad.
   Clasifica incidentes (ransomware, phishing, data breach, DDoS)..."

recon_agent.description =
  "Especialista en reconocimiento y recopilación de información (OSINT).
   Realiza consultas DNS, WHOIS y análisis de headers HTTP..."
```

### Ejemplo de delegación completa

```
Usuario: "Tenemos archivos cifrados y una nota de rescate"
    │
    ▼  Coordinator lee descriptions → match: incident_responder
    │
    ▼  classify_incident("archivos cifrados, nota de rescate")
       → incident_type: "ransomware", severity: "CRITICAL"
    │
    ▼  get_incident_playbook("ransomware", "all")
       → 4 fases: acciones inmediatas / contención / recuperación / post
    │
    ▼  Respuesta al usuario con playbook completo y pasos priorizados
```

---

## Slide 24 — Las Tools — Anatomía de una Tool

Las tools son funciones Python normales. ADK usa el **docstring** y los **type hints** para que el LLM sepa cuándo y cómo invocarlas. **Deben retornar un `dict`.**

### Anatomía de una tool bien definida

```python
def dns_lookup(domain: str) -> dict:
    """
    Realiza consultas DNS para un dominio (registros A, MX, NS, TXT).

    Usa esta herramienta cuando el usuario quiera obtener información
    DNS de un dominio, verificar registros MX o buscar registros SPF/DKIM.

    Args:
        domain: El dominio a consultar (ejemplo: 'example.com').

    Returns:
        dict: Registros DNS organizados por tipo.
    """
    # ... lógica real con dnspython ...
    return {
        "status": "success",
        "domain": domain,
        "records": {"A": ["93.184.216.34"], "MX": [...], "NS": [...], "TXT": [...]}
    }
```

### Reglas de diseño de tools

| Hacer | Evitar |
|-------|--------|
| Docstring claro con cuándo usarla | Docstrings vacíos o vagos |
| Type hints en todos los parámetros | Parámetros sin tipo (`x`, `y`) |
| Retornar siempre un `dict` | Retornar strings o None |
| Incluir `status: success/error` | Lanzar excepciones sin capturar |

> **Regla de oro:** La calidad del docstring determina la calidad del uso que el LLM hace de la tool.

---

## Slide 25 — Las Tools — Catálogo por Agente

```
cis_tools.py  (CIS Benchmark Advisor)
  ├── check_cis_benchmark(os_type, benchmark_id)
  │     → Detalles de un control CIS: título, nivel, remediación, comando de check
  │
  ├── get_hardening_checklist(os_type, category)
  │     → Lista de controles filtrados por OS y categoría
  │
  └── run_cis_check(os_type, benchmark_id)
        → Ejecuta el comando de verificación REAL en el sistema local

scanner_tools.py  (Port Scanner)
  └── scan_ports(target, port_range)
        → Análisis de puertos con evaluación de riesgo (critical/high/medium/low)

incident_tools.py  (Incident Responder)
  ├── classify_incident(description)
  │     → Clasifica el incidente: tipo + severidad (critical/high/medium)
  │
  └── get_incident_playbook(incident_type, phase)
        → Playbook por fases: immediate_actions / containment / recovery / post_incident

recon_tools.py  (Recon Specialist)
  ├── dns_lookup(domain)
  │     → Registros A, MX, NS, TXT usando dnspython (real)
  │
  ├── whois_lookup(target)
  │     → Registrante, fechas, name servers usando python-whois (real)
  │
  └── check_http_headers(url)
        → Análisis de 7 headers de seguridad con puntuación A-F (httpx)
```

---

# SECCIÓN 6: PRUEBA DE CONCEPTO Y CONCLUSIONES

---

## Slide 26 — Prueba de Concepto — Setup y Escenarios 1-2

### Preparar y levantar el sistema

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar clave en .env
echo "OPENROUTER_API_KEY=sk-or-v1-..." > .env

# 3a. Opción FastAPI (endpoint productivo)
python main.py            # → http://localhost:8080/docs

# 3b. Opción ADK Web UI (interfaz de desarrollo visual)
adk web                   # → http://localhost:8000
```

### Escenario 1 — CIS Benchmark advisor

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuáles son los controles CIS de SSH para Linux?",
       "user_id": "demo"}'
```

### Escenario 2 — Port Scanner

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Escanea los puertos del servidor 192.168.1.100",
       "user_id": "demo"}'
```

---

## Slide 27 — Prueba de Concepto — Escenarios 3-4 y Verificación

### Escenario 3 — Incident Responder (ransomware)

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tenemos archivos cifrados en producción y apareció una nota de rescate",
       "user_id": "demo"}'
```

### Escenario 4 — Recon Specialist (OSINT)

```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Investiga el dominio example.com: DNS, WHOIS y headers de seguridad",
       "user_id": "demo"}'
```

### Verificar agentes registrados

```bash
curl http://localhost:8080/agents
# {"agents": [{"name": "cyberguard_coordinator", "role": "coordinator",
#              "sub_agents": ["cis_benchmark_advisor", "port_scanner",
#                             "incident_responder", "recon_specialist"]}, ...]}
```

### Continuidad de sesión (memoria multi-turno)

```bash
# Reutilizar session_id de una respuesta anterior para mantener contexto
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Muéstrame ahora el checklist completo de Linux",
       "user_id": "demo",
       "session_id": "UUID-DE-LA-SESION-ANTERIOR"}'
```

---

## Slide 28 — Conclusiones — Lo que Aprendimos

1. **Los agentes de IA extienden los LLM** con la capacidad de actuar, no solo responder. El patrón ReAct (Reason-Act-Observe) permite resolver tareas complejas de forma iterativa.

2. **Google ADK democratiza la construcción de agentes** con un enfoque code-first, multi-agente nativo y FastAPI integrado. Menor curva de aprendizaje versus LangChain.

3. **LiteLLM + OpenRouter rompen el vendor lock-in:** un mismo código puede usar Gemini, Claude, GPT-4 u Ollama cambiando solo una línea de configuración.

4. **FastAPI es el stack natural** para exponer agentes como microservicios: async nativo compatible con ADK, validación Pydantic, Swagger automático sin configuración extra.

5. **El routing por LLM es poderoso:** no hay que programar reglas de enrutado; el coordinador decide qué especialista activar leyendo las `description` de cada sub-agente.

6. **CyberGuard demuestra** que dominios especializados (ciberseguridad, medicina, legal) se benefician enormemente de agentes con tools de dominio y system prompts especializados.

---

## Slide 29 — Conclusiones — Takeaways Prácticos

### Lecciones de implementación

- **Docstrings claros = tool calls correctos.** El LLM decide cuándo y cómo invocar una tool basándose únicamente en su docstring y type hints.
- **`description` específica = routing preciso.** Una descripción vaga en el sub-agente genera delegaciones incorrectas del coordinador.
- **Empieza con `InMemorySessionService`**, migra a `DatabaseSessionService` (SQLite / PostgreSQL) cuando necesites persistencia entre reinicios.
- **Cada agente puede tener un modelo distinto:** coordinador con un modelo económico, especialistas con modelos de mayor calidad cuando la tarea lo requiera.
- **El sistema es modular:** agregar un nuevo especialista solo requiere crear el módulo y añadirlo al array `sub_agents` del coordinador. Sin modificar ningún otro agente.
- **`adk web` es tu mejor aliado de depuración:** muestra en tiempo real qué tool fue llamada, con qué argumentos, y qué agente respondió.

### El stack mínimo para producir valor

```
google-adk[litellm] + python-dotenv   →  agente funcionando en < 1 hora
+ fastapi + uvicorn                   →  API REST en < 30 minutos más
+ tools de dominio + system prompt    →  especialista vertical listo para usar
```

---

## Slide 30 — Referencias y Recursos

### Google ADK

- **Documentación oficial:** [google.github.io/adk-docs](https://google.github.io/adk-docs/)
- **Repositorio Python:** [github.com/google/adk-python](https://github.com/google/adk-python)
- **Ejemplos oficiales:** [github.com/google/adk-samples](https://github.com/google/adk-samples)

### LLMs y proveedores

- **LiteLLM (proveedores soportados):** [docs.litellm.ai/docs/providers](https://docs.litellm.ai/docs/providers)
- **OpenRouter (modelos y precios):** [openrouter.ai/models](https://openrouter.ai/models)
- **Google AI Studio (Gemini API keys):** [aistudio.google.com](https://aistudio.google.com)
- **Ollama (modelos locales):** [ollama.ai](https://ollama.ai)

### Frameworks web

- **FastAPI:** [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- **Pydantic v2:** [docs.pydantic.dev](https://docs.pydantic.dev)

### Ciberseguridad

- **CIS Benchmarks:** [cisecurity.org/cis-benchmarks](https://www.cisecurity.org/cis-benchmarks)
- **NIST Cybersecurity Framework:** [nist.gov/cyberframework](https://www.nist.gov/cyberframework)
- **MITRE ATT&CK:** [attack.mitre.org](https://attack.mitre.org)
- **OWASP Top 10:** [owasp.org/www-project-top-ten](https://owasp.org/www-project-top-ten)

### Dependencias del proyecto

```
google-adk[extensions]   fastapi          uvicorn[standard]
python-dotenv            dnspython        python-whois
httpx                    python-nmap
```

---

> **</Qu@ntum>** · Sistema CyberGuard Multi-Agent
> Google ADK · OpenRouter · LiteLLM · FastAPI · Python 3.10+

# CyberGuard — Multi-Agent Cybersecurity System
<div align="right"><sub>by <strong>&lt;/Qu@ntum&gt;</strong></sub></div>

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Google ADK](https://img.shields.io/badge/Google%20ADK-latest-orange?logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-green?logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

Sistema de agentes especializados en ciberseguridad construido con **[Google ADK](https://google.github.io/adk-docs/)** (Agent Development Kit) y **FastAPI**.

Cada agente dispone de herramientas reales: escaneo de puertos con nmap, consultas DNS/WHOIS, análisis de headers HTTP, verificación de controles CIS y playbooks de respuesta a incidentes.

> **Aviso ético:** Este sistema es para uso autorizado en entornos propios o con permiso explícito. Usar herramientas de escaneo contra sistemas ajenos sin autorización puede ser ilegal.

---

## Arquitectura

```
Usuario  ──► POST /chat (FastAPI)
                 │
         CyberGuard Coordinator
                 │
    ┌────────────┼────────────┐────────────┐
    ▼            ▼            ▼            ▼
cis_benchmark  port_scanner  recon_      incident_
_advisor                    specialist   responder
    │            │            │            │
check_cis_     scan_ports   dns_lookup   classify_
benchmark      scan_vulns   whois_lookup  incident
get_hardening              check_http_  get_playbook
_checklist                 headers
run_cis_check
```

### Agentes

| Agente | Descripción | Herramientas |
|--------|-------------|--------------|
| `cyberguard_coordinator` | Coordinador principal — enruta al agente correcto | — |
| `cis_benchmark_advisor` | Controles CIS para Linux/Windows con verificación real | `check_cis_benchmark`, `get_hardening_checklist`, `run_cis_check` |
| `port_scanner` | Escaneo nmap, detección de versiones y vulnerabilidades NSE | `scan_ports`, `scan_vulnerabilities` |
| `recon_specialist` | Reconocimiento OSINT: DNS, WHOIS, headers HTTP | `dns_lookup`, `whois_lookup`, `check_http_headers` |
| `incident_responder` | Clasificación de incidentes y playbooks de respuesta | `classify_incident`, `get_incident_playbook` |

---

## Requisitos

- **Python 3.10+**
- **[nmap](https://nmap.org/download.html)** instalado en el sistema (opcional — sin él, las herramientas de escaneo devuelven un error descriptivo en lugar de crashear)
- **API Key de [OpenRouter](https://openrouter.ai/)** para acceder a Gemini 2.5 Flash

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/QuantumEdu/AgentCyber.git
cd AgentCyber

# 2. Crear entorno virtual e instalar dependencias
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
# .venv\Scripts\activate    # Windows

pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env
# Edita .env y agrega tu OPENROUTER_API_KEY
```

### Instalar nmap

```bash
# Linux
sudo apt install nmap

# macOS
brew install nmap

# Windows
# Descarga el instalador desde https://nmap.org/download.html
```

---

## Iniciar el servidor

```bash
python main.py
```

El servidor arranca en `http://localhost:8080`.
Documentación interactiva Swagger UI en:

```
http://localhost:8080/docs
```

---

## Uso

### Endpoint principal: `POST /chat`

```json
{
  "message": "tu pregunta o instrucción aquí",
  "user_id": "default_user",
  "session_id": null
}
```

| Campo | Descripción |
|-------|-------------|
| `message` | Consulta de ciberseguridad (ver ejemplos abajo) |
| `user_id` | Identificador del usuario. Agrupa sesiones. |
| `session_id` | `null` para nueva conversación. Reusar el valor devuelto para mantener contexto. |

**Respuesta:**

```json
{
  "response": "Resultado del agente...",
  "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "agent_name": "port_scanner"
}
```

---

## Ejemplos de uso

### Escaneo de puertos

```json
{ "message": "Escanea los puertos de scanme.nmap.org" }
```

### Detección de vulnerabilidades

```json
{ "message": "Busca vulnerabilidades en scanme.nmap.org en los puertos 22 y 80" }
```

### Reconocimiento DNS

```json
{ "message": "Haz una consulta DNS completa de example.com" }
```

### Información WHOIS

```json
{ "message": "Dame la información WHOIS de github.com" }
```

### Análisis de headers HTTP

```json
{ "message": "Analiza los headers de seguridad de https://google.com" }
```

### Controles CIS

```json
{ "message": "¿Cuáles son los controles CIS de SSH para Linux?" }
```

```json
{ "message": "Verifica si el control CIS 9.1.1 de Windows Firewall se cumple en este sistema" }
```

### Respuesta a incidentes

```json
{ "message": "Varios archivos del servidor aparecieron cifrados con extensión .locked y hay una nota pidiendo Bitcoin" }
```

```json
{ "message": "Un empleado hizo clic en un enlace sospechoso e ingresó sus credenciales" }
```

### Consultas generales

```json
{ "message": "¿Qué es el principio de mínimo privilegio?" }
```

---

## Endpoints REST

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/` | Health check e info del servicio |
| `POST` | `/chat` | Chat principal con el sistema multi-agente |
| `GET` | `/agents` | Lista todos los agentes y sus herramientas |
| `DELETE` | `/sessions/{user_id}/{session_id}` | Elimina una sesión de conversación |
| `GET` | `/docs` | Documentación interactiva Swagger UI |

---

## Configuración

Copia `.env.example` a `.env` y completa los valores:

```env
GOOGLE_GENAI_USE_VERTEXAI=0
GOOGLE_API_KEY=your-google-api-key-here
OPENROUTER_API_KEY=sk-or-v1-your-openrouter-key-here
```

- **`OPENROUTER_API_KEY`** — Requerida. Obtén la tuya en [openrouter.ai/keys](https://openrouter.ai/keys).
- **`GOOGLE_API_KEY`** — Opcional si ya usas OpenRouter.

---

## Notas de producción

- Las **sesiones se almacenan en memoria** y se pierden al reiniciar el servidor. Para producción, usa un servicio de sesiones persistente (Redis, base de datos).
- **No hay autenticación** en la API por defecto. Para exponer públicamente, implementa autenticación (API key, JWT, OAuth2) y restringe el CORS.
- Los controles **CIS solo se ejecutan en el sistema local** y solo si el OS coincide (no ejecuta comandos Linux en Windows ni viceversa).

---

## Estructura del proyecto

```
cyberguard_agents/
├── agent.py                    # Coordinador principal
├── cis_advisor/agent.py        # Agente CIS Benchmarks
├── port_scanner/agent.py       # Agente de escaneo
├── recon/agent.py              # Agente de reconocimiento
├── incident_responder/agent.py # Agente de respuesta a incidentes
└── tools/
    ├── cis_tools.py
    ├── scanner_tools.py
    ├── recon_tools.py
    └── incident_tools.py
main.py                         # Servidor FastAPI
requirements.txt
.env.example                    # Plantilla de configuración
Google_Agent_Dev.md             # Tutorial completo de Google ADK
```

---

## Stack tecnológico

| Componente | Tecnología |
|------------|------------|
| Framework de agentes | [Google ADK](https://google.github.io/adk-docs/) |
| API REST | [FastAPI](https://fastapi.tiangolo.com/) |
| Servidor ASGI | [Uvicorn](https://www.uvicorn.org/) |
| LLM | Google Gemini 2.5 Flash (via OpenRouter) |
| Escaneo de puertos | [nmap](https://nmap.org/) / [python-nmap](https://pypi.org/project/python-nmap/) |
| DNS | [dnspython](https://www.dnspython.org/) |
| WHOIS | [python-whois](https://pypi.org/project/python-whois/) |

---

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Realiza tus cambios y haz commit: `git commit -m "feat: descripción"`
4. Envía tu rama: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

---

## Licencia

MIT © [QuantumEdu](https://github.com/QuantumEdu)

---

<div align="center">
  <sub>Powered by <strong>&lt;/Qu@ntum&gt;</strong></sub>
</div>

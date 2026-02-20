# 🛡️ Tutorial Práctico: Google Agent Development Kit (ADK)
## Agente de Ciberseguridad con OpenRouter + FastAPI

> **Nivel:** Básico-Intermedio | **Tiempo estimado:** 60-90 minutos  
> **Resultado:** Un sistema multi-agente de ciberseguridad funcional con API REST

---

## 📋 Tabla de Contenidos

1. [¿Qué es Google ADK?](#1-qué-es-google-adk)
2. [Arquitectura del Proyecto](#2-arquitectura-del-proyecto)
3. [Configuración del Entorno](#3-configuración-del-entorno)
4. [Paso 1: Agente Básico — CIS Benchmark Advisor](#4-paso-1-agente-básico--cis-benchmark-advisor)
5. [Paso 2: Herramientas (Tools) Personalizadas](#5-paso-2-herramientas-tools-personalizadas)
6. [Paso 3: Sistema Multi-Agente](#6-paso-3-sistema-multi-agente)
7. [Paso 4: Integración con FastAPI](#7-paso-4-integración-con-fastapi)
8. [Paso 5: Ejecución y Pruebas](#8-paso-5-ejecución-y-pruebas)
9. [Conceptos Clave de ADK](#9-conceptos-clave-de-adk)
10. [Troubleshooting y Tips](#10-troubleshooting-y-tips)
11. [Próximos Pasos](#11-próximos-pasos)

---

## 1. ¿Qué es Google ADK?

**Agent Development Kit (ADK)** es un framework open-source de Google para construir agentes de IA. Piensa en él como el "Django de los agentes": te da estructura, herramientas y patrones para crear sistemas agenticos de manera profesional.

### Características principales

- **Code-First:** Todo se define en Python, sin YAML ni configuraciones mágicas.
- **Model-Agnostic:** Funciona con Gemini, pero también con cualquier LLM vía LiteLLM (OpenRouter, Ollama, OpenAI, Anthropic, etc.).
- **Multi-Agente por diseño:** Compone agentes especializados en jerarquías (coordinador → sub-agentes).
- **Tools integrados:** Funciones Python normales se convierten en herramientas del agente.
- **Session & State:** Gestión de conversaciones y estado entre turnos.
- **FastAPI nativo:** Incluye `get_fast_api_app()` para exponer agentes como API REST.

### ¿Por qué ADK y no LangChain/CrewAI?

| Aspecto | ADK | LangChain | CrewAI |
|---------|-----|-----------|--------|
| Enfoque | Software engineering | Chaining | Role-playing |
| Complejidad | Baja | Alta | Media |
| Multi-agente | Nativo (jerárquico) | Requiere LangGraph | Nativo (secuencial) |
| Deployment | FastAPI integrado | Manual | Manual |
| Model flexibility | LiteLLM built-in | Sí | Limitado |

---

## 2. Arquitectura del Proyecto

Vamos a construir **CyberGuard** — un sistema multi-agente de ciberseguridad que:

```
┌─────────────────────────────────────────────────┐
│                  FastAPI Server                  │
│                 (localhost:8080)                 │
├─────────────────────────────────────────────────┤
│                                                 │
│   ┌─────────────────────────────────────────┐   │
│   │        🎯 Coordinator Agent             │   │
│   │   (Orquesta y delega al sub-agente      │   │
│   │    correcto según la consulta)          │   │
│   └─────────┬──────────┬──────────┬─────────┘   │
│             │          │          │              │
│   ┌─────────▼──┐ ┌─────▼────┐ ┌──▼──────────┐  │
│   │ CIS Bench  │ │ Port     │ │ Incident    │  │
│   │ Advisor    │ │ Scanner  │ │ Responder   │  │
│   │ Agent      │ │ Agent    │ │ Agent       │  │
│   └─────┬──────┘ └────┬─────┘ └──────┬──────┘  │
│         │              │              │          │
│   ┌─────▼──────┐ ┌────▼─────┐ ┌──────▼──────┐  │
│   │ Tools:     │ │ Tools:   │ │ Tools:      │  │
│   │ • check_   │ │ • scan_  │ │ • classify_ │  │
│   │   benchmark│ │   ports  │ │   incident  │  │
│   │ • get_     │ │          │ │ • get_      │  │
│   │   hardening│ │          │ │   playbook  │  │
│   └────────────┘ └──────────┘ └─────────────┘  │
│                                                 │
│   LLM: OpenRouter (vía LiteLLM)                │
└─────────────────────────────────────────────────┘
```

### Estructura de archivos

```
cyberguard/
├── .env                          # API keys
├── requirements.txt              # Dependencias
├── main.py                       # FastAPI server + endpoints custom
│
├── cyberguard_agents/            # Directorio de agentes ADK
│   ├── __init__.py               # Exporta root_agent
│   ├── agent.py                  # Coordinator (root_agent)
│   │
│   ├── cis_advisor/              # Sub-agente CIS Benchmarks
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── port_scanner/             # Sub-agente Scanner
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── incident_responder/       # Sub-agente Respuesta a Incidentes
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   └── tools/                    # Herramientas compartidas
│       ├── __init__.py
│       ├── cis_tools.py
│       ├── scanner_tools.py
│       └── incident_tools.py
│
└── tests/
    └── test_agents.py            # Tests básicos
```

---

## 3. Configuración del Entorno

### 3.1 Requisitos previos

- Python 3.10+ instalado
- Cuenta en [OpenRouter](https://openrouter.ai/) (tienen modelos gratuitos para pruebas)
- Terminal / VS Code

### 3.2 Crear el proyecto

```bash
# Crear directorio del proyecto
mkdir cyberguard && cd cyberguard

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# Linux/Mac:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
```

### 3.3 Instalar dependencias

```bash
# Crear requirements.txt
cat > requirements.txt << 'EOF'
google-adk[litellm]
fastapi
uvicorn[standard]
python-dotenv
httpx
EOF

# Instalar
pip install -r requirements.txt
```

> **Nota:** `google-adk[litellm]` instala ADK + la integración con LiteLLM que necesitamos para OpenRouter.

### 3.4 Configurar API Key

```bash
# Crear archivo .env
cat > .env << 'EOF'
OPENROUTER_API_KEY=sk-or-v1-TU_API_KEY_AQUI
EOF
```

Para obtener tu API key:
1. Ve a [openrouter.ai/keys](https://openrouter.ai/keys)
2. Crea una nueva key
3. Copia y pega en el `.env`

> **Tip:** OpenRouter ofrece modelos gratuitos como `google/gemma-2-9b-it:free` para pruebas. Para producción puedes usar `google/gemini-2.5-flash`, `anthropic/claude-sonnet-4`, `openai/gpt-4o-mini`, etc.

---

## 4. Paso 1: Agente Básico — CIS Benchmark Advisor

Empecemos con un solo agente para entender los conceptos fundamentales de ADK.

### 4.1 Conceptos ADK que vamos a usar

- **`LlmAgent`**: Un agente potenciado por un LLM. Es la unidad básica.
- **`LiteLlm`**: Wrapper que conecta ADK con cualquier proveedor vía LiteLLM.
- **`tools`**: Lista de funciones Python que el agente puede invocar.
- **`instruction`**: El system prompt del agente.
- **`description`**: Cómo otros agentes entienden qué hace este agente (crucial en multi-agente).

### 4.2 Crear las tools del CIS Advisor

```bash
# Crear estructura de directorios
mkdir -p cyberguard_agents/tools
```

Crea el archivo `cyberguard_agents/tools/__init__.py`:

```python
# cyberguard_agents/tools/__init__.py
# Paquete de herramientas
```

Ahora crea `cyberguard_agents/tools/cis_tools.py`:

```python
"""
Herramientas para consulta de CIS Benchmarks.

CONCEPTO ADK: Las tools son funciones Python normales. ADK usa el docstring
y los type hints para que el LLM entienda CUÁNDO y CÓMO usar cada tool.
Las tools DEBEN retornar un diccionario.
"""


# Base de conocimiento simplificada de CIS Benchmarks
# En producción, esto sería una base de datos o API externa
CIS_BENCHMARKS = {
    "linux": {
        "1.1.1": {
            "title": "Ensure mounting of cramfs filesystems is disabled",
            "level": 1,
            "description": "The cramfs filesystem type is a compressed read-only Linux filesystem.",
            "remediation": "Edit /etc/modprobe.d/cramfs.conf and add: install cramfs /bin/true\n"
                           "Run: rmmod cramfs",
            "check_command": "modprobe -n -v cramfs | grep -E '(cramfs|install)'",
            "category": "Filesystem Configuration"
        },
        "1.1.2": {
            "title": "Ensure /tmp is configured",
            "level": 1,
            "description": "The /tmp directory is used for temporary file storage.",
            "remediation": "Configure /tmp as a separate partition in /etc/fstab:\n"
                           "tmpfs /tmp tmpfs defaults,rw,nosuid,nodev,noexec,relatime 0 0",
            "check_command": "findmnt -n /tmp",
            "category": "Filesystem Configuration"
        },
        "5.2.1": {
            "title": "Ensure permissions on /etc/ssh/sshd_config are configured",
            "level": 1,
            "description": "The /etc/ssh/sshd_config file contains configuration for the SSH daemon.",
            "remediation": "Run: chown root:root /etc/ssh/sshd_config\n"
                           "Run: chmod og-rwx /etc/ssh/sshd_config",
            "check_command": "stat /etc/ssh/sshd_config",
            "category": "SSH Configuration"
        },
        "5.2.4": {
            "title": "Ensure SSH Protocol is set to 2",
            "level": 1,
            "description": "SSH supports two protocols. Protocol 1 has known vulnerabilities.",
            "remediation": "Edit /etc/ssh/sshd_config: Protocol 2\n"
                           "Restart sshd: systemctl restart sshd",
            "check_command": "grep '^Protocol' /etc/ssh/sshd_config",
            "category": "SSH Configuration"
        },
        "5.2.8": {
            "title": "Ensure SSH root login is disabled",
            "level": 1,
            "description": "Disabling root login forces system admins to authenticate with their own credentials.",
            "remediation": "Edit /etc/ssh/sshd_config: PermitRootLogin no\n"
                           "Restart sshd: systemctl restart sshd",
            "check_command": "grep '^PermitRootLogin' /etc/ssh/sshd_config",
            "category": "SSH Configuration"
        },
        "4.2.1": {
            "title": "Ensure firewall is installed",
            "level": 1,
            "description": "A firewall utility is required to configure the host-based firewall rules.",
            "remediation": "Install UFW: apt install ufw\nEnable: ufw enable",
            "check_command": "dpkg -s ufw | grep Status",
            "category": "Firewall Configuration"
        },
    },
    "windows": {
        "1.1.1": {
            "title": "Ensure 'Enforce password history' is set to 24 or more",
            "level": 1,
            "description": "Determines the number of unique new passwords before an old password can be reused.",
            "remediation": "Computer Configuration > Policies > Windows Settings > Security Settings >\n"
                           "Account Policies > Password Policy > Enforce password history = 24",
            "check_command": "net accounts | findstr /i 'password history'",
            "category": "Account Policies"
        },
        "2.3.1": {
            "title": "Ensure 'Accounts: Administrator account status' is set to Disabled",
            "level": 1,
            "description": "The built-in Administrator account should be disabled in normal use.",
            "remediation": "Computer Configuration > Windows Settings > Security Settings >\n"
                           "Local Policies > Security Options > Accounts: Administrator account status = Disabled",
            "check_command": "net user administrator | findstr /i 'Account active'",
            "category": "Security Options"
        },
        "9.1.1": {
            "title": "Ensure 'Windows Firewall: Domain: Firewall state' is set to On",
            "level": 1,
            "description": "The Windows Firewall should be enabled on domain networks.",
            "remediation": "Computer Configuration > Windows Settings > Security Settings >\n"
                           "Windows Defender Firewall > Domain Profile > Firewall state = On",
            "check_command": "netsh advfirewall show domainprofile state",
            "category": "Firewall Configuration"
        },
    }
}


def check_cis_benchmark(os_type: str, benchmark_id: str) -> dict:
    """
    Consulta un control específico de CIS Benchmark por su ID.

    Usa esta herramienta cuando el usuario pregunte por un control CIS específico,
    quiera saber los detalles de un benchmark, o necesite el comando de verificación.

    Args:
        os_type: Sistema operativo. Puede ser 'linux' o 'windows'.
        benchmark_id: El identificador del benchmark CIS (ejemplo: '5.2.1', '1.1.1').

    Returns:
        dict: Información del benchmark o mensaje de error.
    """
    os_type = os_type.lower().strip()

    if os_type not in CIS_BENCHMARKS:
        return {
            "status": "error",
            "message": f"OS '{os_type}' no soportado. Opciones: linux, windows"
        }

    benchmarks = CIS_BENCHMARKS[os_type]
    benchmark_id = benchmark_id.strip()

    if benchmark_id not in benchmarks:
        available = ", ".join(benchmarks.keys())
        return {
            "status": "error",
            "message": f"Benchmark '{benchmark_id}' no encontrado para {os_type}. "
                       f"Disponibles: {available}"
        }

    bm = benchmarks[benchmark_id]
    return {
        "status": "success",
        "os": os_type,
        "id": benchmark_id,
        "title": bm["title"],
        "level": bm["level"],
        "category": bm["category"],
        "description": bm["description"],
        "remediation": bm["remediation"],
        "check_command": bm["check_command"]
    }


def get_hardening_checklist(os_type: str, category: str = "all") -> dict:
    """
    Obtiene una lista de controles de hardening para un sistema operativo,
    opcionalmente filtrada por categoría.

    Usa esta herramienta cuando el usuario pida una lista de controles de seguridad,
    un checklist de hardening, o quiera ver todos los benchmarks de una categoría.

    Args:
        os_type: Sistema operativo. Puede ser 'linux' o 'windows'.
        category: Categoría a filtrar. Puede ser 'all', 'SSH Configuration',
                  'Filesystem Configuration', 'Firewall Configuration',
                  'Account Policies', 'Security Options'.

    Returns:
        dict: Lista de controles o mensaje de error.
    """
    os_type = os_type.lower().strip()

    if os_type not in CIS_BENCHMARKS:
        return {
            "status": "error",
            "message": f"OS '{os_type}' no soportado. Opciones: linux, windows"
        }

    benchmarks = CIS_BENCHMARKS[os_type]
    results = []

    for bm_id, bm in benchmarks.items():
        if category.lower() == "all" or bm["category"].lower() == category.lower():
            results.append({
                "id": bm_id,
                "title": bm["title"],
                "level": bm["level"],
                "category": bm["category"]
            })

    if not results:
        categories = set(bm["category"] for bm in benchmarks.values())
        return {
            "status": "error",
            "message": f"Categoría '{category}' no encontrada. "
                       f"Disponibles: {', '.join(categories)}"
        }

    return {
        "status": "success",
        "os": os_type,
        "filter": category,
        "total_controls": len(results),
        "controls": results
    }
```

### 4.3 Crear el agente CIS Advisor

Crea `cyberguard_agents/cis_advisor/__init__.py`:

```python
from .agent import cis_agent
```

Crea `cyberguard_agents/cis_advisor/agent.py`:

```python
"""
CIS Benchmark Advisor Agent.

CONCEPTO ADK — LlmAgent:
- `name`: Identificador único (sin espacios). Usado internamente por ADK.
- `model`: El LLM que usa. Con LiteLlm() podemos usar OpenRouter.
- `instruction`: System prompt. Define CÓMO debe comportarse el agente.
- `description`: Describe QUÉ hace. Crucial en multi-agente porque el
                 coordinador lee esto para decidir a quién delegar.
- `tools`: Lista de funciones Python que el agente puede invocar.
"""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.cis_tools import (
    check_cis_benchmark,
    get_hardening_checklist,
)

# ──────────────────────────────────────────────
# Configuración del modelo vía OpenRouter
# ──────────────────────────────────────────────
# Formato: "openrouter/<provider>/<model>"
# Ejemplos:
#   "openrouter/google/gemini-2.5-flash"
#   "openrouter/anthropic/claude-sonnet-4"
#   "openrouter/openai/gpt-4o-mini"
#   "openrouter/google/gemma-2-9b-it:free"  (gratis para pruebas)

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

# ──────────────────────────────────────────────
# Definición del Agente
# ──────────────────────────────────────────────
cis_agent = LlmAgent(
    name="cis_benchmark_advisor",
    model=MODEL,
    description=(
        "Especialista en CIS Benchmarks para Linux y Windows. "
        "Consulta controles específicos, proporciona checklists de hardening, "
        "y da recomendaciones de remediación basadas en los estándares CIS."
    ),
    instruction="""Eres un experto en CIS Benchmarks y hardening de sistemas.

Tu rol es:
1. Ayudar a los usuarios a entender y aplicar controles de seguridad CIS.
2. Proporcionar comandos de verificación y pasos de remediación.
3. Dar recomendaciones priorizadas según el nivel del benchmark (Level 1 = esencial, Level 2 = avanzado).

Reglas:
- Siempre usa las herramientas disponibles para consultar benchmarks reales, NO inventes controles.
- Si el usuario no especifica OS, pregunta cuál sistema operativo necesita.
- Responde en español.
- Sé conciso pero completo en las remediaciones.
- Incluye siempre el comando de verificación cuando sea relevante.
""",
    tools=[check_cis_benchmark, get_hardening_checklist],
)
```

---

## 5. Paso 2: Herramientas (Tools) Personalizadas

Ahora creemos las tools para los otros dos agentes.

### 5.1 Tools del Port Scanner

Crea `cyberguard_agents/tools/scanner_tools.py`:

```python
"""
Herramientas de escaneo de puertos.

CONCEPTO ADK — Tools:
Las tools son el "puente" entre el agente y el mundo real.
- El LLM lee el docstring para entender CUÁNDO usarla.
- Los type hints le dicen QUÉ parámetros pasar.
- El dict de retorno es lo que el LLM procesa como resultado.

En producción, estas tools ejecutarían nmap o conectarían con APIs reales.
Aquí las simulamos para mantener el tutorial funcional sin dependencias extra.
"""
import random


def scan_ports(target: str, port_range: str = "1-1024") -> dict:
    """
    Escanea puertos de un host objetivo y reporta cuáles están abiertos.

    Usa esta herramienta cuando el usuario quiera escanear puertos de un host,
    verificar qué servicios están expuestos, o hacer un reconocimiento básico.

    NOTA: Esta es una simulación. En producción, integrar con nmap o similar.

    Args:
        target: La dirección IP o hostname a escanear (ejemplo: '192.168.1.1', 'servidor.local').
        port_range: Rango de puertos a escanear (ejemplo: '1-1024', '80-443', '22').

    Returns:
        dict: Resultado del escaneo con puertos abiertos y servicios detectados.
    """
    # Simulación de resultados de escaneo
    common_services = {
        22: {"service": "SSH", "risk": "medium", "note": "Verificar que use Protocol 2 y no permita root login"},
        80: {"service": "HTTP", "risk": "high", "note": "Servicio sin cifrado. Considerar redirección a HTTPS"},
        443: {"service": "HTTPS", "risk": "low", "note": "Verificar certificado TLS y versión del protocolo"},
        3306: {"service": "MySQL", "risk": "critical", "note": "Base de datos expuesta. No debe ser accesible externamente"},
        5432: {"service": "PostgreSQL", "risk": "critical", "note": "Base de datos expuesta. Restringir acceso por IP"},
        8080: {"service": "HTTP-Proxy", "risk": "medium", "note": "Puerto alternativo HTTP. Verificar qué servicio corre"},
        3389: {"service": "RDP", "risk": "high", "note": "Remote Desktop expuesto. Usar VPN o restringir por IP"},
        21: {"service": "FTP", "risk": "high", "note": "Protocolo inseguro. Migrar a SFTP"},
        25: {"service": "SMTP", "risk": "medium", "note": "Verificar configuración de relay abierto"},
        53: {"service": "DNS", "risk": "medium", "note": "Verificar que no sea un resolver abierto"},
    }

    # Simular puertos encontrados abiertos
    # En producción: usar python-nmap o socket scanning
    simulated_open = random.sample(
        list(common_services.keys()),
        k=random.randint(2, 5)
    )
    simulated_open.sort()

    open_ports = []
    for port in simulated_open:
        info = common_services[port]
        open_ports.append({
            "port": port,
            "state": "open",
            "service": info["service"],
            "risk_level": info["risk"],
            "recommendation": info["note"]
        })

    risk_summary = {
        "critical": len([p for p in open_ports if p["risk_level"] == "critical"]),
        "high": len([p for p in open_ports if p["risk_level"] == "high"]),
        "medium": len([p for p in open_ports if p["risk_level"] == "medium"]),
        "low": len([p for p in open_ports if p["risk_level"] == "low"]),
    }

    return {
        "status": "success",
        "target": target,
        "port_range": port_range,
        "scan_type": "simulated_tcp_connect",
        "open_ports_count": len(open_ports),
        "open_ports": open_ports,
        "risk_summary": risk_summary,
        "disclaimer": "SIMULACIÓN - En producción integrar con nmap para resultados reales"
    }
```

### 5.2 Tools del Incident Responder

Crea `cyberguard_agents/tools/incident_tools.py`:

```python
"""
Herramientas para respuesta a incidentes.
"""


INCIDENT_PLAYBOOKS = {
    "ransomware": {
        "severity": "critical",
        "category": "Malware",
        "immediate_actions": [
            "1. AISLAR el sistema afectado de la red inmediatamente (desconectar cable/WiFi)",
            "2. NO apagar el equipo (preservar evidencia en memoria RAM)",
            "3. Documentar: hora de detección, síntomas, sistemas afectados",
            "4. Notificar al equipo de respuesta a incidentes",
            "5. Identificar el vector de entrada (email, RDP, USB, web)",
        ],
        "containment": [
            "Bloquear IPs/dominios maliciosos en firewall perimetral",
            "Deshabilitar cuentas comprometidas en Active Directory",
            "Segmentar la red para prevenir movimiento lateral",
            "Capturar imagen forense del disco antes de cualquier remediación",
        ],
        "recovery": [
            "Restaurar desde backups verificados (verificar integridad antes)",
            "Reinstalar sistemas afectados desde imágenes limpias",
            "Cambiar TODAS las contraseñas del dominio",
            "Aplicar parches pendientes antes de reconectar a la red",
            "Monitorear sistemas restaurados por 72 horas mínimo",
        ],
        "post_incident": [
            "Realizar análisis forense completo",
            "Documentar timeline del incidente",
            "Actualizar reglas de detección (SIEM/IDS)",
            "Realizar sesión de lecciones aprendidas",
            "Reportar a autoridades si aplica (CERT nacional)",
        ]
    },
    "phishing": {
        "severity": "high",
        "category": "Social Engineering",
        "immediate_actions": [
            "1. Si se hizo clic en enlace: desconectar de la red",
            "2. Si se ingresaron credenciales: cambiar contraseñas inmediatamente",
            "3. Reportar el email al equipo de seguridad",
            "4. NO reenviar el email sospechoso",
            "5. Verificar si otros usuarios recibieron el mismo email",
        ],
        "containment": [
            "Bloquear el remitente y dominio en el gateway de correo",
            "Buscar y eliminar el email de todos los buzones (purge)",
            "Bloquear URLs maliciosas en proxy/firewall",
            "Revocar tokens de sesión de cuentas comprometidas",
        ],
        "recovery": [
            "Restablecer credenciales de usuarios afectados",
            "Habilitar MFA si no está configurado",
            "Escanear endpoints afectados con EDR/antimalware",
            "Verificar reglas de reenvío de correo no autorizadas",
        ],
        "post_incident": [
            "Enviar alerta de awareness a toda la organización",
            "Agregar indicadores de compromiso (IOCs) al SIEM",
            "Programar simulación de phishing para el departamento afectado",
            "Revisar y reforzar políticas de correo electrónico",
        ]
    },
    "data_breach": {
        "severity": "critical",
        "category": "Data Loss",
        "immediate_actions": [
            "1. Identificar qué datos fueron comprometidos (PII, financieros, IP)",
            "2. Determinar el alcance: cuántos registros/usuarios afectados",
            "3. Preservar logs de acceso y evidencia forense",
            "4. Notificar al CISO y al equipo legal",
            "5. Activar el plan de comunicación de crisis",
        ],
        "containment": [
            "Cerrar la vía de acceso/exfiltración identificada",
            "Revocar accesos de cuentas comprometidas",
            "Implementar monitoreo adicional en sistemas afectados",
            "Verificar integridad de datos restantes",
        ],
        "recovery": [
            "Corregir la vulnerabilidad que permitió el breach",
            "Implementar controles de acceso adicionales (DLP, CASB)",
            "Restaurar datos si fueron modificados/eliminados",
            "Notificar a usuarios afectados según regulaciones (GDPR, LFPDPPP)",
        ],
        "post_incident": [
            "Realizar evaluación de impacto regulatorio",
            "Notificar a autoridades de protección de datos si aplica",
            "Contratar auditoría externa de seguridad",
            "Implementar programa de monitoreo de crédito si aplica",
        ]
    },
    "ddos": {
        "severity": "high",
        "category": "Availability",
        "immediate_actions": [
            "1. Confirmar que es un DDoS y no un problema de capacidad",
            "2. Activar mitigación DDoS del proveedor (Cloudflare, AWS Shield, etc.)",
            "3. Documentar IPs de origen y patrones del ataque",
            "4. Notificar al ISP si el ataque satura el enlace",
            "5. Comunicar a usuarios sobre posible degradación del servicio",
        ],
        "containment": [
            "Habilitar rate limiting agresivo",
            "Bloquear rangos de IP geográficos si el tráfico es de origen conocido",
            "Activar CAPTCHA o challenge pages",
            "Escalar infraestructura si es posible (auto-scaling)",
        ],
        "recovery": [
            "Verificar que todos los servicios respondan correctamente",
            "Revisar logs para identificar si el DDoS fue una cortina de humo",
            "Restaurar configuraciones originales una vez mitigado",
            "Validar integridad de datos post-ataque",
        ],
        "post_incident": [
            "Analizar vectores del ataque (SYN flood, HTTP flood, amplificación)",
            "Evaluar y mejorar la capacidad de mitigación",
            "Considerar servicio de scrubbing permanente",
            "Actualizar runbook de DDoS con lecciones aprendidas",
        ]
    }
}


def classify_incident(description: str) -> dict:
    """
    Clasifica un incidente de seguridad basándose en su descripción
    y retorna el tipo, severidad y categoría.

    Usa esta herramienta cuando el usuario describa un incidente de seguridad
    y necesite saber qué tipo de incidente es y su severidad.

    Args:
        description: Descripción del incidente en lenguaje natural
                     (ejemplo: 'archivos cifrados en el servidor',
                      'usuario reporta email sospechoso con enlace').

    Returns:
        dict: Clasificación del incidente con tipo y severidad.
    """
    description_lower = description.lower()

    # Clasificación basada en keywords
    if any(kw in description_lower for kw in [
        "ransomware", "cifrado", "encrypted", "rescate", "ransom",
        "archivos bloqueados", "extensión extraña"
    ]):
        incident_type = "ransomware"
    elif any(kw in description_lower for kw in [
        "phishing", "email sospechoso", "enlace malicioso", "correo falso",
        "suplantación", "credenciales robadas"
    ]):
        incident_type = "phishing"
    elif any(kw in description_lower for kw in [
        "breach", "fuga de datos", "datos expuestos", "leak",
        "exfiltración", "datos robados", "acceso no autorizado a datos"
    ]):
        incident_type = "data_breach"
    elif any(kw in description_lower for kw in [
        "ddos", "denegación de servicio", "sitio caído", "tráfico anormal",
        "flood", "saturación"
    ]):
        incident_type = "ddos"
    else:
        return {
            "status": "unclassified",
            "message": "No se pudo clasificar automáticamente. "
                       "Tipos conocidos: ransomware, phishing, data_breach, ddos. "
                       "Proporciona más detalles del incidente.",
            "known_types": list(INCIDENT_PLAYBOOKS.keys())
        }

    playbook = INCIDENT_PLAYBOOKS[incident_type]
    return {
        "status": "classified",
        "incident_type": incident_type,
        "severity": playbook["severity"],
        "category": playbook["category"],
        "description_analyzed": description
    }


def get_incident_playbook(incident_type: str, phase: str = "all") -> dict:
    """
    Obtiene el playbook de respuesta para un tipo de incidente específico.

    Usa esta herramienta después de clasificar un incidente, para obtener
    los pasos de respuesta organizados por fase.

    Args:
        incident_type: Tipo de incidente. Opciones: 'ransomware', 'phishing',
                       'data_breach', 'ddos'.
        phase: Fase del playbook a consultar. Opciones: 'all', 'immediate_actions',
               'containment', 'recovery', 'post_incident'.

    Returns:
        dict: Playbook con los pasos de respuesta para el incidente.
    """
    incident_type = incident_type.lower().strip()

    if incident_type not in INCIDENT_PLAYBOOKS:
        return {
            "status": "error",
            "message": f"Tipo '{incident_type}' no encontrado. "
                       f"Disponibles: {', '.join(INCIDENT_PLAYBOOKS.keys())}"
        }

    playbook = INCIDENT_PLAYBOOKS[incident_type]

    if phase == "all":
        return {
            "status": "success",
            "incident_type": incident_type,
            "severity": playbook["severity"],
            "category": playbook["category"],
            "phases": {
                "immediate_actions": playbook["immediate_actions"],
                "containment": playbook["containment"],
                "recovery": playbook["recovery"],
                "post_incident": playbook["post_incident"]
            }
        }

    if phase not in playbook:
        return {
            "status": "error",
            "message": f"Fase '{phase}' no válida. "
                       f"Opciones: all, immediate_actions, containment, recovery, post_incident"
        }

    return {
        "status": "success",
        "incident_type": incident_type,
        "severity": playbook["severity"],
        "phase": phase,
        "steps": playbook[phase]
    }
```

---

## 6. Paso 3: Sistema Multi-Agente

Ahora creemos los sub-agentes y el coordinador.

### 6.1 Concepto: Delegación en ADK

En ADK, la delegación funciona así:

```
Usuario: "Escanea los puertos de 192.168.1.1"
    │
    ▼
Coordinator lee el mensaje
    │
    ├── Lee la `description` de cada sub-agente
    ├── Decide que "port_scanner" es el más apropiado
    │
    ▼
ADK transfiere el control al Port Scanner Agent
    │
    ├── Port Scanner usa su `instruction` como contexto
    ├── Llama a la tool `scan_ports("192.168.1.1")`
    ├── Interpreta el resultado
    │
    ▼
Respuesta final al usuario
```

El coordinador NO necesita conocer los detalles técnicos de las tools. Solo necesita saber la `description` de cada sub-agente.

### 6.2 Port Scanner Agent

Crea `cyberguard_agents/port_scanner/__init__.py`:

```python
from .agent import port_scanner_agent
```

Crea `cyberguard_agents/port_scanner/agent.py`:

```python
"""Port Scanner Agent — Escaneo y análisis de puertos."""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.tools.scanner_tools import scan_ports

MODEL = LiteLlm(
    model="openrouter/google/gemini-2.5-flash",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    api_base="https://openrouter.ai/api/v1",
)

port_scanner_agent = LlmAgent(
    name="port_scanner",
    model=MODEL,
    description=(
        "Especialista en escaneo y análisis de puertos de red. "
        "Escanea hosts, identifica servicios expuestos y evalúa riesgos "
        "de los puertos abiertos encontrados."
    ),
    instruction="""Eres un especialista en reconocimiento de red y análisis de puertos.

Tu rol es:
1. Escanear puertos de hosts que el usuario indique.
2. Analizar los servicios encontrados y evaluar su riesgo.
3. Proporcionar recomendaciones de seguridad para cada puerto abierto.

Reglas:
- Siempre usa la herramienta scan_ports para obtener resultados.
- Prioriza hallazgos por nivel de riesgo (critical > high > medium > low).
- Sugiere acciones concretas para cada hallazgo.
- Responde en español.
- Recuerda mencionar que es una simulación si el usuario pregunta sobre la precisión.
""",
    tools=[scan_ports],
)
```

### 6.3 Incident Responder Agent

Crea `cyberguard_agents/incident_responder/__init__.py`:

```python
from .agent import incident_responder_agent
```

Crea `cyberguard_agents/incident_responder/agent.py`:

```python
"""Incident Responder Agent — Clasificación y respuesta a incidentes."""
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
1. Clasificar incidentes de seguridad según la descripción del usuario.
2. Proporcionar playbooks de respuesta organizados por fase.
3. Guiar al usuario paso a paso durante la respuesta al incidente.

Reglas:
- SIEMPRE clasifica el incidente primero usando classify_incident.
- Luego obtén el playbook correspondiente con get_incident_playbook.
- Presenta los pasos en orden de prioridad: primero acciones inmediatas.
- Si el incidente es crítico, enfatiza la urgencia.
- Responde en español.
- Adapta el nivel técnico según las preguntas del usuario.
""",
    tools=[classify_incident, get_incident_playbook],
)
```

### 6.4 Coordinator Agent (Root Agent)

El **root_agent** es el punto de entrada. ADK busca una variable llamada exactamente `root_agent` en `__init__.py` o `agent.py` del directorio del agente.

Crea `cyberguard_agents/__init__.py`:

```python
"""
CyberGuard — Sistema Multi-Agente de Ciberseguridad.

CONCEPTO ADK — root_agent:
ADK busca una variable llamada `root_agent` en el __init__.py o agent.py
del directorio del agente. Este es el punto de entrada para TODA interacción.
"""
from .agent import root_agent
```

Crea `cyberguard_agents/agent.py`:

```python
"""
Coordinator Agent — Orquesta el sistema multi-agente.

CONCEPTO ADK — sub_agents:
Un agente puede tener `sub_agents`. Cuando el coordinador recibe un mensaje,
el LLM lee las `description` de cada sub-agente y decide a cuál delegar.
Esto es "LLM-driven dynamic routing" — el modelo decide el flujo.

No necesitas escribir lógica de routing manual. El LLM lo hace por ti
basándose en las descripciones.
"""
import os
from google.adk.agents import LlmAgent
from google.adk.models.lite_llm import LiteLlm

from cyberguard_agents.cis_advisor import cis_agent
from cyberguard_agents.port_scanner import port_scanner_agent
from cyberguard_agents.incident_responder import incident_responder_agent

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
  configuraciones de seguridad, checklists de cumplimiento.

- **port_scanner**: Para escaneo de puertos, análisis de servicios expuestos,
  reconocimiento de red, verificación de puertos abiertos.

- **incident_responder**: Para incidentes de seguridad activos, ataques en curso,
  ransomware, phishing, fugas de datos, DDoS, playbooks de respuesta.

Reglas:
- Analiza la intención del usuario y delega al agente más apropiado.
- Si la consulta es general sobre ciberseguridad, responde directamente.
- Si no estás seguro de a quién delegar, pregunta al usuario para clarificar.
- Saluda al usuario como CyberGuard en la primera interacción.
- Responde en español.
""",
    # ──────────────────────────────────────────
    # sub_agents: Aquí está la magia del multi-agente
    # El coordinator puede delegar a cualquiera de estos
    # ──────────────────────────────────────────
    sub_agents=[
        cis_agent,
        port_scanner_agent,
        incident_responder_agent,
    ],
)
```

---

## 7. Paso 4: Integración con FastAPI

### 7.1 El archivo `.env`

Asegúrate de que tu `.env` tenga:

```env
OPENROUTER_API_KEY=sk-or-v1-TU_API_KEY_AQUI
```

### 7.2 Servidor FastAPI

ADK incluye `get_fast_api_app()` que genera automáticamente todos los endpoints necesarios. Pero también podemos agregar endpoints custom.

Crea `main.py`:

```python
"""
CyberGuard — FastAPI Server.

Este archivo integra el sistema de agentes ADK con FastAPI.
Hay DOS formas de hacerlo:

1. `get_fast_api_app()`: Genera automáticamente endpoints ADK completos
   (sessions, run, streaming, etc.). Ideal para usar con el ADK Web UI.

2. Endpoints custom: Creamos nuestras propias rutas con Runner + Session
   para tener control total. Ideal para integrar con frontends propios.

En este tutorial usamos AMBOS enfoques.
"""
import os
import uuid
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Cargar variables de entorno ANTES de importar agentes
load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Importar nuestro root_agent
from cyberguard_agents import root_agent


# ──────────────────────────────────────────────
# Configuración de Session y Runner
# ──────────────────────────────────────────────
# CONCEPTO ADK — SessionService:
# Gestiona el estado de las conversaciones. InMemorySessionService
# almacena todo en memoria (se pierde al reiniciar).
# Para producción: DatabaseSessionService (SQLite, PostgreSQL).

APP_NAME = "cyberguard"
session_service = InMemorySessionService()

# CONCEPTO ADK — Runner:
# Es el "motor de ejecución". Recibe un mensaje, lo pasa al agente,
# gestiona las llamadas a tools, y devuelve la respuesta.
runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service,
)


# ──────────────────────────────────────────────
# Modelos Pydantic para la API
# ──────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    session_id: str | None = None  # None = crear nueva sesión

class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent_name: str


# ──────────────────────────────────────────────
# FastAPI App
# ──────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle del servidor."""
    print("🛡️  CyberGuard Multi-Agent System starting...")
    print(f"📡 Agents loaded: {root_agent.name}")
    for sub in root_agent.sub_agents:
        print(f"   └── {sub.name}: {sub.description[:60]}...")
    yield
    print("🛡️  CyberGuard shutting down...")


app = FastAPI(
    title="CyberGuard API",
    description="Sistema Multi-Agente de Ciberseguridad con Google ADK",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────
@app.get("/")
async def root():
    """Health check y info del sistema."""
    return {
        "service": "CyberGuard",
        "version": "1.0.0",
        "agents": [root_agent.name] + [a.name for a in root_agent.sub_agents],
        "docs": "/docs",
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de chat.

    Envía un mensaje al sistema multi-agente CyberGuard.
    Si no se proporciona session_id, se crea una nueva sesión.
    """
    # Crear o reutilizar sesión
    session_id = request.session_id or str(uuid.uuid4())

    # CONCEPTO ADK — Session:
    # Una session mantiene el historial de la conversación.
    # Cada session tiene un user_id (identifica al usuario)
    # y un session_id (identifica la conversación).
    session = await session_service.get_session(
        app_name=APP_NAME,
        user_id=request.user_id,
        session_id=session_id,
    )

    if session is None:
        session = await session_service.create_session(
            app_name=APP_NAME,
            user_id=request.user_id,
            session_id=session_id,
        )

    # Preparar el mensaje en formato ADK
    user_message = types.Content(
        role="user",
        parts=[types.Part(text=request.message)]
    )

    # CONCEPTO ADK — Runner.run_async():
    # Ejecuta el agente de forma asíncrona. Retorna un stream de Events.
    # Cada Event puede ser: llamada a tool, respuesta parcial, respuesta final.
    # Filtramos por `is_final_response()` para obtener la respuesta completa.
    final_response = ""
    agent_name = root_agent.name

    async for event in runner.run_async(
        user_id=request.user_id,
        session_id=session_id,
        new_message=user_message,
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                agent_name = event.author or root_agent.name

    if not final_response:
        final_response = "No se pudo generar una respuesta. Intenta reformular tu consulta."

    return ChatResponse(
        response=final_response,
        session_id=session_id,
        agent_name=agent_name,
    )


@app.get("/agents")
async def list_agents():
    """Lista todos los agentes disponibles y sus capacidades."""
    agents = [
        {
            "name": root_agent.name,
            "description": root_agent.description,
            "role": "coordinator",
            "sub_agents": [a.name for a in root_agent.sub_agents],
        }
    ]
    for agent in root_agent.sub_agents:
        tool_names = [t.__name__ if callable(t) else str(t) for t in (agent.tools or [])]
        agents.append({
            "name": agent.name,
            "description": agent.description,
            "role": "specialist",
            "tools": tool_names,
        })
    return {"agents": agents}


@app.delete("/sessions/{user_id}/{session_id}")
async def delete_session(user_id: str, session_id: str):
    """Elimina una sesión de conversación."""
    await session_service.delete_session(
        app_name=APP_NAME,
        user_id=user_id,
        session_id=session_id,
    )
    return {"status": "deleted", "session_id": session_id}


# ──────────────────────────────────────────────
# Entry point
# ──────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")
```

---

## 8. Paso 5: Ejecución y Pruebas

### 8.1 Verificar estructura

Tu proyecto debería verse así:

```
cyberguard/
├── .env
├── requirements.txt
├── main.py
│
├── cyberguard_agents/
│   ├── __init__.py                    # Exporta root_agent
│   ├── agent.py                       # Coordinator
│   │
│   ├── cis_advisor/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── port_scanner/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   ├── incident_responder/
│   │   ├── __init__.py
│   │   └── agent.py
│   │
│   └── tools/
│       ├── __init__.py
│       ├── cis_tools.py
│       ├── scanner_tools.py
│       └── incident_tools.py
```

### 8.2 Opción A: Ejecutar con FastAPI (nuestro servidor custom)

```bash
# Desde el directorio cyberguard/
python main.py
```

Abre http://localhost:8080/docs para ver la documentación Swagger interactiva.

### 8.3 Opción B: Ejecutar con ADK Web UI (interfaz de desarrollo)

ADK incluye un UI de desarrollo que es muy útil para debugging:

```bash
# Desde el directorio PADRE de cyberguard_agents/
adk web
```

Luego abre http://localhost:8000 y selecciona `cyberguard_agents` en el dropdown.

### 8.4 Probar con cURL

```bash
# ── Test 1: Health check ──
curl http://localhost:8080/

# ── Test 2: CIS Benchmark (delega al cis_benchmark_advisor) ──
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuáles son los controles CIS de SSH para Linux?",
    "user_id": "quantum"
  }'

# ── Test 3: Port Scanning (delega al port_scanner) ──
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Escanea los puertos del servidor 192.168.1.100",
    "user_id": "quantum"
  }'

# ── Test 4: Incident Response (delega al incident_responder) ──
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Tenemos archivos cifrados en el servidor de producción y apareció una nota de rescate",
    "user_id": "quantum"
  }'

# ── Test 5: Consulta general (responde el coordinator) ──
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Qué servicios de ciberseguridad ofreces?",
    "user_id": "quantum"
  }'

# ── Test 6: Continuidad de sesión ──
# Primero obtén el session_id de una respuesta anterior, luego:
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Ahora muéstrame el checklist completo de Linux",
    "user_id": "quantum",
    "session_id": "PEGAR_SESSION_ID_AQUI"
  }'

# ── Test 7: Listar agentes ──
curl http://localhost:8080/agents
```

### 8.5 Probar con Python

Crea `tests/test_agents.py`:

```python
"""Test rápido del sistema CyberGuard."""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from cyberguard_agents import root_agent


async def test_chat(message: str):
    """Envía un mensaje al sistema y muestra la respuesta."""
    session_service = InMemorySessionService()
    runner = Runner(
        agent=root_agent,
        app_name="cyberguard_test",
        session_service=session_service,
    )

    session = await session_service.create_session(
        app_name="cyberguard_test",
        user_id="tester",
        session_id="test-001",
    )

    content = types.Content(role="user", parts=[types.Part(text=message)])

    print(f"\n{'='*60}")
    print(f"📤 Pregunta: {message}")
    print(f"{'='*60}")

    async for event in runner.run_async(
        user_id="tester",
        session_id="test-001",
        new_message=content,
    ):
        # Mostrar eventos intermedios (tool calls, delegaciones)
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    print(f"  🔧 Tool call: {part.function_call.name}({part.function_call.args})")
                if hasattr(part, 'function_response') and part.function_response:
                    print(f"  📦 Tool response received")

        if event.is_final_response():
            if event.content and event.content.parts:
                print(f"\n📥 Respuesta ({event.author}):")
                print(event.content.parts[0].text)


async def main():
    test_cases = [
        "¿Cuáles son los controles CIS de SSH para Linux?",
        "Escanea los puertos de 10.0.0.1",
        "Recibimos un email con un enlace sospechoso y un empleado dio sus credenciales",
    ]

    for test in test_cases:
        await test_chat(test)
        print("\n")


if __name__ == "__main__":
    asyncio.run(main())
```

Ejecuta:

```bash
python tests/test_agents.py
```

---

## 9. Conceptos Clave de ADK

### 9.1 Resumen de Arquitectura

```
┌──────────────────────────────────────────────────┐
│                    ADK Stack                     │
├──────────────────────────────────────────────────┤
│                                                  │
│  LlmAgent          ← Define agentes con LLM     │
│    ├── model        ← LLM a usar (LiteLlm)      │
│    ├── instruction  ← System prompt              │
│    ├── description  ← Para routing multi-agente  │
│    ├── tools        ← Funciones Python           │
│    └── sub_agents   ← Agentes hijos (delegación) │
│                                                  │
│  Runner             ← Motor de ejecución         │
│    ├── run_async()  ← Ejecuta el agente          │
│    └── Events       ← Stream de resultados       │
│                                                  │
│  SessionService     ← Gestión de conversaciones  │
│    ├── InMemory     ← Para desarrollo            │
│    └── Database     ← Para producción            │
│                                                  │
│  LiteLlm            ← Conector de modelos        │
│    ├── OpenRouter    ← Múltiples proveedores     │
│    ├── Ollama        ← Modelos locales           │
│    └── OpenAI/etc    ← Conexión directa          │
│                                                  │
│  FastAPI             ← Deployment como API REST  │
│    └── get_fast_api_app() ← Generación auto      │
│                                                  │
└──────────────────────────────────────────────────┘
```

### 9.2 Flujo de una solicitud

```
1. Usuario envía mensaje via POST /chat
2. Runner recibe el mensaje + session_id
3. Runner pasa el mensaje al root_agent (coordinator)
4. El LLM del coordinator lee las descriptions de sub_agents
5. El LLM decide a quién delegar (o responde directamente)
6. Si delega → ADK transfiere el control al sub-agente
7. El sub-agente procesa con su instruction + tools
8. Si necesita una tool → el LLM genera function_call
9. ADK ejecuta la función Python y retorna el resultado
10. El LLM interpreta el resultado y genera la respuesta final
11. Runner retorna el evento final al endpoint FastAPI
12. El endpoint retorna la respuesta al usuario
```

### 9.3 Tips para diseñar Tools

```python
# ✅ BUENA tool: docstring claro, types específicos, retorna dict
def check_cis_benchmark(os_type: str, benchmark_id: str) -> dict:
    """
    Consulta un control específico de CIS Benchmark.

    Args:
        os_type: Sistema operativo ('linux' o 'windows').
        benchmark_id: ID del benchmark (ejemplo: '5.2.1').

    Returns:
        dict: Información del benchmark.
    """
    ...

# ❌ MALA tool: sin docstring, types vagos, no retorna dict
def check(x, y):
    return "ok"
```

### 9.4 Tips para descriptions de agentes

```python
# ✅ BUENA description: específica, con keywords claros
description="Especialista en CIS Benchmarks para Linux y Windows. "
            "Consulta controles específicos y proporciona checklists de hardening."

# ❌ MALA description: vaga, no ayuda al routing
description="Un agente de seguridad."
```

---

## 10. Troubleshooting y Tips

### Errores comunes

| Error | Causa | Solución |
|-------|-------|----------|
| `OPENROUTER_API_KEY not found` | `.env` no cargado | Verifica que `load_dotenv()` está antes de los imports de agentes |
| `BadRequestError: Provider returned error` | Modelo no soporta function calling | Usa un modelo que soporte tools: `gemini-2.5-flash`, `gpt-4o-mini`, `claude-sonnet-4` |
| `root_agent not found` | Import incorrecto | Verifica que `__init__.py` exporta `root_agent` |
| `Session not found` | Session expirada o incorrecta | Crea una nueva session (omite `session_id`) |
| Rate limit exceeded | Muchas requests a OpenRouter | Agrega delays o usa tier pago |

### Modelos recomendados en OpenRouter

| Modelo | Precio | Tool Calling | Recomendación |
|--------|--------|-------------|---------------|
| `google/gemma-2-9b-it:free` | Gratis | Limitado | Solo pruebas básicas |
| `google/gemini-2.5-flash` | ~$0.15/1M tokens | Sí | Mejor relación costo/rendimiento |
| `openai/gpt-4o-mini` | ~$0.15/1M tokens | Sí | Bueno para tools |
| `anthropic/claude-sonnet-4` | ~$3/1M tokens | Sí | Máxima calidad |

### Tips de producción

1. **Cambia `InMemorySessionService`** por `DatabaseSessionService` con SQLite o PostgreSQL.
2. **Agrega autenticación** al FastAPI (API keys, OAuth2).
3. **Implementa rate limiting** con `slowapi` o middleware custom.
4. **Usa modelos diferentes por agente** — el coordinator puede usar un modelo barato y los especialistas uno más potente.
5. **Agrega logging** estructurado para debugging.

---

## 11. Próximos Pasos

Ahora que tienes un sistema funcional, puedes expandirlo:

### Ideas de expansión inmediata

- **Tools reales**: Conectar `scan_ports` con `python-nmap` para escaneos reales.
- **Base de datos CIS**: Importar el dataset completo de CIS Benchmarks.
- **MCP Integration**: Exponer las tools como un MCP Server para usar con Claude, Cursor, etc.
- **Workflow Agents**: Usar `SequentialAgent` para pipelines de auditoría automática.
- **Callbacks**: Agregar `before_tool_callback` para logging o confirmación HITL (Human-in-the-loop).

### Ejemplo: Agregar un SequentialAgent para auditoría

```python
from google.adk.agents import SequentialAgent

# Pipeline: Escanear → Evaluar CIS → Generar reporte
audit_pipeline = SequentialAgent(
    name="security_audit",
    description="Ejecuta una auditoría de seguridad completa en secuencia.",
    sub_agents=[port_scanner_agent, cis_agent, report_generator_agent],
)
```

### Ejemplo: Callback de confirmación antes de escanear

```python
from google.adk.agents import LlmAgent

async def confirm_scan(callback_context, tool_name, args):
    """Pide confirmación antes de ejecutar un escaneo."""
    if tool_name == "scan_ports":
        # En producción: enviar notificación y esperar aprobación
        print(f"⚠️ Confirmar escaneo de {args.get('target')}?")
    return None  # None = continuar, retornar dict = cancelar

port_scanner_agent = LlmAgent(
    name="port_scanner",
    # ...
    before_tool_callback=confirm_scan,
)
```

---

## 📚 Recursos

- [Documentación oficial ADK](https://google.github.io/adk-docs/)
- [Repositorio GitHub ADK Python](https://github.com/google/adk-python)
- [LiteLLM Providers](https://docs.litellm.ai/docs/providers)
- [OpenRouter Models](https://openrouter.ai/models)
- [CIS Benchmarks](https://www.cisecurity.org/cis-benchmarks)
- [ADK + LiteLLM Docs](https://google.github.io/adk-docs/agents/models/litellm/)

---

> **Autor:** Tutorial creado para uso freelance en ciberseguridad  
> **Stack:** Google ADK + OpenRouter (LiteLLM) + FastAPI + Python  
> **Licencia:** Libre para uso personal y comercial
# AgentCyber

Sistema multiagente de ciberseguridad con 3 agentes especializados, desarrollado con Python, FastAPI y Google Generative AI.

## Descripción

AgentCyber es un sistema de análisis de ciberseguridad basado en múltiples agentes de IA que trabajan de forma coordinada para:

- **Agente de Seguridad**: Monitoreo y detección de amenazas en tiempo real
- **Agente de Análisis**: Análisis profundo de amenazas y reconocimiento de patrones
- **Agente de Respuesta**: Planificación de respuesta a incidentes y remediación

## Características

- ✅ 3 agentes especializados trabajando en conjunto
- ✅ API REST desarrollada con FastAPI
- ✅ Integración con Google Generative AI (Gemini)
- ✅ Análisis completo multi-agente
- ✅ Endpoints individuales para cada agente
- ✅ Documentación automática con Swagger/OpenAPI

## Requisitos

- Python 3.8+
- Google API Key (para Generative AI)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/QuantumEdu/AgentCyber.git
cd AgentCyber
```

2. Crear un entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Configurar variables de entorno:
```bash
cp .env.example .env
# Editar .env y agregar tu GOOGLE_API_KEY
```

## Uso

### Iniciar el servidor

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

El servidor estará disponible en `http://localhost:8000`

### Documentación API

Una vez iniciado el servidor, accede a:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Ejemplos de uso

#### 1. Agente de Seguridad

```bash
curl -X POST "http://localhost:8000/agent/security" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Se detectaron múltiples intentos de login fallidos desde la IP 192.168.1.100",
    "context": "Usuario: admin"
  }'
```

#### 2. Agente de Análisis

```bash
curl -X POST "http://localhost:8000/agent/analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analizar posible ataque de fuerza bruta",
    "context": "Patrón detectado en logs de autenticación"
  }'
```

#### 3. Agente de Respuesta

```bash
curl -X POST "http://localhost:8000/agent/response" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Plan de respuesta para ataque DDoS detectado",
    "context": "Tráfico anormal desde múltiples IPs"
  }'
```

#### 4. Análisis Completo (3 agentes)

```bash
curl -X POST "http://localhost:8000/agent/full-analysis" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Actividad sospechosa detectada en el servidor web",
    "context": "Múltiples solicitudes a rutas no existentes"
  }'
```

## Arquitectura

```
AgentCyber/
├── app/
│   ├── __init__.py
│   ├── main.py              # Aplicación FastAPI principal
│   ├── agents/              # Agentes especializados
│   │   ├── __init__.py
│   │   ├── base_agent.py    # Clase base para agentes
│   │   ├── security_agent.py    # Agente de seguridad
│   │   ├── analysis_agent.py    # Agente de análisis
│   │   └── response_agent.py    # Agente de respuesta
│   ├── models/              # Modelos de datos
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── utils/               # Utilidades
│       ├── __init__.py
│       └── config.py
├── requirements.txt
├── .env.example
└── README.md
```

## Endpoints API

### Información del Sistema

- `GET /` - Información general del sistema
- `GET /health` - Estado de salud del sistema

### Agentes Individuales

- `POST /agent/security` - Consultar agente de seguridad
- `POST /agent/analysis` - Consultar agente de análisis
- `POST /agent/response` - Consultar agente de respuesta

### Análisis Multi-Agente

- `POST /agent/full-analysis` - Análisis completo con los 3 agentes

## Tecnologías

- **FastAPI**: Framework web moderno y rápido
- **Python**: Lenguaje de programación
- **Google Generative AI**: Modelo de IA Gemini Pro
- **Pydantic**: Validación de datos
- **Uvicorn**: Servidor ASGI

## Licencia

Ver archivo [LICENSE](LICENSE) para más detalles.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request para sugerencias o mejoras.
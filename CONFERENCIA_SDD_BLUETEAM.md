# Conferencia (45 min) — Versión final

## Título
**De SDD a Blue Team: Ingeniería de Agentes IA para Ciberseguridad Real**

## Público objetivo
Estudiantes de ciberseguridad (2° y 4° trimestre)

## Duración
45 minutos (incluye demos)

---

## Slide 01
**Título:** Portada  
**Subtema:** Contexto de la conferencia  
**Contenido:**
- Presentación del tema, expositor y objetivo.
- Idea central: pasar de “usar IA” a “ingeniería de sistemas de IA para ciberseguridad”.
**Demostración:** No

## Slide 02
**Título:** Agenda  
**Subtema:** Los 3 ejes + demos  
**Contenido:**
1. Flujo IA con SDD + agentes + swarms + rules + skills.
2. ADK + programación + DevOps/DevSecOps + GitHub + Docker.
3. Pentesting y Blue Team asistidos por IA.
**Demostración:** No

## Slide 03
**Título:** Problema real en ciberseguridad  
**Subtema:** Brecha entre PoC y operación  
**Contenido:**
- Muchas pruebas de concepto no escalan a producción.
- SOC con alto volumen de alertas y bajo contexto.
- Se requiere trazabilidad, calidad y gobernanza técnica.
**Demostración:** No

## Slide 04
**Título:** ¿Por qué ADK?  
**Subtema:** Orquestación real de agentes  
**Contenido:**
- Definición clara de roles por agente.
- Integración de tools y flujos ejecutables.
- Arquitectura extensible para ciberseguridad aplicada.
**Demostración:** No

## Slide 05
**Título:** Estructura de agentes (swarm)  
**Subtema:** División de responsabilidades  
**Contenido:**
- Orquestador: coordina secuencia y criterios.
- Recon Agent: recibe señales iniciales.
- Analysis Agent: correlación + scoring de riesgo.
- Response Agent: propone contención y remediación.
- Report Agent: salida técnica y ejecutiva.
**Demostración:** **Sí (Demo A - 3 min)**

## Slide 06
**Título:** Del prompt al sistema con SDD  
**Subtema:** Ingeniería por especificación  
**Contenido:**
- Flujo: proposal → spec → design → tasks → apply → verify.
- Menos improvisación, más consistencia técnica.
- Facilita auditoría, calidad y aprendizaje del equipo.
**Demostración:** No

## Slide 07 (NUEVA)
**Título:** SDD y marcos relacionados (comparativa)  
**Subtema:** Opciones para estructurar desarrollo con IA  
**Contenido:**

| Enfoque | Objetivo principal | Fortalezas | Riesgos/Limitaciones | Cuándo usarlo |
|---|---|---|---|---|
| **Spec Kit** | Estandarizar requisitos y diseño | Plantillas claras, onboarding rápido | Puede quedar documental si no hay ejecución disciplinada | Equipos en etapa formativa de ingeniería |
| **OpenSpec** | Especificaciones versionables en repositorio | Trazabilidad en Git, colaboración en equipo | Más fricción inicial para mantener artefactos | Proyectos académicos/profesionales con revisión formal |
| **GSD** (Goal-Structured Delivery) | Entregar por objetivos medibles | Alinea negocio/técnica, foco en outcomes | Riesgo de simplificar demasiado lo técnico | Roadmaps con metas trimestrales y KPIs |
| **BDM** (Behavior-Driven Modeling) | Diseñar por comportamientos observables | Excelente para pruebas y validación | Requiere madurez en modelado de escenarios | Sistemas con lógica compleja y alta criticidad |
| **IA DLC** (AI Development Life Cycle) | Ciclo de vida integral de soluciones IA | Cubre datos, modelo, despliegue, monitoreo | Puede ser pesado si el alcance es pequeño | Soluciones IA con operación continua y compliance |

- Recomendación para esta charla/proyecto: **SDD + prácticas IA DLC + ejecución DevSecOps**.
**Demostración:** No

## Slide 08
**Título:** Agentes, swarms, rules y skills  
**Subtema:** Componentes base de la solución  
**Contenido:**
- Agente: rol técnico especializado.
- Swarm: coordinación de varios agentes.
- Rules: guardrails de seguridad y calidad.
- Skills: bloques reutilizables de capacidad.
**Demostración:** No

## Slide 09
**Título:** Ventajas concretas de ADK  
**Subtema:** Diferenciales técnicos  
**Contenido:**
- Desacopla roles y reduce complejidad por módulo.
- Escala de 1 a N agentes sin reescribir todo.
- Mejor observabilidad de decisiones y tools.
- Facilita iteración y mantenimiento evolutivo.
**Demostración:** No

## Slide 10
**Título:** Ejemplo de código de agente ADK  
**Subtema:** Código mínimo útil  
**Contenido:**
```python
from google.adk.agents import Agent

def classify_alert(alert: str) -> dict:
    critical_keywords = ["ransomware", "exfiltration", "c2", "lateral movement"]
    score = sum(1 for k in critical_keywords if k in alert.lower())
    level = "high" if score >= 2 else "medium" if score == 1 else "low"
    return {"risk_level": level, "score": score}

triage_agent = Agent(
    name="triage_agent",
    model="gemini-2.0-flash",
    description="Clasifica alertas iniciales",
    instruction=(
        "Analizá la alerta, devolvé nivel de riesgo y justificación breve. "
        "Si falta contexto, pedí más datos."
    ),
    tools=[classify_alert],
)
```
**Demostración:** **Sí (Demo B - 4 min)**

## Slide 11
**Título:** Flujo end-to-end  
**Subtema:** Entrada, análisis, salida accionable  
**Contenido:**
- Evento de seguridad → swarm → clasificación y respuesta sugerida.
- Salida estructurada: riesgo, evidencia, acción priorizada.
**Demostración:** No

## Slide 12
**Título:** GitHub como backbone operativo  
**Subtema:** Trazabilidad del trabajo técnico  
**Contenido:**
- Issues para historias/casos.
- Branching por feature/incidente.
- Pull Requests con revisión técnica + seguridad.
- Historial auditable de decisiones.
**Demostración:** No

## Slide 13
**Título:** FastAPI + ADK  
**Subtema:** Exponer agentes como servicio  
**Contenido:**
- Endpoint para inferencia/triage.
- Contrato JSON claro.
- Integración con otros sistemas de seguridad.
**Demostración:** **Sí (Demo C - 4 min)**

## Slide 14
**Título:** Dockerización  
**Subtema:** Reproducibilidad y despliegue  
**Contenido:**
- Empaquetado de dependencias y runtime.
- Configuración por entorno.
- Consistencia entre desarrollo y demo/lab.
**Demostración:** **Sí (Demo D - 3 min)**

## Slide 15
**Título:** DevOps por etapa (qué se hizo / qué se hace)  
**Subtema:** Práctica operativa real  
**Contenido:**
- Plan: issue + criterios de aceptación.
- Build: validación de dependencias, lint/tests.
- Secure: secretos, vulnerabilidades, revisión de cambios.
- Release: versionado de imagen y changelog.
- Operate: logs, alertas y rollback.
- Improve: postmortem y hardening.
**Demostración:** No

## Slide 16
**Título:** DevSecOps mínimo viable  
**Subtema:** Seguridad integrada al ciclo  
**Contenido:**
- Gate de seguridad antes de release.
- Reglas para secrets y dependencias críticas.
- Aprobación técnica para cambios sensibles.
**Demostración:** No

## Slide 17
**Título:** Caso Red Team (entorno autorizado)  
**Subtema:** Pentesting asistido por IA  
**Contenido:**
- Reconocimiento y priorización de hipótesis.
- Validación controlada de hallazgos.
- Reporte con impacto y mitigación.
**Demostración:** **Sí (Demo E - 4 min)**

## Slide 18
**Título:** Comandos del agente de ciberseguridad (demo segura)  
**Subtema:** Ejecución técnica y pipeline de análisis  
**Contenido:**
> Solo en laboratorio autorizado.

- `nmap -sV -T3 <host_lab>`
- `nikto -h https://<host_lab>`
- `curl -I https://<host_lab>`
- `zap-baseline.py -t https://<host_lab> -r zap_report.html`

Pipeline del agente:
1. Ejecuta comando permitido.
2. Parsea salida estructurada.
3. Asigna severidad.
4. Propone remediación priorizada.
**Demostración:** **Sí (Demo F - 5 min)**

## Slide 19
**Título:** Caso Blue Team  
**Subtema:** Detección, triage y respuesta  
**Contenido:**
- Correlación de eventos y reducción de ruido.
- Clasificación por criticidad.
- Recomendaciones de contención e investigación.
**Demostración:** **Sí (Demo G - 4 min)**

## Slide 20
**Título:** Métricas de valor  
**Subtema:** Cómo medir mejora real  
**Contenido:**
- MTTD, MTTR.
- Tasa de falsos positivos.
- Tiempo de remediación por severidad.
**Demostración:** No

## Slide 21
**Título:** Riesgos y límites de IA en ciberseguridad  
**Subtema:** Gobernanza y criterio profesional  
**Contenido:**
- Alucinación y sobreautomatización.
- Exposición de datos sensibles.
- Mitigación: human-in-the-loop, validación, políticas.
**Demostración:** No

## Slide 22
**Título:** Ruta de aprendizaje (2° y 4° trimestre)  
**Subtema:** Cómo crecer técnicamente  
**Contenido:**
- Base: redes, Linux, scripting, Git.
- Intermedio: APIs, Docker, CI/CD.
- Avanzado: detección, respuesta, agentes IA productivos.
**Demostración:** No

## Slide 23
**Título:** Arquitectura final consolidada  
**Subtema:** Vista completa del sistema  
**Contenido:**
- Capa IA (swarm ADK).
- Capa servicio (API).
- Capa operación (DevSecOps).
- Capa ciber (red + blue + mejora continua).
**Demostración:** No

## Slide 24
**Título:** Mejoras futuras (esta solución es base)  
**Subtema:** Roadmap de evolución  
**Contenido:**
- Integración SIEM/SOAR.
- Evaluación sistemática de calidad de agentes.
- RAG con base de incidentes internos.
- Controles avanzados (RBAC, SBOM, firma de artefactos).
- Observabilidad avanzada por agente.
**Demostración:** No

## Slide 25
**Título:** Cierre + Q&A  
**Subtema:** Mensaje final  
**Contenido:**
- No es magia: es arquitectura, ingeniería y disciplina.
- Próximo paso: implementar mini-lab por equipos.
**Demostración:** No

---

## Notas finales — Propuestas de ejercicios prácticos

1. **Mini-swarm de triage (básico)**
   - Crear 2 agentes: uno clasifica severidad, otro propone remediación.
   - Entrada: 10 alertas simuladas.
   - Salida: tabla priorizada con justificación.

2. **API de seguridad con ADK + FastAPI (intermedio)**
   - Exponer endpoint `/triage`.
   - Agregar validación de esquema JSON y manejo de errores.
   - Probar con casos benignos y críticos.

3. **Pipeline DevSecOps mínimo (intermedio/avanzado)**
   - Definir flujo: lint + tests + análisis de dependencias.
   - Gate de seguridad para bloquear release con hallazgos críticos.
   - Entregar evidencia de pipeline y acciones correctivas.

4. **Red vs Blue en laboratorio controlado (avanzado)**
   - Red Team: reconocimiento autorizado + reporte de hallazgos.
   - Blue Team: detección, triage y plan de contención.
   - Cierre: comparar tiempos y precisión antes/después del uso de agentes.

5. **Métricas y mejora continua (avanzado)**
   - Medir MTTD, MTTR, falsos positivos y cobertura.
   - Proponer 3 mejoras concretas de arquitectura/proceso.
   - Presentar roadmap técnico trimestral.

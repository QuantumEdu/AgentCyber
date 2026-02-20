"""
Herramientas para respuesta a incidentes de ciberseguridad.
"""

INCIDENT_PLAYBOOKS = {
    "ransomware": {
        "severity": "critical",
        "category": "Malware",
        "immediate_actions": [
            "1. AISLAR el sistema afectado de la red inmediatamente (desconectar cable/WiFi)",
            "2. NO apagar el equipo (preservar evidencia en memoria RAM)",
            "3. Documentar: hora de deteccion, sintomas, sistemas afectados",
            "4. Notificar al equipo de respuesta a incidentes",
            "5. Identificar el vector de entrada (email, RDP, USB, web)",
        ],
        "containment": [
            "Bloquear IPs/dominios maliciosos en firewall perimetral",
            "Deshabilitar cuentas comprometidas en Active Directory",
            "Segmentar la red para prevenir movimiento lateral",
            "Capturar imagen forense del disco antes de cualquier remediacion",
        ],
        "recovery": [
            "Restaurar desde backups verificados (verificar integridad antes)",
            "Reinstalar sistemas afectados desde imagenes limpias",
            "Cambiar TODAS las contraseñas del dominio",
            "Aplicar parches pendientes antes de reconectar a la red",
            "Monitorear sistemas restaurados por 72 horas minimo",
        ],
        "post_incident": [
            "Realizar analisis forense completo",
            "Documentar timeline del incidente",
            "Actualizar reglas de deteccion (SIEM/IDS)",
            "Realizar sesion de lecciones aprendidas",
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
            "Revocar tokens de sesion de cuentas comprometidas",
        ],
        "recovery": [
            "Restablecer credenciales de usuarios afectados",
            "Habilitar MFA si no esta configurado",
            "Escanear endpoints afectados con EDR/antimalware",
            "Verificar reglas de reenvio de correo no autorizadas",
        ],
        "post_incident": [
            "Enviar alerta de awareness a toda la organizacion",
            "Agregar indicadores de compromiso (IOCs) al SIEM",
            "Programar simulacion de phishing para el departamento afectado",
            "Revisar y reforzar politicas de correo electronico",
        ]
    },
    "data_breach": {
        "severity": "critical",
        "category": "Data Loss",
        "immediate_actions": [
            "1. Identificar que datos fueron comprometidos (PII, financieros, IP)",
            "2. Determinar el alcance: cuantos registros/usuarios afectados",
            "3. Preservar logs de acceso y evidencia forense",
            "4. Notificar al CISO y al equipo legal",
            "5. Activar el plan de comunicacion de crisis",
        ],
        "containment": [
            "Cerrar la via de acceso/exfiltracion identificada",
            "Revocar accesos de cuentas comprometidas",
            "Implementar monitoreo adicional en sistemas afectados",
            "Verificar integridad de datos restantes",
        ],
        "recovery": [
            "Corregir la vulnerabilidad que permitio el breach",
            "Implementar controles de acceso adicionales (DLP, CASB)",
            "Restaurar datos si fueron modificados/eliminados",
            "Notificar a usuarios afectados segun regulaciones (GDPR, LFPDPPP)",
        ],
        "post_incident": [
            "Realizar evaluacion de impacto regulatorio",
            "Notificar a autoridades de proteccion de datos si aplica",
            "Contratar auditoria externa de seguridad",
            "Implementar programa de monitoreo de credito si aplica",
        ]
    },
    "ddos": {
        "severity": "high",
        "category": "Availability",
        "immediate_actions": [
            "1. Confirmar que es un DDoS y no un problema de capacidad",
            "2. Activar mitigacion DDoS del proveedor (Cloudflare, AWS Shield, etc.)",
            "3. Documentar IPs de origen y patrones del ataque",
            "4. Notificar al ISP si el ataque satura el enlace",
            "5. Comunicar a usuarios sobre posible degradacion del servicio",
        ],
        "containment": [
            "Habilitar rate limiting agresivo",
            "Bloquear rangos de IP geograficos si el trafico es de origen conocido",
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
            "Analizar vectores del ataque (SYN flood, HTTP flood, amplificacion)",
            "Evaluar y mejorar la capacidad de mitigacion",
            "Considerar servicio de scrubbing permanente",
            "Actualizar runbook de DDoS con lecciones aprendidas",
        ]
    }
}


def classify_incident(description: str) -> dict:
    """
    Clasifica un incidente de seguridad basandose en su descripcion
    y retorna el tipo, severidad y categoria.

    Usa esta herramienta cuando el usuario describa un incidente de seguridad
    y necesite saber que tipo de incidente es y su severidad.

    Args:
        description: Descripcion del incidente en lenguaje natural
                     (ejemplo: 'archivos cifrados en el servidor',
                      'usuario reporta email sospechoso con enlace').

    Returns:
        dict: Clasificacion del incidente con tipo y severidad.
    """
    description_lower = description.lower()

    if any(kw in description_lower for kw in [
        "ransomware", "cifrado", "encrypted", "rescate", "ransom",
        "archivos bloqueados", "extension extraña"
    ]):
        incident_type = "ransomware"
    elif any(kw in description_lower for kw in [
        "phishing", "email sospechoso", "enlace malicioso", "correo falso",
        "suplantacion", "credenciales robadas"
    ]):
        incident_type = "phishing"
    elif any(kw in description_lower for kw in [
        "breach", "fuga de datos", "datos expuestos", "leak",
        "exfiltracion", "datos robados", "acceso no autorizado a datos"
    ]):
        incident_type = "data_breach"
    elif any(kw in description_lower for kw in [
        "ddos", "denegacion de servicio", "sitio caido", "trafico anormal",
        "flood", "saturacion"
    ]):
        incident_type = "ddos"
    else:
        return {
            "status": "unclassified",
            "message": "No se pudo clasificar automaticamente. "
                       "Tipos conocidos: ransomware, phishing, data_breach, ddos. "
                       "Proporciona mas detalles del incidente.",
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
    Obtiene el playbook de respuesta para un tipo de incidente especifico.

    Usa esta herramienta despues de clasificar un incidente, para obtener
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
            "message": f"Fase '{phase}' no valida. "
                       f"Opciones: all, immediate_actions, containment, recovery, post_incident"
        }

    return {
        "status": "success",
        "incident_type": incident_type,
        "severity": playbook["severity"],
        "phase": phase,
        "steps": playbook[phase]
    }

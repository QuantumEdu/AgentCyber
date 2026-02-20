"""
Herramientas de reconocimiento: DNS, WHOIS y analisis de headers HTTP.

Usa librerias reales (dnspython, python-whois, httpx).
Si una libreria no esta instalada, retorna error descriptivo.
"""
import socket


def dns_lookup(domain: str) -> dict:
    """
    Realiza consultas DNS para un dominio, obteniendo registros A, MX, NS y TXT.

    Usa esta herramienta cuando el usuario quiera obtener informacion DNS de un dominio,
    verificar registros MX, NS, o buscar registros TXT como SPF/DKIM.

    Args:
        domain: El dominio a consultar (ejemplo: 'example.com', 'google.com').

    Returns:
        dict: Registros DNS encontrados organizados por tipo.
    """
    try:
        import dns.resolver
    except ImportError:
        return {
            "status": "error",
            "message": (
                "dnspython no esta instalado. "
                "Instala con: pip install dnspython"
            ),
        }

    results = {"A": [], "MX": [], "NS": [], "TXT": []}

    # Registros A via socket (siempre disponible)
    try:
        addr_info = socket.getaddrinfo(domain, None, socket.AF_INET)
        results["A"] = list({info[4][0] for info in addr_info})
    except socket.gaierror:
        results["A"] = []

    # Registros MX
    try:
        mx_records = dns.resolver.resolve(domain, "MX")
        results["MX"] = [
            {"priority": r.preference, "host": str(r.exchange).rstrip(".")}
            for r in mx_records
        ]
    except Exception:
        results["MX"] = []

    # Registros NS
    try:
        ns_records = dns.resolver.resolve(domain, "NS")
        results["NS"] = [str(r.target).rstrip(".") for r in ns_records]
    except Exception:
        results["NS"] = []

    # Registros TXT
    try:
        txt_records = dns.resolver.resolve(domain, "TXT")
        results["TXT"] = [str(r).strip('"') for r in txt_records]
    except Exception:
        results["TXT"] = []

    return {
        "status": "success",
        "domain": domain,
        "records": results,
    }


def whois_lookup(target: str) -> dict:
    """
    Realiza una consulta WHOIS para un dominio o IP, obteniendo informacion de registro.

    Usa esta herramienta cuando el usuario quiera saber quien registro un dominio,
    cuando expira, o informacion del registrante.

    Args:
        target: Dominio o IP a consultar (ejemplo: 'example.com', '8.8.8.8').

    Returns:
        dict: Informacion WHOIS del dominio/IP.
    """
    try:
        import whois
    except ImportError:
        return {
            "status": "error",
            "message": (
                "python-whois no esta instalado. "
                "Instala con: pip install python-whois"
            ),
        }

    try:
        w = whois.whois(target)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en consulta WHOIS para '{target}': {e}",
        }

    # Normalizar campos que pueden ser listas o valores unicos
    def _first(val):
        if isinstance(val, list):
            return str(val[0]) if val else None
        return str(val) if val else None

    def _str_date(val):
        if isinstance(val, list):
            val = val[0] if val else None
        return str(val) if val else None

    return {
        "status": "success",
        "target": target,
        "whois": {
            "domain_name": _first(w.domain_name),
            "registrar": _first(w.registrar),
            "creation_date": _str_date(w.creation_date),
            "expiration_date": _str_date(w.expiration_date),
            "updated_date": _str_date(w.updated_date),
            "name_servers": w.name_servers if isinstance(w.name_servers, list) else [],
            "registrant": _first(getattr(w, "org", None) or getattr(w, "name", None)),
            "country": _first(getattr(w, "country", None)),
        },
    }


def check_http_headers(url: str) -> dict:
    """
    Analiza los headers de seguridad HTTP de una URL.

    Verifica la presencia y configuracion de headers de seguridad criticos como
    HSTS, CSP, X-Frame-Options, etc. Usa esta herramienta cuando el usuario quiera
    evaluar la seguridad de los headers HTTP de un sitio web.

    Args:
        url: La URL a analizar (ejemplo: 'https://example.com', 'https://google.com').

    Returns:
        dict: Analisis de headers de seguridad con recomendaciones.
    """
    try:
        import httpx
    except ImportError:
        return {
            "status": "error",
            "message": (
                "httpx no esta instalado. "
                "Instala con: pip install httpx"
            ),
        }

    SECURITY_HEADERS = {
        "strict-transport-security": {
            "name": "Strict-Transport-Security (HSTS)",
            "description": "Fuerza conexiones HTTPS. Previene ataques de downgrade.",
            "recommendation": "Agregar header: Strict-Transport-Security: max-age=31536000; includeSubDomains; preload",
        },
        "content-security-policy": {
            "name": "Content-Security-Policy (CSP)",
            "description": "Controla origenes de contenido permitidos. Previene XSS.",
            "recommendation": "Configurar CSP segun los recursos del sitio. Minimo: default-src 'self'",
        },
        "x-frame-options": {
            "name": "X-Frame-Options",
            "description": "Previene clickjacking al controlar el embedding en iframes.",
            "recommendation": "Agregar header: X-Frame-Options: DENY o SAMEORIGIN",
        },
        "x-content-type-options": {
            "name": "X-Content-Type-Options",
            "description": "Previene MIME-type sniffing.",
            "recommendation": "Agregar header: X-Content-Type-Options: nosniff",
        },
        "x-xss-protection": {
            "name": "X-XSS-Protection",
            "description": "Activa el filtro XSS del navegador (legacy, CSP es preferido).",
            "recommendation": "Agregar header: X-XSS-Protection: 1; mode=block",
        },
        "referrer-policy": {
            "name": "Referrer-Policy",
            "description": "Controla informacion del referrer enviada en requests.",
            "recommendation": "Agregar header: Referrer-Policy: strict-origin-when-cross-origin",
        },
        "permissions-policy": {
            "name": "Permissions-Policy",
            "description": "Controla APIs del navegador (camara, microfono, geolocalizacion).",
            "recommendation": "Configurar segun necesidades. Ejemplo: Permissions-Policy: camera=(), microphone=()",
        },
    }

    try:
        with httpx.Client(follow_redirects=True, timeout=10.0, verify=False) as client:
            response = client.get(url)
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error al conectar con '{url}': {e}",
        }

    headers_lower = {k.lower(): v for k, v in response.headers.items()}
    analysis = []
    present_count = 0

    for header_key, info in SECURITY_HEADERS.items():
        value = headers_lower.get(header_key)
        if value:
            present_count += 1
            analysis.append({
                "header": info["name"],
                "status": "present",
                "value": value,
                "description": info["description"],
            })
        else:
            analysis.append({
                "header": info["name"],
                "status": "missing",
                "description": info["description"],
                "recommendation": info["recommendation"],
            })

    total = len(SECURITY_HEADERS)
    score = f"{present_count}/{total}"

    if present_count == total:
        grade = "A"
    elif present_count >= 5:
        grade = "B"
    elif present_count >= 3:
        grade = "C"
    elif present_count >= 1:
        grade = "D"
    else:
        grade = "F"

    return {
        "status": "success",
        "url": url,
        "http_status": response.status_code,
        "server": headers_lower.get("server", "no reportado"),
        "security_score": score,
        "grade": grade,
        "headers_analysis": analysis,
    }

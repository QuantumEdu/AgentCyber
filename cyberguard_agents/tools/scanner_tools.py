"""
Herramientas de escaneo de puertos y vulnerabilidades con nmap real.

Usa python-nmap como wrapper del CLI de nmap.
Si nmap no esta instalado, retorna error descriptivo.
"""
import nmap


def scan_ports(target: str, port_range: str = "1-1024") -> dict:
    """
    Escanea puertos de un host objetivo usando nmap con deteccion de version de servicios.

    Usa esta herramienta cuando el usuario quiera escanear puertos de un host,
    verificar que servicios estan expuestos, o hacer reconocimiento de red.

    Args:
        target: La direccion IP o hostname a escanear (ejemplo: '192.168.1.1', 'scanme.nmap.org').
        port_range: Rango de puertos a escanear (ejemplo: '1-1024', '80,443', '22').

    Returns:
        dict: Resultado del escaneo con puertos abiertos y servicios detectados.
    """
    try:
        scanner = nmap.PortScanner()
    except nmap.PortScannerError:
        return {
            "status": "error",
            "message": (
                "nmap no esta instalado o no se encuentra en el PATH. "
                "Instala nmap: https://nmap.org/download.html — "
                "En Linux: sudo apt install nmap | En Windows: descarga el instalador desde nmap.org"
            ),
        }

    try:
        scanner.scan(hosts=target, ports=port_range, arguments="-sV")
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error ejecutando nmap: {e}",
        }

    if target not in scanner.all_hosts():
        return {
            "status": "success",
            "target": target,
            "port_range": port_range,
            "scan_type": "nmap_service_version",
            "open_ports_count": 0,
            "open_ports": [],
            "risk_summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
            "note": "Host no encontrado o no responde. Verifica la IP/hostname y conectividad.",
        }

    RISK_MAP = {
        21: "high", 22: "medium", 23: "critical", 25: "medium",
        53: "medium", 80: "high", 110: "medium", 135: "high",
        139: "high", 143: "medium", 443: "low", 445: "critical",
        993: "low", 995: "low", 1433: "critical", 1521: "critical",
        3306: "critical", 3389: "high", 5432: "critical", 5900: "high",
        6379: "critical", 8080: "medium", 8443: "low", 27017: "critical",
    }

    RECOMMENDATIONS = {
        21: "FTP es inseguro. Migrar a SFTP o FTPS.",
        22: "Verificar Protocol 2, deshabilitar root login, usar autenticacion por llave.",
        23: "Telnet transmite en texto plano. Deshabilitar y usar SSH.",
        25: "Verificar configuracion de relay abierto.",
        53: "Verificar que no sea un resolver abierto.",
        80: "Servicio sin cifrado. Redirigir a HTTPS.",
        135: "RPC expuesto. Restringir acceso por firewall.",
        139: "NetBIOS expuesto. Restringir acceso por firewall.",
        443: "Verificar certificado TLS y version del protocolo.",
        445: "SMB expuesto. Alto riesgo de exploits (EternalBlue). Restringir acceso.",
        1433: "MSSQL expuesto. No debe ser accesible externamente.",
        1521: "Oracle DB expuesta. Restringir acceso por IP.",
        3306: "MySQL expuesto. No debe ser accesible externamente.",
        3389: "RDP expuesto. Usar VPN o restringir por IP.",
        5432: "PostgreSQL expuesto. Restringir acceso por IP.",
        5900: "VNC expuesto. Usar tunel SSH o VPN.",
        6379: "Redis expuesto sin autenticacion por defecto. Critico.",
        8080: "Puerto alternativo HTTP. Verificar que servicio corre.",
        27017: "MongoDB expuesto. Configurar autenticacion y restringir acceso.",
    }

    open_ports = []
    host_info = scanner[target]

    for proto in host_info.all_protocols():
        for port in sorted(host_info[proto].keys()):
            port_data = host_info[proto][port]
            if port_data["state"] == "open":
                risk = RISK_MAP.get(port, "medium")
                recommendation = RECOMMENDATIONS.get(
                    port,
                    f"Verificar si el servicio {port_data.get('name', 'desconocido')} es necesario.",
                )
                open_ports.append({
                    "port": port,
                    "state": "open",
                    "service": port_data.get("name", "unknown"),
                    "version": port_data.get("version", ""),
                    "product": port_data.get("product", ""),
                    "risk_level": risk,
                    "recommendation": recommendation,
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
        "scan_type": "nmap_service_version",
        "nmap_command": scanner.command_line(),
        "open_ports_count": len(open_ports),
        "open_ports": open_ports,
        "risk_summary": risk_summary,
    }


def scan_vulnerabilities(target: str, port_range: str = "1-1024") -> dict:
    """
    Escanea un host en busca de vulnerabilidades conocidas usando scripts NSE de nmap.

    Usa esta herramienta cuando el usuario quiera detectar vulnerabilidades en un host,
    buscar CVEs conocidos, o hacer un analisis de seguridad mas profundo que un simple escaneo de puertos.

    Args:
        target: La direccion IP o hostname a escanear (ejemplo: '192.168.1.1', 'scanme.nmap.org').
        port_range: Rango de puertos a analizar (ejemplo: '1-1024', '80,443', '22').

    Returns:
        dict: Vulnerabilidades detectadas organizadas por puerto y servicio.
    """
    try:
        scanner = nmap.PortScanner()
    except nmap.PortScannerError:
        return {
            "status": "error",
            "message": (
                "nmap no esta instalado o no se encuentra en el PATH. "
                "Instala nmap: https://nmap.org/download.html — "
                "En Linux: sudo apt install nmap | En Windows: descarga el instalador desde nmap.org"
            ),
        }

    try:
        scanner.scan(hosts=target, ports=port_range, arguments="-sV --script vuln")
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error ejecutando nmap vuln scan: {e}",
        }

    if target not in scanner.all_hosts():
        return {
            "status": "success",
            "target": target,
            "port_range": port_range,
            "scan_type": "nmap_vuln_scripts",
            "vulnerabilities": [],
            "note": "Host no encontrado o no responde.",
        }

    vulnerabilities = []
    host_info = scanner[target]

    for proto in host_info.all_protocols():
        for port in sorted(host_info[proto].keys()):
            port_data = host_info[proto][port]
            if port_data["state"] != "open":
                continue

            script_results = port_data.get("script", {})
            for script_name, output in script_results.items():
                vulnerabilities.append({
                    "port": port,
                    "service": port_data.get("name", "unknown"),
                    "script": script_name,
                    "output": output,
                })

    # Also check host-level scripts
    if hasattr(host_info, "get") and "hostscript" in scanner._scan_result.get("scan", {}).get(target, {}):
        for script in scanner._scan_result["scan"][target]["hostscript"]:
            vulnerabilities.append({
                "port": "host",
                "service": "host-level",
                "script": script.get("id", "unknown"),
                "output": script.get("output", ""),
            })

    return {
        "status": "success",
        "target": target,
        "port_range": port_range,
        "scan_type": "nmap_vuln_scripts",
        "nmap_command": scanner.command_line(),
        "vulnerabilities_count": len(vulnerabilities),
        "vulnerabilities": vulnerabilities,
    }

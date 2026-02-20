"""
Herramientas para consulta y verificacion de CIS Benchmarks.

Las tools son funciones Python normales. ADK usa el docstring
y los type hints para que el LLM entienda CUANDO y COMO usar cada tool.
Las tools DEBEN retornar un diccionario.
"""
import subprocess
import platform

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
    Consulta un control especifico de CIS Benchmark por su ID.

    Usa esta herramienta cuando el usuario pregunte por un control CIS especifico,
    quiera saber los detalles de un benchmark, o necesite el comando de verificacion.

    Args:
        os_type: Sistema operativo. Puede ser 'linux' o 'windows'.
        benchmark_id: El identificador del benchmark CIS (ejemplo: '5.2.1', '1.1.1').

    Returns:
        dict: Informacion del benchmark o mensaje de error.
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
    opcionalmente filtrada por categoria.

    Usa esta herramienta cuando el usuario pida una lista de controles de seguridad,
    un checklist de hardening, o quiera ver todos los benchmarks de una categoria.

    Args:
        os_type: Sistema operativo. Puede ser 'linux' o 'windows'.
        category: Categoria a filtrar. Puede ser 'all', 'SSH Configuration',
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
            "message": f"Categoria '{category}' no encontrada. "
                       f"Disponibles: {', '.join(categories)}"
        }

    return {
        "status": "success",
        "os": os_type,
        "filter": category,
        "total_controls": len(results),
        "controls": results
    }


def run_cis_check(os_type: str, benchmark_id: str) -> dict:
    """
    Ejecuta el comando de verificacion real de un control CIS en el sistema local.

    Usa esta herramienta cuando el usuario quiera verificar si un control CIS especifico
    se cumple en el sistema actual. Ejecuta el check_command del benchmark en la maquina local.

    IMPORTANTE: Solo ejecuta comandos de verificacion (lectura), no modifica el sistema.

    Args:
        os_type: Sistema operativo. Puede ser 'linux' o 'windows'.
        benchmark_id: El identificador del benchmark CIS (ejemplo: '5.2.1', '1.1.1').

    Returns:
        dict: Resultado de la ejecucion del comando de verificacion.
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
    check_command = bm["check_command"]

    # Verificar que el OS del sistema coincide con el solicitado
    current_os = "windows" if platform.system() == "Windows" else "linux"
    if current_os != os_type:
        return {
            "status": "error",
            "message": (
                f"Este sistema es {current_os}, pero el check solicitado es para {os_type}. "
                f"El comando '{check_command}' no se puede ejecutar en este OS."
            ),
            "check_command": check_command,
            "benchmark": bm["title"],
        }

    try:
        shell = platform.system() == "Windows"
        result = subprocess.run(
            check_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return {
            "status": "success",
            "os": os_type,
            "id": benchmark_id,
            "title": bm["title"],
            "check_command": check_command,
            "exit_code": result.returncode,
            "stdout": result.stdout.strip() if result.stdout else "",
            "stderr": result.stderr.strip() if result.stderr else "",
            "passed": result.returncode == 0,
        }
    except subprocess.TimeoutExpired:
        return {
            "status": "error",
            "message": f"Timeout ejecutando '{check_command}' (limite: 30s)",
            "benchmark": bm["title"],
        }
    except FileNotFoundError:
        return {
            "status": "error",
            "message": f"Comando no encontrado: '{check_command}'. Verifica que las herramientas necesarias estan instaladas.",
            "benchmark": bm["title"],
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error ejecutando check: {e}",
            "check_command": check_command,
            "benchmark": bm["title"],
        }

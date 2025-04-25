import requests
import socket
from app.utils.env_config import require_env_var

# Obtener las variables de entorno (ya cargadas)
CONSUL_URL = require_env_var("CONSUL_ADDR")
PORT_INVENTORY = int(require_env_var("PORT_INVENTORY"))
ENV = require_env_var("ENV")

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return "127.0.0.1"

def register_service():
    service_id = "auth-service-1"
    service_data = {
        "ID": service_id,
        "Name": "auth-service",
        "Address": get_local_ip(),
        "Port": PORT_INVENTORY,
        "Check": {
            "HTTP": f"http://{get_local_ip()}:{PORT_INVENTORY}/health",
            "Interval": "10s",
            "Timeout": "1s"
        },
        "Tags": ["auth", "fastapi", "v1", f"env:{ENV}"],
        "Meta": {
            "version": "1.0.0",
            "maintainer": "infra@eztoplatform.com"
        }
    }

    try:
        res = requests.put(f"{CONSUL_URL}/v1/agent/service/register", json=service_data)
        print("[CONSUL] Registro exitoso." if res.status_code == 200 else f"[CONSUL] Error: {res.text}")
    except Exception as e:
        print(f"[CONSUL] Error de conexión: {e}")

def deregister_service():
    try:
        res = requests.put(f"{CONSUL_URL}/v1/agent/service/deregister/auth-service-1")
        print("[CONSUL] Desregistro exitoso." if res.status_code == 200 else f"[CONSUL] Error: {res.text}")
    except Exception as e:
        print(f"[CONSUL] Error al desregistrar: {e}")

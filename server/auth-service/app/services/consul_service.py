import requests
from app.utils.env_config import require_env_var

# Cargar las variables de entorno correctas
CONSUL_URL = require_env_var("CONSUL_ADDR")
PORT_AUTH = int(require_env_var("PORT_AUTH"))  # Este es 8006 según tu .env
ENV = require_env_var("ENV")

def register_service():
    service_id = "auth-service-1"
    service_data = {
        "ID": service_id,
        "Name": "auth-service",
        "Address": "auth-service",  # Nombre del contenedor en Docker Compose
        "Port": PORT_AUTH,
        "Check": {
            "HTTP": f"http://auth-service:{PORT_AUTH}/health",
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
        if res.status_code == 200:
            print("[CONSUL] Registro exitoso del auth-service.")
        else:
            print(f"[CONSUL] Error al registrar el auth-service: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[CONSUL] Error de conexión durante el registro: {e}")

def deregister_service():
    try:
        res = requests.put(f"{CONSUL_URL}/v1/agent/service/deregister/auth-service-1")
        if res.status_code == 200:
            print("[CONSUL] Desregistro exitoso del auth-service.")
        else:
            print(f"[CONSUL] Error al desregistrar el auth-service: {res.status_code} - {res.text}")
    except Exception as e:
        print(f"[CONSUL] Error de conexión durante el desregistro: {e}")

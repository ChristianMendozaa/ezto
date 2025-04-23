# app/services/consul_service.py
import requests
import socket

CONSUL_URL = "http://consul:8500"

def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return "127.0.0.1"

def register_service():
    service_id = "classes-service-1"  # Cambiado de auth-service-1
    service_data = {
        "ID": service_id,
        "Name": "classes-service",    # Cambiado de auth-service
        "Address": get_local_ip(),
        "Port": 8000,
        "Check": { 
            "HTTP": f"http://{get_local_ip()}:8000/health",
            "Interval": "10s",
            "Timeout": "1s"
        },
        "Tags": ["classes", "reservations", "fastapi", "v1", "env:dev"],  # Actualizados los tags
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
        res = requests.put(f"{CONSUL_URL}/v1/agent/service/deregister/classes-service-1")  # Cambiado el ID del servicio
        print("[CONSUL] Desregistro exitoso." if res.status_code == 200 else f"[CONSUL] Error: {res.text}")
    except Exception as e:
        print(f"[CONSUL] Error al desregistrar: {e}")
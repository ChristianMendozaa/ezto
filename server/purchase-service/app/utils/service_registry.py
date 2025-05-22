# app/utils/service_registry.py
import socket
import uuid
import logging
import requests

logger = logging.getLogger(__name__)

def register_service(consul_addr: str, service_name: str, service_port: int) -> str:
    """
    Registra el servicio en Consul y devuelve el service_id.
    """
    service_id = f"{service_name}-{uuid.uuid4()}"
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except:
        host_ip = "localhost"

    payload = {
        "ID": service_id,
        "Name": service_name,
        "Address": host_ip,
        "Port": service_port,
        "Check": {
            "HTTP": f"http://{host_ip}:{service_port}/health",
            "Interval": "10s",
            "Timeout": "5s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }
    try:
        url = f"{consul_addr}/v1/agent/service/register"
        resp = requests.put(url, json=payload, timeout=5)
        resp.raise_for_status()
        logger.info("Service registered in Consul: %s", service_id)
    except Exception as e:
        logger.exception("Error registering service in Consul: %s", e)
    return service_id

def deregister_service(consul_addr: str, service_id: str) -> None:
    """
    Elimina el registro del servicio en Consul.
    """
    try:
        url = f"{consul_addr}/v1/agent/service/deregister/{service_id}"
        resp = requests.put(url, timeout=5)
        resp.raise_for_status()
        logger.info("Service deregistered from Consul: %s", service_id)
    except Exception as e:
        logger.exception("Error deregistering service in Consul: %s", e)

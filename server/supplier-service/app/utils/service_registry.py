import socket
import os
import requests
import logging

logger = logging.getLogger(__name__)


def register_service(consul_addr: str, service_name: str, port: int) -> str:
    """
    Registra el servicio en Consul.

    Returns:
        service_id (str): ID único asignado.
    """
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = "localhost"

    service_id = f"{service_name}-{os.getenv('HOSTNAME', host_ip)}-{port}"
    payload = {
        "ID": service_id,
        "Name": service_name,
        "Address": host_ip,
        "Port": port,
        "Check": {
            "HTTP": f"http://{host_ip}:{port}/health",
            "Interval": "10s",
            "Timeout": "5s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }
    try:
        url = f"{consul_addr}/v1/agent/service/register"
        resp = requests.put(url, json=payload, timeout=5)
        if resp.ok:
            logger.info("Service registered with Consul: %s", service_id)
        else:
            logger.error("Failed to register service: %s", resp.text)
    except Exception as e:
        logger.exception("Error registering service with Consul: %s", e)

    return service_id


def deregister_service(consul_addr: str, service_id: str) -> None:
    """
    Elimina el servicio de Consul.
    """
    try:
        url = f"{consul_addr}/v1/agent/service/deregister/{service_id}"
        resp = requests.put(url, timeout=5)
        if resp.ok:
            logger.info("Service deregistered from Consul: %s", service_id)
        else:
            logger.error("Failed to deregister service: %s", resp.text)
    except Exception as e:
        logger.exception("Error deregistering service from Consul: %s", e)
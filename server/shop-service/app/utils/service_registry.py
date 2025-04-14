# app/utils/service_registry.py
import socket
import os
import requests
import logging

logger = logging.getLogger(__name__)

def register_service(service_name: str, port: int, discovery_url: str) -> None:
    """
    Registra el servicio en el sistema de service discovery (Consul).

    Args:
        service_name (str): El nombre del servicio a registrar (por ejemplo, "shop-service").
        port (int): El puerto en el que corre la instancia.
        discovery_url (str): URL del endpoint de registro del discovery.
    """
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = "localhost"
    
    payload = {
        "service_name": service_name,
        "address": host_ip,
        "port": port,
        "tags": [service_name]
    }
    
    try:
        response = requests.post(discovery_url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info("Service registered with Consul: %s", response.json())
        else:
            logger.error("Failed to register service with Consul: %s", response.text)
    except Exception as e:
        logger.exception("Exception when registering service with Consul: %s", str(e))

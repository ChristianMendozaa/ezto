# app/utils/service_registry.py
import os
import socket
import uuid
import requests
import logging

logger = logging.getLogger(__name__)

def register_service(consul_addr: str, service_name: str, service_port: int) -> str:
    service_id = f"{service_name}-{uuid.uuid4()}"
    payload = {
        "ID": service_id,
        "Name": service_name,
        "Address": socket.gethostbyname(socket.gethostname()),
        "Port": service_port,
        "Check": {
            "HTTP": f"http://{socket.gethostbyname(socket.gethostname())}:{service_port}/health",
            "Interval": "10s",
            "Timeout": "5s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }
    url = f"{consul_addr}/v1/agent/service/register"
    try:
        resp = requests.put(url, json=payload, timeout=5)
        if resp.ok:
            logger.info("Service registered in Consul: %s", service_id)
        else:
            logger.error("Consul register failed: %s", resp.text)
    except Exception as e:
        logger.exception("Error registering service in Consul: %s", e)
    return service_id

def deregister_service(consul_addr: str, service_id: str):
    url = f"{consul_addr}/v1/agent/service/deregister/{service_id}"
    try:
        resp = requests.put(url, timeout=5)
        if resp.ok:
            logger.info("Service deregistered from Consul: %s", service_id)
        else:
            logger.error("Consul deregister failed: %s", resp.text)
    except Exception as e:
        logger.exception("Error deregistering service in Consul: %s", e)

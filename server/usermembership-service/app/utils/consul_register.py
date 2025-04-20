# app/utils/consul_register.py
import socket
import atexit
from consul import Consul

def get_local_ip():
    return socket.gethostbyname(socket.gethostname())

def register_service_in_consul(service_name: str, service_port: int):
    consul_host = "consul"
    consul_port = 8500
    consul_client = Consul(host=consul_host, port=consul_port)

    hostname = socket.gethostname()
    service_id = f"{service_name}-{hostname}"
    address = get_local_ip()

    # Mensaje inicial
    print(f"🛰 Registrando servicio '{service_name}' en Consul en el puerto {service_port} (ID: {service_id})")

    # 🔎 Intentar desregistrar si ya existe el servicio
    try:
        services = consul_client.agent.services()
        if service_id in services:
            print(f"♻️  Ya existe el servicio '{service_id}', desregistrando primero...")
            consul_client.agent.service.deregister(service_id)
    except Exception as e:
        print(f"⚠️  Error al verificar servicios existentes: {e}")

    # ✅ Registrar nuevo servicio con chequeos
    try:
        consul_client.agent.service.register(
            name=service_name,
            service_id=service_id,
            address=address,
            port=service_port,
            check={
                "http": f"http://{address}:{service_port}/health",
                "tcp": f"{address}:{service_port}",
                "interval": "10s",
                "timeout": "3s",
                "deregister_critical_service_after": "1m"
            },
            tags=["fastapi", "v1", "env:dev"],
            meta={
                "version": "1.0.0",
                "maintainer": "infra@eztoplatform.com"
            }
        )

        print(f"✅ Servicio '{service_name}' registrado correctamente en Consul.")
    
    except Exception as e:
        print(f"❌ Error al registrar el servicio '{service_name}' en Consul: {e}")

    # 🧹 Desregistro automático al cerrar
    def deregister():
        try:
            consul_client.agent.service.deregister(service_id)
            print(f"🧹 Servicio '{service_id}' desregistrado correctamente de Consul.")
        except Exception as e:
            print(f"⚠️ Error al desregistrar '{service_id}': {e}")

    atexit.register(deregister)

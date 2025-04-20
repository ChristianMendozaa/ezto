import socket
from consul import Consul

def register_service_in_consul(service_name: str, service_port: int, service_id: str = None):
    consul_host = "consul"
    consul_port = 8500

    consul_client = Consul(host=consul_host, port=consul_port)

    if not service_id:
        service_id = f"{service_name}-{socket.gethostname()}"

    consul_client.agent.service.register(
        name=service_name,
        service_id=service_id,
        address=socket.gethostbyname(socket.gethostname()),
        port=service_port,
        check={
            "http": f"http://{socket.gethostbyname(socket.gethostname())}:{service_port}/health",
            "interval": "10s",
            "timeout": "3s"
        }
    )

    print(f"✅ Servicio '{service_name}' registrado en Consul.")

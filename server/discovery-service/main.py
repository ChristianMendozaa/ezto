# discovery-service/main.py

import os
import uuid
from datetime import datetime
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import consul

app = FastAPI(
    title="Service Discovery with Consul",
    description="Servicio de descubrimiento que utiliza Consul para registrar y consultar instancias de microservicios.",
    version="1.0.0"
)

# Modelo para la información de una instancia de servicio.
class ServiceInstance(BaseModel):
    instance_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Identificador único de la instancia")
    service_name: str = Field(..., description="Nombre del servicio (por ejemplo, 'auth', 'shop', etc.)")
    address: str = Field(..., description="Dirección IP o dominio de la instancia")
    port: int = Field(..., description="Puerto en el que el servicio escucha")
    tags: List[str] = Field(default=[], description="Lista de etiquetas (opcional)")
    registered_at: datetime = Field(default_factory=datetime.utcnow, description="Fecha y hora de registro")


# Configuración del cliente de Consul
CONSUL_HOST = os.getenv("CONSUL_HOST", "consul")  # Se asume que en docker-compose el host del contenedor Consul es "consul"
CONSUL_PORT = 8500
consul_client = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)

@app.post("/register", response_model=ServiceInstance, summary="Registrar un servicio")
async def register_service(instance: ServiceInstance):
    """
    Registra una nueva instancia de servicio en Consul.

    Se envía la información del servicio (nombre, dirección, puerto y etiquetas) y se utiliza la API del agente de Consul para
    registrar el servicio. La respuesta incluye el `instance_id` asignado y la fecha de registro.
    """
    try:
        # Registrar en Consul
        consul_client.agent.service.register(
            name=instance.service_name,
            service_id=instance.instance_id,
            address=instance.address,
            port=instance.port,
            tags=instance.tags
        )
        return instance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo registrar el servicio: {e}")

@app.post("/deregister", summary="Desregistrar una instancia de servicio")
async def deregister_service(service_name: str, instance_id: str):
    """
    Desregistra una instancia de servicio de Consul usando el `instance_id`.

    Se requiere el nombre del servicio para determinar cuál instancia eliminar.
    """
    try:
        consul_client.agent.service.deregister(instance_id)
        return {"message": f"Instancia {instance_id} de '{service_name}' desregistrada."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo desregistrar el servicio: {e}")

@app.get("/services/{service_name}", response_model=List[dict], summary="Listar instancias de un servicio")
async def list_service_instances(service_name: str):
    """
    Devuelve la lista de instancias registradas en Consul para un servicio dado.

    Se extrae la información almacenada en el agente de Consul y se filtra por el nombre del servicio.
    """
    try:
        # Obtén todos los servicios registrados
        services = consul_client.agent.services()
        filtered = [
            service for service in services.values() if service["Service"] == service_name
        ]
        if not filtered:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")
        return filtered
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener servicios: {e}")

# Endpoint de heartbeat (opcional)
@app.post("/heartbeat", summary="Actualizar heartbeat")
async def update_heartbeat(service_name: str, instance_id: str):
    """
    Actualiza el 'heartbeat' (latido) de una instancia de servicio.
    
    Aquí podrías implementar lógica adicional, por ejemplo, actualizando un campo en una base de datos o en Consul (si lo requieres).
    En este ejemplo solo se retorna un mensaje.
    """
    # En un caso real podrías, por ejemplo, volver a registrar el servicio o actualizar la marca de tiempo en una base de datos.
    return {"message": f"Heartbeat actualizado para {instance_id} de '{service_name}'."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=True)

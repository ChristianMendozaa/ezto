# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
import uuid
import threading

app = FastAPI(
    title="Service Discovery",
    description="Servidor de descubrimiento de servicios para arquitecturas de microservicios",
    version="1.0.0"
)

# Definición del modelo para una instancia de servicio.
class ServiceInstance(BaseModel):
    instance_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Identificador único de la instancia")
    service_name: str = Field(..., description="Nombre del servicio (por ejemplo, 'auth', 'shop', etc.)")
    host: str = Field(..., description="Dirección IP o dominio de la instancia")
    port: int = Field(..., description="Puerto de la instancia")
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow, description="Último latido recibido")

# Diccionario global para almacenar instancias de servicios, con lock para evitar condiciones de carrera.
registry_lock = threading.Lock()
service_registry: Dict[str, List[ServiceInstance]] = {}

@app.post("/register", response_model=ServiceInstance, summary="Registrar un servicio")
async def register_service(service: ServiceInstance):
    """
    Registra una nueva instancia del servicio en el registro.
    
    Cada servicio (cliente de discovery) se registra con su nombre, host, puerto y se genera un identificador único.
    """
    with registry_lock:
        if service.service_name not in service_registry:
            service_registry[service.service_name] = []
        service_registry[service.service_name].append(service)
    return service

@app.post("/deregister", summary="Deregister a service instance")
async def deregister_service(service_name: str, instance_id: str):
    """
    Dado el nombre del servicio y su instancia, elimina esa instancia del registro.
    """
    with registry_lock:
        if service_name in service_registry:
            original_count = len(service_registry[service_name])
            service_registry[service_name] = [inst for inst in service_registry[service_name] if inst.instance_id != instance_id]
            if len(service_registry[service_name]) < original_count:
                return {"message": "Service instance deregistered"}
    raise HTTPException(status_code=404, detail="Service instance not found")

@app.get("/services/{service_name}", response_model=List[ServiceInstance], summary="Listar instancias de un servicio")
async def list_service_instances(service_name: str):
    """
    Devuelve la lista de instancias registradas para un servicio dado.
    """
    with registry_lock:
        if service_name in service_registry:
            return service_registry[service_name]
    raise HTTPException(status_code=404, detail="Service not found")

@app.post("/heartbeat", summary="Actualizar heartbeat")
async def update_heartbeat(service_name: str, instance_id: str):
    """
    Actualiza el 'heartbeat' (latido) de una instancia de servicio para confirmar que sigue activa.
    """
    with registry_lock:
        if service_name in service_registry:
            for inst in service_registry[service_name]:
                if inst.instance_id == instance_id:
                    inst.last_heartbeat = datetime.utcnow()
                    return {"message": "Heartbeat updated"}
    raise HTTPException(status_code=404, detail="Service instance not found")

# Optional: Puedes agregar una tarea en segundo plano que limpie las instancias inactivas.
@app.on_event("startup")
async def startup_event():
    from asyncio import create_task, sleep

    async def cleanup_inactive_instances():
        while True:
            await sleep(30)  # Ejemplo: limpiar cada 30 segundos
            with registry_lock:
                for service, instances in list(service_registry.items()):
                    active_instances = [
                        inst for inst in instances 
                        if datetime.utcnow() - inst.last_heartbeat < timedelta(seconds=60)
                    ]
                    service_registry[service] = active_instances
            # Puedes agregar logging para saber que se ha limpiado
            print("Limpieza de instancias inactivas completada")

    create_task(cleanup_inactive_instances())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

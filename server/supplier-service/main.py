import os
import socket
import uuid
import requests
import logging
from fastapi import FastAPI, Request, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exceptions import RequestValidationError
from app.controllers.supplier_controller import router as supplier_router
from app.utils.service_registry import register_service, deregister_service

CONSUL_ADDR = os.getenv("CONSUL_ADDR", "http://consul:8500")
PORT = int(os.getenv("PORT", 8003))  # Ajusta según servicio
SERVICE_NAME = "supplier-service"         # Cambia según cada microservicio
service_id = None

@app.on_event("startup")
async def on_startup():
    global service_id
    service_id = register_service(CONSUL_ADDR, SERVICE_NAME, PORT)

@app.on_event("shutdown")
async def on_shutdown():
    if service_id:
        deregister_service(CONSUL_ADDR, service_id)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Supplier Service",
    description="Microservicio para gestión de proveedores",
    version="1.0.0",
    openapi_tags=[{"name":"Proveedores"}]
)

# Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail": "Error en la validación de datos."})

# Routers
app.include_router(supplier_router, prefix="/suppliers", tags=["Proveedores"])

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "supplier-service"}

# Registro en Consul
def register_service():
    consul_addr = os.getenv("CONSUL_ADDR", "http://consul:8500")
    service_id = f"supplier-service-{uuid.uuid4()}"
    payload = {
        "ID": service_id,
        "Name": "supplier-service",
        "Address": socket.gethostbyname(socket.gethostname()),
        "Port": int(os.getenv("PORT", 8003)),
        "Check": {
            "HTTP": f"http://{socket.gethostbyname(socket.gethostname())}:{os.getenv('PORT',8003)}/health",
            "Interval": "10s",
            "Timeout": "5s",
            "DeregisterCriticalServiceAfter": "1m"
        }
    }
    try:
        url = f"{consul_addr}/v1/agent/service/register"
        resp = requests.put(url, json=payload, timeout=5)
        if resp.ok:
            logger.info("Service registered: %s", service_id)
        else:
            logger.error("Fail to register service: %s", resp.text)
    except Exception as e:
        logger.exception("Consul registration error: %s", e)

@app.on_event("startup")
async def startup():
    register_service()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8003)), reload=True)
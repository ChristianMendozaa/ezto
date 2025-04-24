import os
import logging
from fastapi import FastAPI, Request, JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.controllers.purchase_controller import router as purchase_router
from app.utils.service_registry import register_service, deregister_service

# Configuración de logging
typelog = logging.getLogger("uvicorn")
logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s: %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Variables de entorno
autoenv = os.getenv
CONSUL_ADDR  = autoenv("CONSUL_ADDR", "http://consul:8500")
PORT         = int(autoenv("PORT", "8004"))
SERVICE_NAME = "purchase-service"
service_id   = None

# Instancia FastAPI
app = FastAPI(
    title="Purchase Service",
    description="Microservicio para gestión de ventas",
    version="1.0.0",
    openapi_tags=[{"name": "Compras"}]
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

# Handlers de errores
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail": "Error en la validación de datos."})

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(status_code=500, content={"detail": "Error interno, intente más tarde."})

# Rutas
app.include_router(purchase_router, prefix="/purchases", tags=["Compras"])

# Health check
@app.get("/health", tags=["Monitoreo"])
async def health_check():
    return {"status": "ok", "service": SERVICE_NAME}

# Eventos startup/shutdown para Consul
@app.on_event("startup")
async def on_startup():
    global service_id
    service_id = register_service(
        consul_addr=CONSUL_ADDR,
        service_name=SERVICE_NAME,
        service_port=PORT
    )
    logger.info(f"Registered service '{SERVICE_NAME}' in Consul with ID: {service_id}")

@app.on_event("shutdown")
async def on_shutdown():
    if service_id:
        deregister_service(CONSUL_ADDR, service_id)
        logger.info(f"Deregistered service '{SERVICE_NAME}' from Consul with ID: {service_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        reload=True
    )

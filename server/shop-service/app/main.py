# shop-service/app/main.py

import os, logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware

from app.controllers.product_controller import router as product_router
from app.utils.service_registry import register_service, deregister_service

# --- logging & config ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CONSUL_ADDR  = os.getenv("CONSUL_ADDR", "http://consul:8500")
PORT         = int(os.getenv("PORT", 8001))
SERVICE_NAME = "shop-service"
service_id   = None

# --- app ---
app = FastAPI(
  title="Productos Service",
  description="Microservicio para gestión de productos",
  version="1.0.0",
  openapi_tags=[{"name":"Productos"}]
)

# --- middlewares ---
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# --- errores ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(req: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}")
    return JSONResponse(status_code=422, content={"detail":"Error en la validación de datos."})

@app.exception_handler(Exception)
async def general_exception_handler(req: Request, exc: Exception):
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(status_code=500, content={"detail":"Error interno, intente más tarde."})

# --- rutas ---
app.include_router(product_router, prefix="/products", tags=["Productos"])

@app.get("/health", tags=["Monitoreo"])
async def health_check():
    return {"status":"ok","service":SERVICE_NAME}

# --- Consul ---
@app.on_event("startup")
async def on_startup():
    global service_id
    service_id = register_service(
      consul_addr=CONSUL_ADDR,
      service_name=SERVICE_NAME,
      service_port=PORT
    )

@app.on_event("shutdown")
async def on_shutdown():
    if service_id:
        deregister_service(CONSUL_ADDR, service_id)

if __name__=="__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)

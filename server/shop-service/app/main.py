# main.py (Microservicio de Shop con registro en Consul)
import os
import socket
import uuid
import requests
import logging
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Gestión de Inventario - Plataforma EzTo (Shop Service)",
    description="Microservicio para gestión de inventario y registro de compras en gimnasios.",
    version="1.0.0",
    contact={
        "name": "Equipo EzTo",
        "url": "https://eztoplatform.com/contact",
        "email": "support@eztoplatform.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {"name": "Productos", "description": "Gestión de productos del inventario"},
        {"name": "Compras", "description": "Registro y seguimiento de transacciones comerciales"},
        {"name": "Inventario", "description": "Operaciones de control de stock y movimientos"},
        {"name": "Proveedores", "description": "Gestión de proveedores"},
        {"name": "Reportes", "description": "Generación de reportes de inventario"},
    ]
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Middleware de seguridad de headers
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    security_headers = {
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "img-src 'self' data: https://fastapi.tiangolo.com; "
            "font-src 'self'; "
            "connect-src 'self'; "
            "frame-ancestors 'self';"
        ),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()"
    }
    response.headers.update(security_headers)
    return response

# Manejadores globales de errores (validación y generales)
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Error de validación: {exc}")
    return JSONResponse(
        status_code=422,
        content={"detail": "Error en la validación de los datos. Revisa la información enviada."}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrió un error interno. Por favor, intenta más tarde."}
    )

# Aquí se incluirían tus routers (productos, compras, inventario, proveedores)
from app.controllers.product_controller import router as product_router
from app.controllers.purchase_controller import router as purchase_router
from app.controllers.inventory_controller import router as inventory_router
from app.controllers.supplier_controller import router as supplier_router

app.include_router(product_router, prefix="/products", tags=["Productos"])
app.include_router(purchase_router, prefix="/purchases", tags=["Compras"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventario"])
app.include_router(supplier_router, prefix="/suppliers", tags=["Proveedores"])

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Monitoreo"])
async def health_check():
    return {"status": "ok", "service": "shop-service"}

# Función para registrar el servicio en Consul
def register_service_with_consul():
    # Obtén la URL de Consul desde la variable de entorno. Usa "consul" (nombre del servicio) en Docker Compose.
    consul_addr = os.getenv("CONSUL_ADDR", "http://localhost:8500")
    # El service_id se genera de forma única para este registro.
    service_id = f"shop-service-{str(uuid.uuid4())}"
    service_name = "shop-service"
    service_port = int(os.getenv("PORT", 8001))
    # Obtén la IP del contenedor o usa 'localhost' (nota: en Docker, hostname de shop-service es su contenedor)
    try:
        host_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        host_ip = "localhost"

    check = {
        "HTTP": f"http://{host_ip}:{service_port}/health",
        "Interval": "10s",
        "Timeout": "5s",
        "DeregisterCriticalServiceAfter": "1m"
    }
    payload = {
        "ID": service_id,
        "Name": service_name,
        "Address": host_ip,
        "Port": service_port,
        "Check": check
    }
    try:
        url = f"{consul_addr}/v1/agent/service/register"
        response = requests.put(url, json=payload, timeout=5)
        if response.status_code == 200:
            logger.info(f"Service registered with Consul: {response.json()} (ID: {service_id})")
        else:
            logger.error(f"Failed to register service with Consul: {response.status_code} {response.text}")
    except Exception as e:
        logger.exception("Exception when registering service with Consul: %s", str(e))

# Evento de startup para registrar el servicio en Consul
@app.on_event("startup")
async def startup_register_service():
    register_service_with_consul()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)

# main.py

from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, JSONResponse
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
import logging

# Middlewares personalizados
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.services.auth_service import AuthService
import os

# Controladores
from app.controllers.product_controller import router as product_router
from app.controllers.purchase_controller import router as purchase_router
from app.controllers.inventory_controller import router as inventory_router
from app.controllers.supplier_controller import router as supplier_router 

logging.basicConfig(level=logging.INFO)

app = FastAPI(
    title="Gestión de Inventario - Plataforma EzTo",
    description="Microservicio para gestión de inventario y registro de compras en gimnasios. "
                "Incluye control de stock, movimiento de productos y transacciones comerciales.",
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
    allow_origins=["http://localhost:3000"],  # Ajusta según tu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.dependency_overrides[AuthService.get_current_user] = AuthService.get_test_user

#app.add_middleware(RateLimitMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
#app.add_middleware(AuthMiddleware)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Ajusta si necesitas restringir hosts
)

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

# Manejador global de errores de validación
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logging.error(f"Error de validación: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Error en la validación de los datos. Revisa la información enviada.",
        }
    )

# Manejador global para todas las excepciones no controladas
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Error inesperado: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Ocurrió un error interno. Por favor, intenta más tarde."}
    )

# Registro de routers principales
app.include_router(product_router, prefix="/products", tags=["Productos"])
app.include_router(purchase_router, prefix="/purchases", tags=["Compras"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventario"])
app.include_router(supplier_router, prefix="/suppliers", tags=["Proveedores"])

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.get("/health", tags=["Monitoreo"])
async def health_check():
    return {"status": "ok", "service": "inventory-service"}

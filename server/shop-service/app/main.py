# main.py

from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

# Middlewares personalizados
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware

# Controladores
from app.controllers.product_controller import router as product_router
from app.controllers.purchase_controller import router as purchase_router
from app.controllers.inventory_controller import router as inventory_router
from app.controllers.supplier_controller import router as supplier_router 

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

# Middlewares esenciales
app.add_middleware(RateLimitMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(AuthMiddleware)
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
            "script-src 'self' 'unsafe-inline'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
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

# Registro de routers principales
app.include_router(product_router, prefix="/products", tags=["Productos"])
app.include_router(purchase_router, prefix="/purchases", tags=["Compras"])
app.include_router(inventory_router, prefix="/inventory", tags=["Inventario"])
app.include_router(supplier_router, prefix="/suppliers", tags=["Proveedores"])  

@app.get("/health", tags=["Monitoreo"])
async def health_check():
    return {"status": "ok", "service": "inventory-service"}


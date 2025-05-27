# main.py (Microservicio de membresías activas)
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from app.utils.consul_register import register_service_in_consul

from app.middleware.rate_limit_middleware import RateLimitMiddleware

# Controladores
from app.controllers.usermembership_controller import router as user_membership_router

# Manejo de errores
from app.utils.exception_handlers import global_exception_dispatcher, request_validation_exception_handler

from .config_loader import fetch_config, PROFILE

cfg = fetch_config()
# ahora vuelca cfg en variables de entorno o en tu pydantic BaseSettings
HOST = cfg.get("host", "0.0.0.0")
PORT = int(cfg.get("port", 8006))


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_service_in_consul("usermembership-service", 8006)
    yield
app = FastAPI(
    title="Gestión de Membresías Activas - Plataforma EzTo",
    description="Microservicio para la gestión de membresías activas de los usuarios dentro del sistema EzTo.",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/usermemberships",
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
        {"name": "Membresías", "description": "Endpoints relacionados con la gestión de membresías activas."},
    ]
)

# 🔐 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📈 GZIP para comprimir respuestas
app.add_middleware(GZipMiddleware, minimum_size=1000)
# 🔒 Autenticación y rate limiting
app.add_middleware(RateLimitMiddleware)

# 🛡️ Seguridad de cabeceras
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update({
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self' https://fastapi.tiangolo.com; "
            "font-src 'self' https://cdnjs.cloudflare.com; "
            "connect-src 'self'; "
            "frame-ancestors 'self'; "
            "form-action 'self'; "
            "base-uri 'self';"
        ),
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "geolocation=(), microphone=(), camera=()",
    })
    return response

# 🌍 Restricción de hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # En producción, reemplazar con dominios válidos
)

# ⚠️ Manejadores globales de excepciones
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_dispatcher)

app.include_router(user_membership_router, prefix="/usermemberships", tags=["Membresías"])

@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {"status": "ok"}
# 📌 Rutas del microservicio

@app.get("/config-health")
def config_health():
    # Devuelve el profile y todo el cfg para inspección
    return {"status": "up", "config_profile": PROFILE, "config": cfg}



# main.py (Microservicio de Membresías)

from fastapi import FastAPI, Request, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from contextlib import asynccontextmanager

from app.controllers.membership_controller import router as membership_router
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from fastapi.exceptions import RequestValidationError
from app.utils.exception_handlers import (
    global_exception_dispatcher,
    request_validation_exception_handler,
)
from app.utils.consul_register import register_service_in_consul

# configuración centralizada
from .config_loader import fetch_config, PROFILE

cfg = fetch_config()
HOST = cfg.get("host", "0.0.0.0")
PORT = int(cfg.get("port", 8007))


@asynccontextmanager
async def lifespan(app: FastAPI):
    register_service_in_consul("memberships-service", PORT)
    yield


app = FastAPI(
    title="Gestión de Planes de Membresía – Plataforma EzTo",
    description="Microservicio para la gestión de planes de membresía dentro del sistema EzTo.",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/memberships-plans",
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
        {
            "name": "Membresías",
            "description": "Endpoints relacionados con la gestión de planes de membresía.",
        }
    ],
)

# CORS: permitir llamadas desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# Compresión GZIP para respuestas grandes
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Encabezados de seguridad
@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers.update({
        "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
        "Content-Security-Policy": (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://cdnjs.cloudflare.com; "
            "img-src 'self'; "
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

# Hosts permitidos
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# Manejadores de excepción personalizados
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_dispatcher)

# Enrutar controladores
app.include_router(
    membership_router,
    prefix="/memberships-plans",
    tags=["Membresías"]
)

# Health checks
@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {"status": "ok"}

@app.get("/config-health", tags=["Monitoreo"])
def config_health():
    return {"status": "up", "config_profile": PROFILE, "config": cfg}


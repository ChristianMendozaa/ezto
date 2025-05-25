# main.py (Microservicio de Reservas)
from fastapi import FastAPI, Request

from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.controllers.reservation_controller import router as reservation_router
from fastapi.exceptions import RequestValidationError
from app.utils.exception_handlers import global_exception_dispatcher, request_validation_exception_handler
from app.utils.consul_register import register_service_in_consul

# Configuración centralizada
from .config_loader import fetch_config, PROFILE

cfg = fetch_config()
HOST = cfg.get("host", "0.0.0.0")
PORT = int(cfg.get("port", 8010))

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_service_in_consul("reservation-service", PORT)
    yield

app = FastAPI(
    title="Gestión de Reservas - Plataforma EzTo",
    description="Microservicio para la gestión de reservas en clases del gimnasio dentro del sistema EzTo.",
    version="1.0.0",
    lifespan=lifespan,
    root_path="/reservations",
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
        {"name": "Reservas", "description": "Endpoints relacionados con la gestión de reservas."},
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

# Middleware de Rate Limiting
app.add_middleware(RateLimitMiddleware)

# Middleware de GZIP
app.add_middleware(GZipMiddleware, minimum_size=1000)

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

# Middleware para restringir hosts permitidos
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# Manejadores de excepciones personalizados
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.add_exception_handler(Exception, global_exception_dispatcher)

# Incluir router de reservas
app.include_router(reservation_router, prefix="/reservations", tags=["Reservas"])

@app.get("/health", tags=["Monitoreo"])
def health_check():
    return {"status": "ok"}

@app.get("/config-health")
def config_health():
    return {"status": "up", "config_profile": PROFILE, "config": cfg}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host=HOST, port=PORT, reload=True)
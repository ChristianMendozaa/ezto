from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.controllers.register_controller import router as register_router
from app.controllers.protected_controller import router as protected_router
from app.controllers.auth_controller import router as auth_router
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.services.consul_service import register_service, deregister_service
from contextlib import asynccontextmanager

from app.config_loader import fetch_config, PROFILE

cfg = fetch_config()
# ahora vuelca cfg en variables de entorno o en tu pydantic BaseSettings
HOST = cfg.get("host", "0.0.0.0")
PORT = int(cfg.get("port", 8000))

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_service()
    yield
    deregister_service()

def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        title="Autenticación y Registro - Plataforma EzTo",
        description="Microservicio para autenticación y registro de usuarios con FastAPI y Firebase...",
        version="1.0.0",
        root_path="/auth",
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
            {"name": "Autenticación", "description": "Endpoints relacionados con autenticación y manejo de sesiones."},
            {"name": "Registro de Usuarios", "description": "Manejo de registro de nuevos usuarios en la plataforma."},
            {"name": "Rutas Protegidas", "description": "Endpoints protegidos que requieren autenticación."},
            {"name": "Logout", "description": "Cierre de sesión y eliminación de cookies de autenticación."},
        ],
        lifespan=lifespan if not testing else None
    )
    
    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:4000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Rate Limiting
    app.add_middleware(RateLimitMiddleware)

    # GZIP
    app.add_middleware(GZipMiddleware, minimum_size=1000)

    if not testing:
        app.add_middleware(AuthMiddleware)

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

    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"],
    )

    @app.get("/health", tags=["Monitoreo"])
    def health_check():
        return {"status": "ok"}
    
    @app.get("/config-health")
    def config_health():
        # Devuelve el profile y todo el cfg para inspección
        return {"status": "up", "config_profile": PROFILE, "config": cfg}

    # Routers
    app.include_router(register_router, tags=["Registro de Usuarios"])
    app.include_router(auth_router, tags=["Autenticación"])
    app.include_router(protected_router, tags=["Rutas Protegidas"])
    app.include_router(auth_router, tags=["Logout"])

    return app

# Ejecutable como servidor
app = create_app()

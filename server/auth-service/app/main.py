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

@asynccontextmanager
async def lifespan(app: FastAPI):
    register_service()
    yield
    deregister_service()

def create_app(testing: bool = False) -> FastAPI:
    app = FastAPI(
        title="Autenticación y Registro - Plataforma EzTo",
        description="Microservicio para autenticación y registro de usuarios con FastAPI y Firebase. "
                    "Incluye autenticación basada en JWT, protección de rutas y manejo de sesiones.",
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
        allow_origins=["http://localhost:3000"],
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

    # Routers
    app.include_router(register_router, prefix="/auth", tags=["Registro de Usuarios"])
    app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
    app.include_router(protected_router, prefix="/protected", tags=["Rutas Protegidas"])
    app.include_router(auth_router, prefix="/auth", tags=["Logout"])

    return app

# Ejecutable como servidor
app = create_app()

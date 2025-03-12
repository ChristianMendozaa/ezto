from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.controllers.register_controller import router as register_router
from app.controllers.login_controller import router as login_router
from app.middleware.auth_middleware import AuthMiddleware
from app.middleware.rate_limit_middleware import RateLimitMiddleware
from app.controllers.protected_controller import router as protected_router
from app.controllers.auth_controller import router as auth_router
from app.controllers.logout_controller import router as logout_router
from app.controllers.membership_controller import router as membership_router

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
        {"name": "Planes de Membresía", "description": "Gestión de planes de membresía y asignaciones."},
    ]
)

# Configuración de CORS para permitir el acceso desde el frontend autorizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Especificar el origen del frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos
    allow_headers=["*"],  # Permitir todos los headers
)

# Middleware de Rate Limiting
app.add_middleware(RateLimitMiddleware)

# Middleware de GZIP para comprimir respuestas (mínimo 1KB)
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Middleware de autenticación
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


# Middleware para restringir hosts permitidos
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],
)

# Inclusión de routers con prefijos y tags
app.include_router(register_router, prefix="/auth", tags=["Registro de Usuarios"])
app.include_router(login_router, prefix="/auth", tags=["Autenticación"])
app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])
app.include_router(protected_router, prefix="/protected", tags=["Rutas Protegidas"])
app.include_router(logout_router, prefix="/auth", tags=["Logout"])
app.include_router(membership_router, prefix="/membership", tags=["Planes de Membresía"])
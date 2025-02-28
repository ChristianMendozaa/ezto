from fastapi import FastAPI
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from app.controllers.register_controller import router as register_router
from datetime import datetime

class RateLimitMiddleware(BaseHTTPMiddleware):
    rate_limit = {}
    max_requests = 10
    window_seconds = 60

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        
        # Asignar el timestamp actual al request.state
        request.state.timestamp = datetime.utcnow().timestamp()

        if client_ip not in self.rate_limit:
            self.rate_limit[client_ip] = []
        
        # Limpiar las solicitudes fuera de la ventana de tiempo permitida
        self.rate_limit[client_ip] = [
            timestamp for timestamp in self.rate_limit[client_ip]
            if timestamp > request.state.timestamp - self.window_seconds
        ]

        # Validar el límite de solicitudes permitidas
        if len(self.rate_limit[client_ip]) >= self.max_requests:
            from starlette.responses import JSONResponse
            return JSONResponse({"detail": "Rate limit exceeded."}, status_code=429)

        # Registrar la solicitud actual
        self.rate_limit[client_ip].append(request.state.timestamp)

        # Continuar con la solicitud
        response = await call_next(request)
        return response

app = FastAPI(
    title="Registro de Usuarios - Plataforma EzTo",
    description="Microservicio para el registro de usuarios con FastAPI y Firebase.",
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
)

# CORS seguro: permitir solo el frontend autorizado
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://eztoplatform.com", "http://localhost:3000"],  # Dominios permitidos
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "Accept"],
)

# Middleware para limitar la tasa de solicitudes (Rate Limiting)
app.add_middleware(RateLimitMiddleware)

# Middleware de GZIP para comprimir respuestas grandes
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Cabeceras de seguridad adicionales
@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline';"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response

# Middleware para permitir solo hosts de confianza (opcional)
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["eztoplatform.com", "localhost", "*.eztoplatform.com"],
)

# Redirección a HTTPS en producción
# app.add_middleware(HTTPSRedirectMiddleware)

# Incluir las rutas del registro de usuarios
app.include_router(register_router, prefix="/auth", tags=["Registro de Usuarios"])

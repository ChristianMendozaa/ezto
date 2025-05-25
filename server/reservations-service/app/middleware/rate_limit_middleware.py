# app/middleware/rate_limit_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from datetime import datetime

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para limitar la tasa de peticiones por IP (Rate Limiting).
    max_requests: número máximo de peticiones
    window_seconds: ventana de tiempo en segundos
    """
    rate_limit_data = {}
    max_requests = 100
    window_seconds = 60

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_timestamp = datetime.utcnow().timestamp()

        if client_ip not in self.rate_limit_data:
            self.rate_limit_data[client_ip] = []

        # Filtrar timestamps antiguos fuera de la ventana
        self.rate_limit_data[client_ip] = [
            ts for ts in self.rate_limit_data[client_ip]
            if ts > current_timestamp - self.window_seconds
        ]

        # Verificar si alcanzó el límite
        if len(self.rate_limit_data[client_ip]) >= self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded."}, status_code=429)

        # Registrar la nueva petición
        self.rate_limit_data[client_ip].append(current_timestamp)

        response = await call_next(request)
        return response

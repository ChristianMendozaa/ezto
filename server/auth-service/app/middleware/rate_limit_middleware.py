from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from datetime import datetime, UTC

class RateLimitMiddleware(BaseHTTPMiddleware):
    rate_limit = {}
    max_requests = 100
    window_seconds = 60

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        request.state.timestamp = datetime.now(UTC).timestamp()

        if client_ip not in self.rate_limit:
            self.rate_limit[client_ip] = []
        
        # Filtrar solicitudes dentro de la ventana de tiempo
        self.rate_limit[client_ip] = [
            timestamp for timestamp in self.rate_limit[client_ip]
            if timestamp > request.state.timestamp - self.window_seconds
        ]

        if len(self.rate_limit[client_ip]) >= self.max_requests:
            return JSONResponse({"detail": "Rate limit exceeded."}, status_code=429)

        self.rate_limit[client_ip].append(request.state.timestamp)
        response = await call_next(request)
        return response

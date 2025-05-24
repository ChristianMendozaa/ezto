from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from datetime import datetime

class RateLimitMiddleware(BaseHTTPMiddleware):
    rate_limit = {}
    max_requests = 100
    window_seconds = 60

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            return response

        client_ip = request.client.host
        request.state.timestamp = datetime.utcnow().timestamp()

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

        # Agregar encabezados CORS a la respuesta
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

        return response

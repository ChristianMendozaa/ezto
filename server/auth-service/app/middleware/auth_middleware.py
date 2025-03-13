from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from firebase_admin import auth

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware para autenticar usuarios mediante Firebase Authentication.
        Extrae el token desde la cookie y lo verifica.
        """
        # Lista de rutas públicas que no requieren autenticación
        public_routes = ["/auth/login", "/auth/register", "/auth/logout"]

        # Si la solicitud es a una ruta pública, continuar sin autenticación
        if request.url.path in public_routes:
            return await call_next(request)

        # Intentar obtener el token desde las cookies o headers
        token = request.cookies.get("authToken")
        if not token:
            token = request.headers.get("Cookie")
            if token and "authToken=" in token:
                token = token.split("authToken=")[-1].split(";")[0]

        # Si no hay token, bloquear la solicitud
        if not token:
            raise HTTPException(status_code=401, detail="Token no proporcionado")

        try:
            # Verificar el token con Firebase Authentication
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token  # Guardar info del usuario en la solicitud
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        return await call_next(request)

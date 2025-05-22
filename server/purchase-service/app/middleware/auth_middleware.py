# app/middleware/auth_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from firebase_admin import auth
import logging

logging.basicConfig(level=logging.INFO)

class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware de autenticación para verificar el token JWT de Firebase en la cookie 'authToken'.
    Si el token está ausente, la solicitud continúa, pero sin credenciales de usuario.
    Si el token existe y es inválido, lanza un HTTPException 401.
    """
    async def dispatch(self, request: Request, call_next):
        token = request.cookies.get("authToken")

        # Si no encuentra la cookie, buscar en headers "Cookie"
        if not token:
            raw_cookie = request.headers.get("Cookie", "")
            if "authToken=" in raw_cookie:
                try:
                    token = raw_cookie.split("authToken=")[-1].split(";")[0]
                except Exception:
                    pass
        
        if token:
            try:
                decoded_token = auth.verify_id_token(token)
                request.state.user = decoded_token
            except Exception as e:
                logging.error(f"Error en la verificación del token: {e}")
                raise HTTPException(status_code=401, detail="Token inválido o expirado")
        else:
            # No se encontró token, la solicitud sigue pero sin user autenticado
            request.state.user = None

        response = await call_next(request)
        return response

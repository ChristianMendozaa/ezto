<<<<<<< HEAD
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
        # Permitir solicitudes OPTIONS sin interrupción
        if request.method == "OPTIONS":
            return await call_next(request)

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
                logging.warning(f"Token inválido o ausente: {e}")
                request.state.user = None  # Permitir que la solicitud continúe sin usuario autenticado

        else:
            request.state.user = None

        response = await call_next(request)

        # Asegurar que las respuestas tengan los encabezados CORS correctos
        response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"

        return response
=======
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
>>>>>>> afb75bf933e10a27a8164a48c8899b5b816ddf92

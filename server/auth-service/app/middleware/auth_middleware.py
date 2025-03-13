from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from firebase_admin import auth

EXCLUDED_PATHS = ["/auth/logout"]  # Rutas excluidas del middleware

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware para autenticar usuarios mediante Firebase Authentication.
        Extrae el token desde la cookie y lo verifica.
        """

        # 🔥 1. Verificar si la ruta está en la lista de exclusión
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)  # Permitir el acceso sin autenticación

        # 🔥 2. Intentar obtener el token desde las cookies o los headers
        token = request.cookies.get("authToken")

        if not token:
            token = request.headers.get("Cookie")  # Intentar obtenerla desde los headers

            if token and "authToken=" in token:
                token = token.split("authToken=")[-1].split(";")[0]  # Extraer el valor

        # 🔥 3. Si no hay token, permitir que la solicitud pase sin bloquearla
        if not token:
            return await call_next(request)

        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token  # Guardar info del usuario en la solicitud
        except Exception:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        return await call_next(request)

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from firebase_admin import auth

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """
        Middleware para autenticar usuarios mediante Firebase Authentication.
        Extrae el token desde la cookie y lo verifica.
        """
        token = request.cookies.get("authToken")  # Intentar obtener la cookie

        if not token:
            token = request.headers.get("Cookie")  # Intentar obtenerla desde los headers

            if token and "authToken=" in token:
                token = token.split("authToken=")[-1].split(";")[0]  # Extraer el valor


        if not token:
            return await call_next(request)  # No bloquear la solicitud

        try:
            decoded_token = auth.verify_id_token(token)
            request.state.user = decoded_token  # Guardar info del usuario en la solicitud
        except Exception as e:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        return await call_next(request)

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.keycloak_config import keycloak_openid
import logging

logger = logging.getLogger(__name__)

EXCLUDED_PATHS = [
    "/auth/register", "/register",
    "/auth/login",    "/login",
    "/auth/logout",   "/logout",
    "/health",        "/auth/health",
]



class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in EXCLUDED_PATHS:
            return await call_next(request)

        token = request.cookies.get("authToken")

        if not token:
            cookie_header = request.headers.get("Cookie", "")
            if "authToken=" in cookie_header:
                token = cookie_header.split("authToken=")[-1].split(";")[0]

        if not token:
            return await call_next(request)  # Permitir acceso a rutas públicas

        try:
            token_info = keycloak_openid.introspect(token)

            if not token_info.get("active"):
                raise Exception("Token inactivo")

            # Guardamos los datos del token para su uso posterior
            request.state.user = {
                "user_id": token_info.get("sub"),
                "email": token_info.get("email"),
                "username": token_info.get("preferred_username"),
                "role": token_info.get("user_type", "gym_member")
            }

        except Exception as e:
            logger.warning(f"Token inválido: {e}")
            return JSONResponse(
                status_code=401,
                content={
                    "success": False,
                    "data": None,
                    "error": "Token inválido o expirado"
                }
            )

        return await call_next(request)

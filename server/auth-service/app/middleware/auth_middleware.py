from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.keycloak_config import keycloak_openid
import logging

logger = logging.getLogger(__name__)

# Las rutas públicas SIN importar el root_path
EXCLUDED_PATHS = ["/logout", "/register", "/login", "/health", "/docs", "/openapi.json"]

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        full_path = request.scope.get("root_path", "") + request.scope.get("path", "")
        logger.debug(f"AuthMiddleware - Path recibido: {full_path}")

        # Verifica si alguna ruta excluida es el final del path (soporta root_path)
        if any(full_path.endswith(path) for path in EXCLUDED_PATHS):
            logger.debug("Ruta pública, permitiendo sin autenticación.")
            return await call_next(request)

        # Buscar el token en las cookies
        token = request.cookies.get("authToken")

        # (Opcional) También buscar en headers por si estás debuggeando en Postman
        if not token:
            cookie_header = request.headers.get("Cookie", "")
            if "authToken=" in cookie_header:
                token = cookie_header.split("authToken=")[-1].split(";")[0]

        if not token:
            logger.warning("Token ausente en cookies o headers.")
            return JSONResponse(
                status_code=401,
                content={"success": False, "data": None, "error": "Token no proporcionado"}
            )

        try:
            token_info = keycloak_openid.introspect(token)

            if not token_info.get("active"):
                logger.warning("Token inactivo o expirado.")
                raise Exception("Token inactivo")

            # Guardar los datos del usuario en request.state.user
            request.state.user = {
                "user_id": token_info.get("sub"),
                "email": token_info.get("email"),
                "username": token_info.get("preferred_username"),
                "role": token_info.get("realm_access", {}).get("roles", [])
            }

            logger.debug(f"Usuario autenticado: {request.state.user}")

        except Exception as e:
            logger.warning(f"Token inválido o error al validar: {e}")
            return JSONResponse(
                status_code=401,
                content={"success": False, "data": None, "error": "Token inválido o expirado"}
            )

        return await call_next(request)

from fastapi import Request, HTTPException
from app.utils.keycloak_config import keycloak_openid
import logging

class AuthService:
    @staticmethod
    async def get_current_user(request: Request) -> dict:
        token = None

        # Extraer token de la cookie o header Authorization
        if "Authorization" in request.headers:
            auth_header = request.headers.get("Authorization")
            if auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
        elif "authToken" in request.cookies:
            token = request.cookies.get("authToken")

        if not token:
            raise HTTPException(status_code=401, detail="Token no proporcionado")

        try:
            token_info = keycloak_openid.introspect(token)
            if not token_info.get("active"):
                raise HTTPException(status_code=401, detail="Token inactivo")

            return {
                "user_id": token_info.get("sub"),
                "email": token_info.get("email"),
                "username": token_info.get("preferred_username"),
                "role": token_info.get("user_type", "gym_member"), 
            }

        except Exception as e:
            logging.exception("Error al validar token con Keycloak")
            raise HTTPException(status_code=401, detail="Token inválido")

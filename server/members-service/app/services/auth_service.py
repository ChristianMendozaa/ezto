# app/services/auth_service.py
import logging
import requests
from fastapi import HTTPException, Request
from jose import jwt, JWTError
from app.config_loader import fetch_config

logger = logging.getLogger("app.services.auth_service")

cfg = fetch_config().get("keycloak", {})

INTERNAL_KEYCLOAK_URL = "http://traefik/keycloak"                    # usado para requests dentro del contenedor
EXTERNAL_KEYCLOAK_URL = cfg["url"].rstrip("/")                     # usado para validar "iss"
REALM = cfg["realm"]

JWKS_URL = f"{INTERNAL_KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
ISSUER   = f"{EXTERNAL_KEYCLOAK_URL}/realms/{REALM}"

class AuthService:

    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")

        token = auth_header.split(" ", 1)[1]
        logger.info("Verifying token…")

        # Extraer header sin verificar
        try:
            unverified_header = jwt.get_unverified_header(token)
        except JWTError:
            raise HTTPException(status_code=401, detail="Token inválido o malformado")

        # Obtener JWKS
        try:
            jwks = requests.get(JWKS_URL, timeout=5).json()
        except Exception:
            logger.exception("No se pudo obtener JWKS")
            raise HTTPException(status_code=500, detail="Error autenticando")

        # Buscar clave
        kid = unverified_header.get("kid")
        key_dict = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key_dict:
            raise HTTPException(status_code=401, detail="Clave pública no encontrada")

        # Verificar token
        try:
            decoded = jwt.decode(
                token,
                key=key_dict,
                algorithms=["RS256"],
                issuer=ISSUER,
                options={"verify_aud": False}
            )
        except JWTError as e:
            logger.error("Error al verificar JWT: %s", e)
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        sub   = decoded.get("sub")
        email = decoded.get("email", "")
        roles = decoded.get("realm_access", {}).get("roles", [])
        role  = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {"user_id": sub, "email": email, "role": role}
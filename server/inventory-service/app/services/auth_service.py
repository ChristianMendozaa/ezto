# app/services/auth_service.py
import os
import logging
import requests
from fastapi import HTTPException, Request
from jose import jwt, JWTError

logger = logging.getLogger("app.services.auth_service")

# Construye la URL de JWKS de tu realm
KEYCLOAK_URL  = os.getenv("KEYCLOAK_SERVER_URL").rstrip("/")
REALM         = os.getenv("KEYCLOAK_REALM")
JWKS_URL      = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
ISSUER        = f"{KEYCLOAK_URL}/realms/{REALM}"

class AuthService:

    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        logger.debug("Received Authorization header: %r", auth_header)
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")

        token = auth_header.split(" ", 1)[1]
        logger.info("Verifying token…")

        # 1) Cargar JWKS
        try:
            jwks = requests.get(JWKS_URL, timeout=5).json()
        except Exception as e:
            logger.exception("No pude descargar JWKS")
            raise HTTPException(status_code=500, detail="Authentication backend error")

        # 2) Buscar la clave pública correcta
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        key_dict = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key_dict:
            logger.error("No hallé la clave JWKS para kid=%s", kid)
            raise HTTPException(status_code=401, detail="Invalid token")

        # 3) Verificar firma + issuer + exp
        try:
            decoded = jwt.decode(
            token,
            key=key_dict,
            algorithms=["RS256"],
            options={"verify_aud": False, "verify_iss": False}
        )

            logger.info("Token verificado OK: sub=%s", decoded.get("sub"))
        except JWTError as e:
            logger.error("Error al verificar JWT: %s", e)
            raise HTTPException(status_code=401, detail="Token invalid or expired")

        # 4) Extraer usuario y roles
        sub   = decoded.get("sub")
        email = decoded.get("email", "")
        roles = decoded.get("realm_access", {}).get("roles", [])
        role  = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {"user_id": sub, "email": email, "role": role}

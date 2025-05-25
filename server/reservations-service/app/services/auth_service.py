# app/services/auth_service.py
import logging
import requests
from fastapi import HTTPException, Request
from jose import jwt, JWTError

from app.config_loader import fetch_config, decrypt_value

logger = logging.getLogger("app.services.auth_service")

# 1) Baja la sección "keycloak" de tu Config-Server
cfg = fetch_config().get("keycloak", {})

# 2) Extrae los valores no cifrados
KEYCLOAK_URL = cfg["url"].rstrip("/")            # p.ej. "http://keycloak:8080"
REALM        = cfg["realm"]                      # p.ej. "master"

# 3) Construye JWKS y issuer desde la configuración
JWKS_URL = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/certs"
ISSUER   = f"{KEYCLOAK_URL}/realms/{REALM}"

class AuthService:

    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        logger.debug("Received Authorization header: %r", auth_header)
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")

        token = auth_header.split(" ", 1)[1]
        logger.info("Verifying token…")

        # 1) Descargar JWKS
        try:
            jwks = requests.get(JWKS_URL, timeout=5).json()
        except Exception:
            logger.exception("No pude descargar JWKS")
            raise HTTPException(status_code=500, detail="Authentication backend error")

        # 2) Busca la clave pública correcta por 'kid'
        unverified_header = jwt.get_unverified_header(token)
        kid = unverified_header.get("kid")
        key_dict = next((k for k in jwks["keys"] if k["kid"] == kid), None)
        if not key_dict:
            logger.error("No hallé la clave JWKS para kid=%s", kid)
            raise HTTPException(status_code=401, detail="Invalid token")

        # 3) Verifica firma, issuer y expiración
        try:
            decoded = jwt.decode(
                token,
                key=key_dict,
                algorithms=["RS256"],
                issuer=ISSUER,
                options={"verify_aud": False}
            )
            logger.info("Token verificado OK: sub=%s", decoded.get("sub"))
        except JWTError as e:
            logger.error("Error al verificar JWT: %s", e)
            raise HTTPException(status_code=401, detail="Token invalid or expired")

        # 4) Extrae usuario y roles
        sub   = decoded.get("sub")
        email = decoded.get("email", "")
        roles = decoded.get("realm_access", {}).get("roles", [])
        # adapta esta lógica a tus roles reales
        role  = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {"user_id": sub, "email": email, "role": role}

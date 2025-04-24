# inventory-service/app/services/auth_service.py
import os
from fastapi import HTTPException, Request
from keycloak import KeycloakOpenID
from jose import JWTError

# Cargamos directo desde las env vars (Docker ya las inyecta)
KEYCLOAK_URL    = os.getenv("KEYCLOAK_URL")      # ej: http://keycloak:8080/
KEYCLOAK_REALM  = os.getenv("KEYCLOAK_REALM")    # ej: master
KEYCLOAK_CLIENT = os.getenv("KEYCLOAK_CLIENT_ID")
KEYCLOAK_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET")  # puede ser None

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_URL,
    realm_name=KEYCLOAK_REALM,
    client_id=KEYCLOAK_CLIENT,
    client_secret_key=KEYCLOAK_SECRET,  # omitir si cliente público
    verify=True
)

class AuthService:
    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")
        token = auth_header.split(" ", 1)[1]

        # 1) Introspección para validar token
        intros = keycloak_openid.introspect(token)
        if not intros.get("active"):
            raise HTTPException(status_code=401, detail="Token invalid or expired")

        # 2) Decodificar para extraer claims / roles
        try:
            decoded = keycloak_openid.decode_token(
                token,
                key=keycloak_openid.public_key(),
                options={"verify_signature": True, "exp": True}
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Token signature error")

        user_id = decoded.get("sub")
        email   = decoded.get("email")
        roles   = decoded.get("realm_access", {}).get("roles", [])
        role    = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {"user_id": user_id, "email": email, "role": role}

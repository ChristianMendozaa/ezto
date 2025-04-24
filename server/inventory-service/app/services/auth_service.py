# app/services/auth_service.py
import os
from fastapi import HTTPException, Request
from keycloak import KeycloakOpenID
from jose import JWTError

# ya lo tenías bien cargado de ENV
keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"),
    realm_name=os.getenv("KEYCLOAK_REALM"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),  # opcional para token endpoint
    verify=True
)

class AuthService:
    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")
        token = auth_header.split(" ", 1)[1]

        try:
            # Decodifica y verifica firma + expiration usando la public key de Keycloak
            decoded = keycloak_openid.decode_token(
                token,
                key=keycloak_openid.public_key(),
                options={"verify_signature": True, "verify_exp": True}
            )
        except JWTError:
            raise HTTPException(status_code=401, detail="Token invalid or expired")

        user_id = decoded.get("sub")
        email   = decoded.get("email")
        roles   = decoded.get("realm_access", {}).get("roles", [])
        role    = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {"user_id": user_id, "email": email, "role": role}

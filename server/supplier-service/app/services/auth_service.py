# app/services/auth_service.py
import os
import logging
from fastapi import HTTPException, Request
from keycloak import KeycloakOpenID
from jose import JWTError

logging.basicConfig(level=logging.INFO)

keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("KEYCLOAK_SERVER_URL"),
    realm_name=os.getenv("KEYCLOAK_REALM"),
    client_id=os.getenv("KEYCLOAK_CLIENT_ID"),
    client_secret_key=os.getenv("KEYCLOAK_CLIENT_SECRET"),
    verify=True
)

class AuthService:
    @staticmethod
    async def get_current_user(request: Request) -> dict:
        auth_header = request.headers.get("Authorization", "")
        logging.debug(f"Received Authorization header: {auth_header!r}")
        if not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token missing")

        token = auth_header.split(" ", 1)[1]
        logging.info(f"Verifying token…")

        # 1) Introspección
        intros = keycloak_openid.introspect(token)
        logging.debug(f"Introspect response: {intros}")
        if not intros.get("active"):
            raise HTTPException(status_code=401, detail="Token invalid or expired")

        # 2) Decodificación
        try:
            public_key = keycloak_openid.public_key()
            decoded = keycloak_openid.decode_token(token, key=public_key)
            logging.info(f"Token decoded: sub={decoded.get('sub')}, email={decoded.get('email')}")
        except JWTError as e:
            logging.error(f"Token decode error: {e}")
            raise HTTPException(status_code=401, detail="Token signature error")
        except Exception as e:
            logging.error(f"Unexpected decode error: {e}")
            raise HTTPException(status_code=401, detail="Authentication failed")

        # 3) Mapea rol
        roles = decoded.get("realm_access", {}).get("roles", [])
        role = "gym_owner" if "gym_owner" in roles else "gym_member"

        return {
            "user_id": decoded.get("sub"),
            "email": decoded.get("email"),
            "role": role
        }

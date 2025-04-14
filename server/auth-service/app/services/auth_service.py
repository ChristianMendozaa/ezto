from fastapi import HTTPException, Request
from app.utils.firebase_config import db
from keycloak import KeycloakAdmin, KeycloakOpenID

import logging

logger = logging.getLogger(__name__)

class AuthService:

    @staticmethod
    async def get_current_user(request: Request):
        token = request.cookies.get("authToken")  # 👈 Leer desde cookie

        if not token:
            logger.warning("⚠️ No se encontró la cookie authToken")
            raise HTTPException(status_code=401, detail="Token ausente o inválido")

        return await AuthService.verify_token(token)

    @staticmethod
    async def verify_token(token: str):
        try:
            keycloak_openid = KeycloakOpenID(
                server_url="http://keycloak:8080/",
                realm_name="master",
                client_id="ezto-client",
                client_secret_key="ezto-secret",
                verify=False
            )
            logger.info("🔍 Verificando token con Keycloak (introspect)...")
            token_info = keycloak_openid.introspect(token)
            logger.debug(f"Resultado introspect: {token_info}")

            if not token_info.get("active"):
                logger.warning("⚠️ Token no activo")
                raise HTTPException(status_code=401, detail="Token inválido o expirado")

        except Exception as e:
            logger.error(f"❌ Error al verificar el token con Keycloak: {e}")
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        user_id = token_info.get("sub")
        if not user_id:
            logger.warning("⚠️ Token sin sub (ID de usuario)")
            raise HTTPException(status_code=401, detail="Token inválido (sin sub)")

        try:
            user_doc = db.collection("users").document(user_id).get()
        except Exception as e:
            logger.error(f"🔥 Error al acceder a Firestore: {e}")
            raise HTTPException(status_code=500, detail="Error al acceder a la base de datos")

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        user_data = user_doc.to_dict()
        user_type = user_data.get("user_type", "gym_member")   
                           
        return {
            "user_id": user_id,
            "email": token_info.get("email", ""),
            "role": user_type
        }
                            
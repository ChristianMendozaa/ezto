from fastapi import HTTPException, Request
from app.utils.firebase_config import db
from app.utils.keycloak_config import keycloak_openid

class AuthService:

    @staticmethod
    async def get_current_user(request: Request):
        token = request.cookies.get("authToken")

        if not token:
            raise HTTPException(status_code=401, detail="Token ausente o inválido")

        return await AuthService.verify_token(token)

    @staticmethod
    async def verify_token(token: str):
        try:
            # Usar introspect de Keycloak para validar el token
            token_info = keycloak_openid.introspect(token)

            if not token_info.get("active"):
                raise HTTPException(status_code=401, detail="Token inválido o expirado")

        except Exception as e:
            raise HTTPException(status_code=401, detail="Error al validar el token con Keycloak")

        user_id = token_info.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido (sin sub)")

        # Leer los roles desde el resultado de introspection
        roles = token_info.get("realm_access", {}).get("roles", [])

        if "gym_owner" in roles:
            user_type = "gym_owner"
        elif "gym_member" in roles:
            user_type = "gym_member"
        else:
            user_type = "unknown"

        return {
            "user_id": user_id,
            "email": token_info.get("email", ""),
            "role": user_type
        }

    @staticmethod
    def require_role(required_role: str):
        async def role_dependency(request: Request):
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(status_code=401, detail="Usuario no autenticado")

            roles = user.get("role", [])
            if isinstance(roles, list):
                if required_role not in roles:
                    raise HTTPException(status_code=403, detail="Acceso denegado: rol insuficiente")
            else:
                if roles != required_role:
                    raise HTTPException(status_code=403, detail="Acceso denegado: rol insuficiente")

            return user

        return role_dependency
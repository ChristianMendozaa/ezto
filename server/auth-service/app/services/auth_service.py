from fastapi import HTTPException, Request, Depends
from app.utils.firebase_config import db
from app.utils.keycloak_config import keycloak_openid

class AuthService:

    @staticmethod
    def require_role(role: str):
        async def dependency(request: Request):
            token = request.cookies.get("authToken")
            if not token:
                raise HTTPException(status_code=401, detail="Token ausente o inválido")

            try:
                token_info = keycloak_openid.introspect(token)
                if not token_info.get("active"):
                    raise HTTPException(status_code=401, detail="Token inválido o expirado")
            except Exception:
                raise HTTPException(status_code=401, detail="Token inválido o expirado")

            user_id = token_info.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Token inválido (sin sub)")

            try:
                user_doc = db.collection("users").document(user_id).get()
            except Exception:
                raise HTTPException(status_code=500, detail="Error al acceder a la base de datos")

            if not user_doc.exists:
                raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

            user_data = user_doc.to_dict()
            user_type = user_data.get("user_type", "gym_member")

            if user_type != role:
                raise HTTPException(status_code=403, detail="No autorizado para este recurso")

            return {
                "user_id": user_id,
                "email": token_info.get("email", ""),
                "role": user_type
            }

        return dependency
    
    @staticmethod
    async def get_current_user(request: Request):
        token = request.cookies.get("authToken")

        if not token:
            raise HTTPException(status_code=401, detail="Token ausente o inválido")

        return await AuthService.verify_token(token)

    @staticmethod
    async def verify_token(token: str):
        try:
            token_info = keycloak_openid.introspect(token)

            if not token_info.get("active"):
                raise HTTPException(status_code=401, detail="Token inválido o expirado")

        except Exception as e:
            raise HTTPException(status_code=401, detail="Token inválido o expirado")

        user_id = token_info.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido (sin sub)")

        try:
            user_doc = db.collection("users").document(user_id).get()
        except Exception as e:
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
                            
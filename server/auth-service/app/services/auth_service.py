import logging
from firebase_admin import auth
from app.utils.firebase_config import db
from fastapi import HTTPException, Request

logging.basicConfig(level=logging.INFO)

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
            # Agregar una tolerancia de 5 segundos en la validación del token
            decoded_token = auth.verify_id_token(token, clock_skew_seconds=10)
            print(f"Decoded token: {decoded_token}")
        except ValueError as e:
            print(f"Error de validación del token: {str(e)}")
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        except Exception as e:
            print(f"Error inesperado en verify_id_token: {str(e)}")
            raise HTTPException(status_code=401, detail="Error en autenticación")

        user_id = decoded_token["uid"]
        user_doc = db.collection("users").document(user_id).get()

        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        user_data = user_doc.to_dict()
        user_type = user_data.get("user_type", "gym_member")

        return {
            "user_id": user_id,
            "email": decoded_token.get("email", ""),
            "role": user_type
        }

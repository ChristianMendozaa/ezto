from firebase_admin import auth
from app.utils.firebase_config import db
from app.models.user_model import UserRegister
import asyncio
from datetime import date

class UserRepository:

    @staticmethod
    async def create_user(user: UserRegister, logo_base64: str = None):
        try:
            # Crear usuario en Firebase Authentication
            user_record = auth.create_user(
                email=user.email,
                password=user.password,
                display_name=user.full_name,
                phone_number=user.phone
            )

            # Datos adicionales a almacenar en Firestore
            user_data = user.dict()
            user_data["uid"] = user_record.uid
            user_data["gym_logo_base64"] = logo_base64
            
            # Convertir las fechas a cadenas en formato ISO-8601 (YYYY-MM-DD)
            if "member_info" in user_data and user_data["member_info"] is not None:
                birth_date = user_data["member_info"].get("birth_date")
                if isinstance(birth_date, date):
                    user_data["member_info"]["birth_date"] = birth_date.isoformat()
            
            # Guardar en Firestore de manera asíncrona
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: db.collection("users").document(user_record.uid).set(user_data)
            )

            return {"message": "Usuario registrado exitosamente", "uid": user_record.uid}

        except Exception as e:
            raise Exception(f"Error registrando el usuario en Firestore: {str(e)}")

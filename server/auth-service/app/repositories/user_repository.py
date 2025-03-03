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

            # Convertir fechas a formato ISO-8601 (YYYY-MM-DD)
            if user_data.get("member_info"):
                birth_date = user_data["member_info"].get("birth_date")
                if isinstance(birth_date, date):
                    user_data["member_info"]["birth_date"] = birth_date.isoformat()

            # Guardar usuario en Firestore
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: db.collection("users").document(user_record.uid).set(user_data)
            )

            # Si el usuario es dueño de un gimnasio, registrar el gimnasio en la colección "gyms"
            if user.user_type == "gym_owner" and user.gym_info:
                gym_data = {
                    "owner_id": user_record.uid,  # Asignar la ID del dueño
                    "name": user.gym_info.name,
                    "address": user.gym_info.address,
                    "phone": user.gym_info.phone,
                    "opening_hours": user.gym_info.opening_hours,
                    "services_offered": user.gym_info.services_offered,
                    "capacity": user.gym_info.capacity,
                    "social_media": user.gym_info.social_media,
                    "gym_logo_base64": logo_base64,  # Guardar el logo en la colección de gimnasios
                }

                # Crear la entrada en la colección "gyms"
                await loop.run_in_executor(
                    None,
                    lambda: db.collection("gyms").add(gym_data)
                )

            return {"message": "Usuario registrado exitosamente", "uid": user_record.uid}

        except Exception as e:
            raise Exception(f"Error registrando el usuario en Firestore: {str(e)}")

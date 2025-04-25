from app.utils.firebase_config import db
from app.utils.keycloak_config import keycloak_admin
from app.models.user_model import UserRegister
import asyncio
from datetime import date

class UserRepository:

    @staticmethod
    async def create_user(user: UserRegister, logo_base64: str = None):
        try:
            # 1. Crear usuario en Keycloak
            user_id = keycloak_admin.create_user({
                "email": user.email,
                "username": user.email,
                "enabled": True,
                "firstName": user.full_name.split(" ")[0],
                "lastName": " ".join(user.full_name.split(" ")[1:]),
                "credentials": [{"value": user.password, "type": "password"}],
            })

            # Asignar el rol según user_type
            role_name = user.user_type  # 'gym_owner' o 'gym_member'
            roles = keycloak_admin.get_realm_roles()
            role = next((r for r in roles if r['name'] == role_name), None)

            if role is None:
                raise Exception(f"El rol '{role_name}' no existe en Keycloak.")

            keycloak_admin.assign_realm_roles(user_id=user_id, roles=[{"id": role['id'], "name": role['name']}])


            # 2. Guardar en Firestore
            user_data = user.dict()
            user_data["uid"] = user_id
            user_data["gym_logo_base64"] = logo_base64

            if user_data.get("member_info"):
                birth_date = user_data["member_info"].get("birth_date")
                if isinstance(birth_date, date):
                    user_data["member_info"]["birth_date"] = birth_date.isoformat()

            loop = asyncio.get_running_loop()
            await loop.run_in_executor(
                None,
                lambda: db.collection("users").document(user_id).set(user_data)
            )

            # 3. Guardar gimnasio si es dueño
            if user.user_type == "gym_owner" and user.gym_info:
                gym_data = {
                    "owner_id": user_id,
                    "name": user.gym_info.name,
                    "address": user.gym_info.address,
                    "phone": user.gym_info.phone,
                    "opening_hours": user.gym_info.opening_hours,
                    "services_offered": user.gym_info.services_offered,
                    "capacity": user.gym_info.capacity,
                    "social_media": user.gym_info.social_media,
                    "gym_logo_base64": logo_base64,
                }

                await loop.run_in_executor(
                    None,
                    lambda: db.collection("gyms").add(gym_data)
                )

            return {"message": "Usuario registrado exitosamente", "uid": user_id}

        except Exception as e:
            raise Exception(f"Error registrando el usuario: {str(e)}")

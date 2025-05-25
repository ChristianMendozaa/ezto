from fastapi import HTTPException
from app.utils.firebase_config import db
from app.utils.keycloak_config import keycloak_admin
from app.models.user_model import UserRegister
from keycloak.exceptions import KeycloakPostError
import asyncio
from datetime import date
from fastapi import HTTPException

class UserRepository:

    @staticmethod
    async def create_user(user: UserRegister, logo_base64: str = None):
        try:
            # Paso 1: Verificar si ya existe el usuario en Keycloak
            existing_users = keycloak_admin.get_users(query={"email": user.email})
            if existing_users:
                raise HTTPException(status_code=409, detail="Ya existe un usuario registrado con este correo.")

            # Paso 2: Crear usuario en Keycloak
            try:
                user_id = keycloak_admin.create_user({
                    "email": user.email,
                    "username": user.email,
                    "enabled": True,
                    "firstName": user.full_name.strip().split(" ")[0],
                    "lastName": " ".join(user.full_name.strip().split(" ")[1:]),
                    "credentials": [{"value": user.password, "type": "password"}],
                })

                # Paso 2.1: Asignar rol al usuario
                role_name = user.user_type  # "gym_owner" o "gym_member"
                role = keycloak_admin.get_realm_role(role_name)
                keycloak_admin.assign_realm_roles(user_id=user_id, roles=[role])

            except KeycloakPostError as e:
                if e.response_code == 409:
                    raise HTTPException(status_code=409, detail="El usuario ya existe en Keycloak.")
                else:
                    raise HTTPException(status_code=502, detail=f"Error en Keycloak: {e}")
            # Paso 3: Guardar en Firestore
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

            # Paso 4: Guardar datos del gimnasio si aplica
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

        except HTTPException as http_exc:
            raise http_exc  # Propaga errores personalizados correctamente
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error registrando el usuario: {str(e)}")

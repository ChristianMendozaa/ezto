from app.models.user_model import UserRegister
from app.repositories.user_repository import UserRepository
from fastapi import UploadFile
import base64

class UserService:

    @staticmethod
    async def register_user(user: UserRegister, gym_logo: UploadFile = None):
        # Validar contraseñas
        if user.password != user.confirm_password:
            raise Exception("Las contraseñas no coinciden.")
        
        # Convertir la imagen a Base64 si se proporciona un logo
        logo_base64 = None
        if gym_logo:
            content = await gym_logo.read()
            logo_base64 = base64.b64encode(content).decode('utf-8')

        # Validar tipo de usuario
        if user.user_type == "gym_owner" and not user.gym_info:
            raise Exception("La información del gimnasio es requerida para dueños de gimnasio.")
        if user.user_type == "gym_member" and not user.member_info:
            raise Exception("La información del miembro es requerida para miembros de gimnasio.")

        # Crear usuario en Firebase y guardar en Firestore
        return await UserRepository.create_user(user, logo_base64)

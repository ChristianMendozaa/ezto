from app.models.user_model import UserRegister
from app.repositories.user_repository import UserRepository
from fastapi import UploadFile
import base64
from PIL import Image
import io

class UserService:

    @staticmethod
    async def register_user(user: UserRegister, gym_logo: UploadFile = None):
        # Validar contraseñas
        if user.password != user.confirm_password:
            raise Exception("Las contraseñas no coinciden.")
        
        # Convertir la imagen a Base64 comprimida en formato WebP si se proporciona un logo
        logo_base64 = None
        if gym_logo:
            try:
                # Leer el archivo subido
                content = await gym_logo.read()
                
                # Abrir la imagen con PIL y redimensionarla (por ejemplo, a 300x300)
                image = Image.open(io.BytesIO(content))
                image = image.convert("RGB")  # Asegurar formato correcto para WebP
                image.thumbnail((800, 800))   # Redimensionar la imagen
                
                # Guardar la imagen comprimida en un buffer como WebP
                buffer = io.BytesIO()
                image.save(buffer, format="WEBP", quality=70)  # Formato WebP con calidad 70%
                compressed_content = buffer.getvalue()
                
                # Convertir la imagen comprimida a Base64
                logo_base64 = base64.b64encode(compressed_content).decode('utf-8')
                
            except Exception as e:
                raise Exception(f"Error al procesar la imagen: {str(e)}")

        # Validar tipo de usuario
        if user.user_type == "gym_owner" and not user.gym_info:
            raise Exception("La información del gimnasio es requerida para dueños de gimnasio.")
        if user.user_type == "gym_member" and not user.member_info:
            raise Exception("La información del miembro es requerida para miembros de gimnasio.")

        # Crear usuario en Firebase y guardar en Firestore
        return await UserRepository.create_user(user, logo_base64)

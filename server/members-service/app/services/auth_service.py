<<<<<<< HEAD
import logging
from firebase_admin import auth
from fastapi import HTTPException, Request
from app.utils.firebase_config import db

logging.basicConfig(level=logging.INFO)

class AuthService:
    """
    Servicio de autenticación local para el microservicio de Miembros.
    Duplica la lógica de verificación de tokens de Firebase para ser autónomo.
    
    - Verifica el token JWT recibido en la cookie 'authToken'.
    - Confirma que el usuario exista en Firestore y extrae su rol.
    - Retorna un diccionario con user_id, email y role.
    
    Cualquier cambio en la lógica de 'auth' de tu otro microservicio NO afecta a este.
    Ambos pueden evolucionar de forma independiente.
    """

    @staticmethod
    async def get_current_user(request: Request) -> dict:
        """
        Obtiene el token desde la cookie 'authToken' y llama a 'verify_token'.
        Lanza HTTPException(401) si no se encuentra o es inválido.
        
        Returns:
            dict: { "user_id": str, "email": str, "role": str }
        """
        token = request.cookies.get("authToken")
        if not token:
            # Opcionalmente, podrías intentar buscar en request.headers["Cookie"] si quieres
            raise HTTPException(status_code=401, detail="Token ausente o inválido")

        return await AuthService.verify_token(token)

    @staticmethod
    async def verify_token(token: str) -> dict:
        """
        Verifica el token JWT con Firebase Admin. Si es válido, confirma la existencia
        del usuario en Firestore y retorna un objeto con user_id, email y role.
        
        Args:
            token (str): Token JWT recibido (normalmente en la cookie 'authToken').

        Raises:
            HTTPException(401): Si el token es inválido o la verificación falla.
            HTTPException(404): Si el usuario no está en Firestore.

        Returns:
            dict: Información del usuario, p.ej. {"user_id": "...", "email": "...", "role": "..."}
        """
        try:
            decoded_token = auth.verify_id_token(token)
            logging.info(f"Decoded token: {decoded_token}")
        except ValueError as e:
            logging.error(f"Error de validación del token: {str(e)}")
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        except Exception as e:
            logging.error(f"Error inesperado en verify_id_token: {str(e)}")
            raise HTTPException(status_code=401, detail="Error en autenticación")

        # Extraer el user_id del token decodificado
        user_id = decoded_token.get("uid")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sin UID de usuario")

        # Consultar Firestore para asegurar que existe y obtener su rol
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        user_data = user_doc.to_dict()
        user_type = user_data.get("user_type", "gym_member")

        return {
            "user_id": user_id,
            "email": decoded_token.get("email", ""),
            "role": user_type
=======
import logging
from firebase_admin import auth
from fastapi import HTTPException, Request
from app.utils.firebase_config import db

logging.basicConfig(level=logging.INFO)

class AuthService:
    """
    Servicio de autenticación local para el microservicio de Miembros.
    Duplica la lógica de verificación de tokens de Firebase para ser autónomo.
    
    - Verifica el token JWT recibido en la cookie 'authToken'.
    - Confirma que el usuario exista en Firestore y extrae su rol.
    - Retorna un diccionario con user_id, email y role.
    
    Cualquier cambio en la lógica de 'auth' de tu otro microservicio NO afecta a este.
    Ambos pueden evolucionar de forma independiente.
    """

    @staticmethod
    async def get_current_user(request: Request) -> dict:
        """
        Obtiene el token desde la cookie 'authToken' y llama a 'verify_token'.
        Lanza HTTPException(401) si no se encuentra o es inválido.
        
        Returns:
            dict: { "user_id": str, "email": str, "role": str }
        """
        token = request.cookies.get("authToken")
        if not token:
            # Opcionalmente, podrías intentar buscar en request.headers["Cookie"] si quieres
            raise HTTPException(status_code=401, detail="Token ausente o inválido")

        return await AuthService.verify_token(token)

    @staticmethod
    async def verify_token(token: str) -> dict:
        """
        Verifica el token JWT con Firebase Admin. Si es válido, confirma la existencia
        del usuario en Firestore y retorna un objeto con user_id, email y role.
        
        Args:
            token (str): Token JWT recibido (normalmente en la cookie 'authToken').

        Raises:
            HTTPException(401): Si el token es inválido o la verificación falla.
            HTTPException(404): Si el usuario no está en Firestore.

        Returns:
            dict: Información del usuario, p.ej. {"user_id": "...", "email": "...", "role": "..."}
        """
        try:
            decoded_token = auth.verify_id_token(token)
            logging.info(f"Decoded token: {decoded_token}")
        except ValueError as e:
            logging.error(f"Error de validación del token: {str(e)}")
            raise HTTPException(status_code=401, detail="Token inválido o expirado")
        except Exception as e:
            logging.error(f"Error inesperado en verify_id_token: {str(e)}")
            raise HTTPException(status_code=401, detail="Error en autenticación")

        # Extraer el user_id del token decodificado
        user_id = decoded_token.get("uid")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token sin UID de usuario")

        # Consultar Firestore para asegurar que existe y obtener su rol
        user_doc = db.collection("users").document(user_id).get()
        if not user_doc.exists:
            raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos")

        user_data = user_doc.to_dict()
        user_type = user_data.get("user_type", "gym_member")

        return {
            "user_id": user_id,
            "email": decoded_token.get("email", ""),
            "role": user_type
>>>>>>> afb75bf933e10a27a8164a48c8899b5b816ddf92
        }
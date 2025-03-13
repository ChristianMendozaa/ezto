<<<<<<< HEAD
from app.utils.firebase_config import db
import asyncio

class MemberRepository:
    @staticmethod
    async def get_all_members():
        """Obtiene todos los miembros de la base de datos."""
        try:
            members_ref = db.collection("members")
            members_snapshot = await members_ref.stream()  # Firestore SDK ya es asincrónico
            # Agregar el id del documento como campo en los datos
            return [{"id": member.id, **member.to_dict()} for member in members_snapshot]
        except Exception as e:
            raise Exception(f"Error al obtener los miembros: {str(e)}")

    @staticmethod
    async def create_member(member_data: dict) -> dict:
        """Crea un nuevo miembro en la base de datos."""
        try:
            print(f"Datos a insertar: {member_data}")
            members_ref = db.collection("members")
            # Insertar el nuevo miembro en Firestore
            return member_data
        except Exception as e:
            raise Exception(f"Error al crear el miembro: {str(e)}")

    @staticmethod
    async def update_member(member_id: str, member_data: dict) -> dict:
        """Actualiza los datos de un miembro existente."""
        try:
            member_ref = db.collection("members").document(member_id)
            await member_ref.update(member_data)  # Firestore SDK es asincrónico
            return {"id": member_id, **member_data}
        except Exception as e:
            raise Exception(f"Error al actualizar el miembro {member_id}: {str(e)}")

    @staticmethod
    async def delete_member(member_id: str) -> dict:
        """Elimina un miembro por su ID."""
        try:
            member_ref = db.collection("members").document(member_id)
            await member_ref.delete()  # Firestore SDK es asincrónico
            return {"message": f"Miembro {member_id} eliminado exitosamente."}
        except Exception as e:
            raise Exception(f"Error al eliminar el miembro {member_id}: {str(e)}")
=======
from app.utils.firebase_config import db

class MemberRepository:
    @staticmethod
    def get_all_members():
        """Obtiene todos los miembros de la base de datos."""
        try:
            members_ref = db.collection("members")
            members_snapshot = members_ref.stream()
            return [{"id": member.id, **member.to_dict()} for member in members_snapshot]
        except Exception as e:
            raise Exception(f"Error al obtener los miembros: {str(e)}")

    @staticmethod
    def create_member(member_data: dict) -> dict:
        """Crea un nuevo miembro en la base de datos."""
        try:
            member_ref = db.collection("members").add(member_data)
            return {"id": member_ref.id, **member_data}
        except Exception as e:
            raise Exception(f"Error al crear el miembro: {str(e)}")

    @staticmethod
    def update_member(member_id: str, member_data: dict) -> dict:
        """Actualiza los datos de un miembro existente."""
        try:
            member_ref = db.collection("members").document(member_id)
            member_ref.update(member_data)
            return {"id": member_id, **member_data}
        except Exception as e:
            raise Exception(f"Error al actualizar el miembro {member_id}: {str(e)}")

    @staticmethod
    def delete_member(member_id: str) -> dict:
        """Elimina un miembro por su ID."""
        try:
            member_ref = db.collection("members").document(member_id)
            member_ref.delete()
            return {"message": f"Miembro {member_id} eliminado exitosamente."}
        except Exception as e:
            raise Exception(f"Error al eliminar el miembro {member_id}: {str(e)}")
>>>>>>> afb75bf933e10a27a8164a48c8899b5b816ddf92

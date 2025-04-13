from app.utils.firebase_config import db
import asyncio
class MemberRepository:
    @staticmethod
    async def get_all_members():
        """Obtiene todos los miembros de la base de datos."""
        try:
            members_ref = db.collection("members")
            members_snapshot = members_ref.stream()  # Firestore SDK ya es asincrónico
            # Agregar el id del documento como campo en los datos
            return [{"id": member.id, **member.to_dict()} for member in members_snapshot]
        except Exception as e:
            raise Exception(f"Error al obtener los miembros: {str(e)}")

    @staticmethod
    async def create_member(member_data):
        """Crea un nuevo miembro en la base de datos con un ID definido por el frontend."""
        try:
            members_ref = db.collection("members")
            member_id = member_data.get("id")  # Obtiene el ID enviado desde el frontend
            
            if not member_id:
                raise ValueError("El ID del miembro es requerido.")

            # Usamos `document(id).set(data)` en lugar de `add(data)`
            await asyncio.to_thread(members_ref.document(member_id).set, member_data)

            return member_data  # Retornamos el mismo objeto enviado
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
            await asyncio.to_thread(member_ref.delete)
            return {"message": f"Miembro {member_id} eliminado exitosamente."}
        except Exception as e:
            raise Exception(f"Error al eliminar el miembro {member_id}: {str(e)}")

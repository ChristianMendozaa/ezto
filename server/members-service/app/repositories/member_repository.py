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

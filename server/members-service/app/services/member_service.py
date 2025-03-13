<<<<<<< HEAD
from app.repositories.member_repository import MemberRepository

class MemberService:
    @staticmethod
    async def list_members():
        """Obtiene todos los miembros."""
        return await MemberRepository.get_all_members()

    @staticmethod
    async def create_member(member_data):
        """Crea un nuevo miembro."""
        return await MemberRepository.create_member(member_data)

    @staticmethod
    async def update_member(member_id, member_data):
        """Actualiza un miembro existente."""
        return await MemberRepository.update_member(member_id, member_data)

    @staticmethod
    async def delete_member(member_id):
        """Elimina un miembro por su ID."""
        return await MemberRepository.delete_member(member_id)
=======
from app.repositories.member_repository import MemberRepository

class MemberService:
    @staticmethod
    async def list_members():
        """Obtiene todos los miembros."""
        return await MemberRepository.get_all_members()

    @staticmethod
    async def create_member(member_data):
        """Crea un nuevo miembro."""
        return await MemberRepository.create_member(member_data)

    @staticmethod
    async def update_member(member_id, member_data):
        """Actualiza un miembro existente."""
        return await MemberRepository.update_member(member_id, member_data)

    @staticmethod
    async def delete_member(member_id):
        """Elimina un miembro por su ID."""
        return await MemberRepository.delete_member(member_id)
>>>>>>> afb75bf933e10a27a8164a48c8899b5b816ddf92

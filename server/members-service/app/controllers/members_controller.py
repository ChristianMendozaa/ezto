"""
Controlador para endpoints de gestión de miembros.

Incluye:
- Registrar un nuevo miembro.
- Listar todos los miembros.
- Obtener un miembro por ID.
- Actualizar un miembro.
- Eliminar un miembro.
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel, Field

from app.services.member_service import MemberService
from app.services.auth_service import AuthService
from app.models.member_model import Member

router = APIRouter()

class ErrorResponse(BaseModel):
    """Modelo de error estándar."""
    detail: str = Field(..., description="Mensaje de error.")


@router.post(
    "/",
    summary="Registrar un nuevo miembro",
    description="Crea un nuevo miembro en la plataforma. Requiere autenticación.",
    response_model=Member,
    responses={401: {"model": ErrorResponse}, 400: {"model": ErrorResponse}}
)
async def create_member(
    member_data: Member,
    user: dict = Depends(AuthService.get_current_user)  # Validación de usuario
):
    """Crea un nuevo miembro y lo registra en la base de datos."""
    return await MemberService.create_member(member_data)


@router.get(
    "/",
    summary="Listar todos los miembros",
    description="Obtiene la lista de todos los miembros registrados en la plataforma.",
    response_model=List[Member],
    responses={401: {"model": ErrorResponse}}
)
async def list_members(user: dict = Depends(AuthService.get_current_user)):
    """Devuelve la lista de miembros."""
    return await MemberService.list_members()


@router.get(
    "/{member_id}",
    summary="Obtener un miembro por ID",
    description="Devuelve los datos de un miembro específico.",
    response_model=Member,
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def get_member(
    member_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """Obtiene la información de un miembro según su ID."""
    member = await MemberService.get_member_by_id(member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")
    return member


@router.put(
    "/{member_id}",
    summary="Actualizar un miembro",
    description="Actualiza los datos de un miembro existente.",
    response_model=Member,
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def update_member(
    member_id: str,
    member_data: Member,
    user: dict = Depends(AuthService.get_current_user)
):
    """Actualiza los datos de un miembro."""
    updated_member = await MemberService.update_member(member_id, member_data)
    if not updated_member:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")
    return updated_member


@router.delete(
    "/{member_id}",
    summary="Eliminar un miembro",
    description="Elimina un miembro de la plataforma.",
    response_model=dict,
    responses={401: {"model": ErrorResponse}, 404: {"model": ErrorResponse}}
)
async def delete_member(
    member_id: str,
    user: dict = Depends(AuthService.get_current_user)
):
    """Elimina un miembro de la base de datos."""
    result = await MemberService.delete_member(member_id)
    if not result:
        raise HTTPException(status_code=404, detail="Miembro no encontrado.")
    return {"message": "Miembro eliminado correctamente."}

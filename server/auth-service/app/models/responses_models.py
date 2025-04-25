from pydantic import BaseModel, Field
from typing import Optional, Generic, TypeVar
from pydantic.generics import GenericModel

# Modelo genérico para el campo "data"
T = TypeVar("T")
class DashboardResponse(BaseModel):
    """
    Respuesta para el Panel de Administración.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Dashboard.")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado.")

class ClientResponse(BaseModel):
    """
    Respuesta para el Panel de Cliente.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de bienvenida al Panel de Cliente.")
    user: dict = Field(..., title="Usuario", description="Información del usuario autenticado.")
class LogoutResponse(BaseModel):
    """
    Respuesta para la operación de cierre de sesión.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de confirmación del cierre de sesión.")
class LoginSuccessResponse(BaseModel):
    """
    Respuesta para un inicio de sesión exitoso.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario autenticado.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario autenticado.")
    role: str = Field(..., title="Rol", description="Rol asignado al usuario en la plataforma.")
    token: str = Field(..., title="Token", description="Token de autenticación devuelto en la respuesta.")
class UserResponse(BaseModel):
    """
    Respuesta para la obtención del usuario autenticado.
    """
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario autenticado.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario autenticado.")
    role: str = Field(..., title="Rol", description="Rol asignado al usuario en la plataforma.")
class RegisterResponse(BaseModel):
    """
    Respuesta estándar para el registro de usuarios.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de éxito.")
    uid: str = Field(..., title="UID", description="Identificador único del usuario registrado.")
class StandardResponse(GenericModel, Generic[T]):
    """
    Modelo de respuesta estándar con success, data y error.
    """
    success: bool = Field(..., description="Indica si la operación fue exitosa.")
    data: Optional[T] = Field(None, description="Datos de la respuesta.")
    error: Optional[str] = Field(None, description="Mensaje de error si ocurre alguno.")
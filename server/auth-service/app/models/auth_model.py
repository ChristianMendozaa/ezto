from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    """
    Modelo para la solicitud de inicio de sesión.
    """
    email: EmailStr = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario.")
    password: str = Field(..., title="Contraseña", description="Contraseña del usuario.")

class LoginResponse(BaseModel):
    """
    Modelo para la respuesta del inicio de sesión.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de respuesta indicando el estado del login.")
    token: str = Field(..., title="Token", description="Token de autenticación para futuras solicitudes.")
    user_id: str = Field(..., title="ID del Usuario", description="Identificador único del usuario autenticado.")
    email: str = Field(..., title="Correo Electrónico", description="Correo electrónico del usuario autenticado.")
    role: str = Field(..., title="Rol", description="Rol asignado al usuario en la plataforma.")

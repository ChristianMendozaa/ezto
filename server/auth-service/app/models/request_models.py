from pydantic import BaseModel, EmailStr, Field

class LoginData(BaseModel):
    email: EmailStr = Field(..., description="Correo electrónico del usuario.")
    password: str = Field(..., min_length=8, description="Contraseña del usuario (mínimo 8 caracteres).")

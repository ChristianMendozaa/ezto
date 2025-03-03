from fastapi import APIRouter, Response
from pydantic import BaseModel, Field

router = APIRouter()

class LogoutResponse(BaseModel):
    """
    Respuesta para la operación de cierre de sesión.
    """
    message: str = Field(..., title="Mensaje", description="Mensaje de confirmación del cierre de sesión.")

@router.post(
    "/logout",
    summary="Cerrar sesión",
    description="Elimina la cookie de autenticación para cerrar sesión de manera segura.",
    response_model=LogoutResponse
)
async def logout(response: Response):
    """
    Endpoint para cerrar sesión.  
    Elimina la cookie de autenticación `authToken` del usuario.
    """
    response.headers["Set-Cookie"] = "authToken=; Path=/; HttpOnly; Secure=False; SameSite=Lax; Max-Age=0"
    return {"message": "Logout exitoso"}

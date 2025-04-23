from fastapi import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Any, Optional

class StandardResponse(BaseModel):
    """
    Estructura estándar de respuesta para la API.
    """
    success: bool = Field(..., title="Éxito", description="Indica si la operación fue exitosa.")
    data: Optional[Any] = Field(None, title="Datos", description="Datos de la respuesta en caso de éxito.")
    error: Optional[str] = Field(None, title="Error", description="Mensaje de error en caso de fallo.")

def success_response(data: Any):
    """
    Genera una respuesta exitosa con la estructura estándar.
    """
    return {"success": True, "data": data, "error": None}

def error_response(message: str, status_code: int = 400):
    """
    Genera una respuesta de error con la estructura estándar.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "data": None,
            "error": message
        }
    )

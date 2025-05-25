from pydantic import BaseModel
from typing import List, Optional, Union

class StandardResponse(BaseModel): #base para todas las respuestas
    status: str  # "success" o "error"
    message: Optional[str] = None
    data: Optional[Union[dict, List[dict]]] = None  # Puede ser un objeto o lista de objetos

class ErrorResponse(StandardResponse):
    status: str = "error"
    errors: Optional[List[str]] = None  # Lista de errores específicos

class SuccessResponse(StandardResponse):
    status: str = "success"


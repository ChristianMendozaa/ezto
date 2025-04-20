from pydantic import BaseModel
from typing import Optional, Any, List
from app.models.dtos.UserMembershipDTO import UserMembershipDTO
#para el repositoru
class StandardResponse(BaseModel):
    status: str  # "success" o "error"
    message: Optional[str] = None 
    data: Optional[Any] = None 

class UserMembershipResponse(BaseModel):
    status: str
    message: Optional[str] = None
    promotions: Optional[List[UserMembershipDTO]] = None

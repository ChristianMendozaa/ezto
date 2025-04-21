# app/dependencies/auth_roles.py
from fastapi import Request, HTTPException, Depends
from typing import Callable
from app.services.auth_service import AuthService

def require_role(*roles: str) -> Callable:
    async def dependency(user: dict = Depends(AuthService.get_current_user)):
        if user.get("role") not in roles:
            raise HTTPException(status_code=403, detail="No autorizado")
        return user
    return dependency


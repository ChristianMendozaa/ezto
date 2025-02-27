from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from app.models.user_model import UserRegister
from app.services.user_service import UserService
from pydantic import EmailStr
from typing import Optional, List
from datetime import date

router = APIRouter()

@router.post("/register")
async def register_user(
    full_name: str = Form(...),
    email: EmailStr = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    phone: str = Form(...),
    user_type: str = Form(...),
    gym_name: Optional[str] = Form(None),
    gym_address: Optional[str] = Form(None),
    gym_phone: Optional[str] = Form(None),
    opening_hours: Optional[str] = Form(None),
    services_offered: Optional[List[str]] = Form(None),
    capacity: Optional[int] = Form(None),
    social_media: Optional[str] = Form(None),
    gym_id: Optional[str] = Form(None),
    membership_number: Optional[str] = Form(None),
    birth_date: Optional[date] = Form(None),
    gender: Optional[str] = Form(None),
    training_goals: Optional[List[str]] = Form(None),
    activity_preferences: Optional[List[str]] = Form(None),
):
    try:
        # Construir el objeto UserRegister manualmente
        user_data = {
            "full_name": full_name,
            "email": email,
            "password": password,
            "confirm_password": confirm_password,
            "phone": phone,
            "user_type": user_type,
            "gym_info": {
                "name": gym_name,
                "address": gym_address,
                "phone": gym_phone,
                "opening_hours": opening_hours,
                "services_offered": services_offered,
                "capacity": capacity,
                "social_media": social_media,
            } if user_type == "gym_owner" else None,
            "member_info": {
                "gym_id": gym_id,
                "membership_number": membership_number,
                "birth_date": birth_date,
                "gender": gender,
                "training_goals": training_goals,
                "activity_preferences": activity_preferences,
            } if user_type == "gym_member" else None,
        }

        # Crear un objeto UserRegister desde el diccionario
        user = UserRegister(**user_data)

        return await UserService.register_user(user)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

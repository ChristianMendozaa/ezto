# app/repositories/schedule_repository.py
from app.utils.firebase_config import db
import asyncio
from datetime import datetime

class ScheduleRepository:
    @staticmethod
    async def create_schedule(schedule_data: dict):
        try:
            loop = asyncio.get_running_loop()
            schedule_ref = await loop.run_in_executor(
                None,
                lambda: db.collection("schedules").add({
                    **schedule_data,
                    "created_at": datetime.now(),
                    "updated_at": datetime.now(),
                    "status": "activo"
                })
            )
            return schedule_ref.id
        except Exception as e:
            raise Exception(f"Error creando el horario: {str(e)}")

    @staticmethod
    async def get_weekly_schedule(start_date: datetime, gym_id: str = None):
        try:
            loop = asyncio.get_running_loop()
            query = db.collection("schedules")
            
            if gym_id:
                query = query.where("gym_id", "==", gym_id)
            
            schedules = await loop.run_in_executor(
                None,
                lambda: query.where("start_date", ">=", start_date).get()
            )
            return [doc.to_dict() for doc in schedules]
        except Exception as e:
            raise Exception(f"Error obteniendo los horarios: {str(e)}")
from datetime import datetime
from app.repositories.schedule_repository import ScheduleRepository
from app.models.schedule_model import ScheduleCreate

class ScheduleService:
    @staticmethod
    async def create_schedule(schedule_data: ScheduleCreate):
        return await ScheduleRepository.create_schedule(schedule_data.dict())

    @staticmethod
    async def get_weekly_schedule(start_date: datetime, gym_id: str = None):
        return await ScheduleRepository.get_weekly_schedule(start_date, gym_id)
# app/models/class_model.py

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional

@dataclass
class ClassEntity:
    id: Optional[str]
    name: str
    description: str
    instructor: str
    start_time: datetime
    end_time: datetime
    capacity: int
    location: Optional[str]
    status: bool

    @property
    def schedule(self) -> str:
        """Horario de la clase formateado HH:MM – HH:MM."""
        return f"{self.start_time.strftime('%H:%M')} – {self.end_time.strftime('%H:%M')}"

    @property
    def day_of_week(self) -> str:
        """Nombre del día de la semana en que se imparte la clase."""
        # En inglés; para español podrías usar locale o un mapeo manual
        return self.start_time.strftime("%A")

    def to_dict(self) -> dict:
        """
        Pasa la entidad a dict listo para JSON:
        - convierte datetimes a ISO
        - añade schedule y day_of_week
        """
        data = asdict(self)
        data["start_time"] = self.start_time.isoformat()
        data["end_time"]   = self.end_time.isoformat()
        data["schedule"]   = self.schedule
        data["day_of_week"] = self.day_of_week
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "ClassEntity":
        """
        Reconstruye una entidad desde un dict, parseando ISO timestamps.
        """
        return cls(
            id=data.get("id"),
            name=data["name"],
            description=data["description"],
            instructor=data["instructor"],
            start_time=datetime.fromisoformat(data["start_time"]),
            end_time=datetime.fromisoformat(data["end_time"]),
            capacity=int(data["capacity"]),
            location=data.get("location"),
            status=bool(data["status"])
        )

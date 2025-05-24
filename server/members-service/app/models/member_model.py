from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

class MemberStatus(str, Enum):
    active = "activo"
    inactive = "inactivo"
    suspended = "suspendido"

@dataclass
class MemberEntity:
    id: str
    name: str
    email: str
    nfc_id: Optional[str]
    status: MemberStatus
    join_date: datetime

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "nfc_id": self.nfc_id,
            "status": self.status.value,
            "join_date": self.join_date.isoformat()
        }

    @staticmethod
    def from_dict(data: dict) -> "MemberEntity":
        try:
            return MemberEntity(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                nfc_id=data.get("nfc_id"),
                status=MemberStatus(data["status"]),
                join_date=datetime.fromisoformat(data["join_date"])
            )
        except Exception as e:
            raise ValueError(f"Error al convertir documento a MemberEntity: {e}")

    def to_dto(self) -> "MemberDTO":
        from app.models.dtos.member_dto import MemberDTO
        return MemberDTO(
            id=self.id,
            name=self.name,
            email=self.email,
            nfc_id=self.nfc_id,
            status=self.status,
            join_date=self.join_date
        )

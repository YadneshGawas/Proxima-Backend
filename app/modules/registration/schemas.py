from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TeamMemberRoleEnum(str, Enum):
    owner = "owner"
    coleader = "coleader"
    member = "member"


class TeamMemberResponseSchema(BaseModel):
    user_id: int
    role: TeamMemberRoleEnum
    name : str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamResponseSchema(BaseModel):
    id: str
    name: str
    created_by: int
    members: List[TeamMemberResponseSchema]

    model_config = ConfigDict(from_attributes=True)


class RegistrationCreateSchema(BaseModel):
    hackathon_id: str
    team_id: Optional[str] = None


class RegistrationResponseSchema(BaseModel):
    id: str
    hackathon_id: str
    user_id: Optional[int]
    team_id: Optional[str]
    status: str
    registered_at: datetime

      # 🔥 New (organizer view)
    team: Optional[TeamResponseSchema] = None

    model_config = ConfigDict(from_attributes=True)

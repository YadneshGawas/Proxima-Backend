from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional
from datetime import datetime


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

    model_config = ConfigDict(from_attributes=True)

# app/modules/winners/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List


class WinnerResponseSchema(BaseModel):
    id: str
    position: int
    score: float

    project: dict
    team: dict

    created_at: datetime

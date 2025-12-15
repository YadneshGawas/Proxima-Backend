from pydantic import BaseModel
from typing import List
from enum import Enum
from datetime import datetime

class TeamRoleEnum(str,Enum):
    owner = "owner"
    coleader = "coleader"
    member = "member"

class TeamCreateSchema(BaseModel):
    name: str

class AddMemberSchema(BaseModel):
    member_id: int
    role: TeamRoleEnum = TeamRoleEnum.member

class UpdateMemberRoleSchema(BaseModel):
    role: TeamRoleEnum

class TeamMemberReadSchema(BaseModel):
    member_id:int
    role:TeamRoleEnum
    joined_at:datetime

class RemoveMemberParamsSchema(BaseModel):
    team_id: str
    member_id: int



# class TeamMemberResponse(BaseModel):
#     id:str
#     name:str
#     members_count = int
#     members:List[TeamMemberReadSchema]
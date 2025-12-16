from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime


class TeamMemberSchema(BaseModel):
    user_id: int
    name: str
    role: str
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamSchema(BaseModel):
    id: str
    name: str
    created_by: int
    members: List[TeamMemberSchema]

    model_config = ConfigDict(from_attributes=True)


class ProjectSubmissionCreateSchema(BaseModel):
    team_id: str
    project_title: str
    project_desc: str
    github_url: str
    live_url: Optional[str] = None


class ProjectSubmissionResponseSchema(BaseModel):
    id: str
    hackathon_id: str
    project_title: str
    project_desc: str
    github_url: str
    live_url: Optional[str]
    created_at: datetime

    team: TeamSchema
    average_score: Optional[float]

    model_config = ConfigDict(from_attributes=True)


class JudgeScoreCreateSchema(BaseModel):
    score: int


class JudgeAssignSchema(BaseModel):
    user_id: int


class JudgeResponseSchema(BaseModel):
    user_id: int
    name:str


class ProjectSubmissionUpdateSchema(BaseModel):
    project_title: str
    project_desc: str
    github_url: str
    live_url: Optional[str] = None
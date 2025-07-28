from pydantic import BaseModel, Field


class UserProfile(BaseModel):
    id: str
    skill_level: str
    time_budget: str
    learning_style: str
    preferences: dict
from pydantic import BaseModel
from typing import List

class LearningTask(BaseModel):
    topic: str
    duration: int  # in minutes or hours
    resources: List[str]
    status: str  # e.g., 'not_started', 'in_progress', 'done'
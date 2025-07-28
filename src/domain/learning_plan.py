from pydantic import BaseModel
from typing import List
from .learning_task import LearningTask

class LearningPlan(BaseModel):
    tasks: List[LearningTask]
    status: str
    feedback_log: List[str]

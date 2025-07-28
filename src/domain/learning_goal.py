from pydantic import BaseModel
from datetime import date

class LearningGoal(BaseModel):
    goal_description: str
    deadline: date
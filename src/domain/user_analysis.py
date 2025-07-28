from pydantic import BaseModel, Field
from typing import List, Optional
from .user_profile import UserProfile
from .learning_goal import LearningGoal
from .learning_plan import LearningPlan
from .learning_task import LearningTask
from datetime import date

class UserAnalysis(BaseModel):
    user_profile: UserProfile
    learning_goals: List[LearningGoal]
    learning_plan: LearningPlan
    completed_tasks: List[LearningTask] = Field(default_factory=list)
    pending_tasks: List[LearningTask] = Field(default_factory=list)
    feedback: Optional[str] = None  
    analysis_date: date  


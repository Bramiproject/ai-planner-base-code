"""
User Input Handler - Structured form-based input collection
"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class LearningRequest:
    skill: str
    experience_level: str  # "Beginner", "Intermediate", "Advanced"
    timeline: str  # "3 weeks", "2 months", etc.
    time_budget: str  # "1 hour/day", "5 hours/week", etc.
    learning_style: str  # "video", "reading", "hands-on", "mixed"
    specific_goals: Optional[str] = None  # Optional specific objectives and additional context

def collect_user_inputs() -> LearningRequest:
    """
    Collect structured inputs from user through a simple form interface
    """
    print("=== AI Learning Planner ===")
    print("Let's create your personalized learning plan!\n")
    
    # Skill input
    skill = input("What skill do you want to learn? (e.g., 'table making', 'piano', 'cooking'): ").strip()
    
    # Experience level
    print("\nWhat's your current experience level?")
    print("1. Beginner (never done this before)")
    print("2. Intermediate (some experience)")
    print("3. Advanced (quite experienced)")
    exp_choice = input("Choose (1-3): ").strip()
    
    experience_map = {"1": "Beginner", "2": "Intermediate", "3": "Advanced"}
    experience_level = experience_map.get(exp_choice, "Beginner")
    
    # Timeline
    timeline = input("\nHow long do you want to spend learning this? (e.g., '5 weeks', '2 months'): ").strip()
    
    # Time budget
    time_budget = input("How much time can you dedicate? (e.g., '1 hour/day', '3 hours/week'): ").strip()
    
    # Learning style
    print("\nWhat's your preferred learning style?")
    print("1. Video tutorials")
    print("2. Reading/articles")
    print("3. Hands-on practice")
    print("4. Mixed (combination)")
    style_choice = input("Choose (1-4): ").strip()
    
    style_map = {"1": "video", "2": "reading", "3": "hands-on", "4": "mixed"}
    learning_style = style_map.get(style_choice, "mixed")
    
    # Specific goals and additional context (optional)
    specific_goals = input("\nAny specific goals, preferences, or additional context? (e.g., classical music focus, budget limitations, equipment available, learning challenges - optional, press Enter to skip): ").strip()
    if not specific_goals:
        specific_goals = None
    
    return LearningRequest(
        skill=skill,
        experience_level=experience_level,
        timeline=timeline,
        time_budget=time_budget,
        learning_style=learning_style,
        specific_goals=specific_goals
    )

def create_search_query(request: LearningRequest) -> str:
    """
    Convert structured input into a clean search query
    """
    # Clean, simple query for search
    base_query = f"learn {request.skill} {request.experience_level.lower()} tutorial"
    
    if request.specific_goals:
        base_query += f" {request.specific_goals}"
    
    return base_query

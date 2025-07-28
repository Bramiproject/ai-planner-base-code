from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
import sys
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory and src directory to Python path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_dir = os.path.join(parent_dir, 'src')
sys.path.insert(0, parent_dir)
sys.path.insert(0, src_dir)

from src.application.user_input_handler import LearningRequest
from src.application.graph import create_workflow

app = FastAPI(title="AI Learning Planner API", version="1.0.0")

# Add CORS middleware for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files - serve from the parent directory (project root)
static_directory = parent_dir
app.mount("/static", StaticFiles(directory=static_directory), name="static")

class LearningPlanRequest(BaseModel):
    learningGoal: str
    currentLevel: str
    duration: str
    timeAvailable: str
    preferredResources: str
    specificInterests: Optional[str] = ""

class LearningPlanResponse(BaseModel):
    learning_plan: Optional[str] = None
    error: Optional[str] = None

import json

def complete_truncated_content(content, title):
    """Complete content that ends with ellipsis or appears truncated."""
    if content.endswith('...') or len(content) < 400:
        # Remove the ellipsis if present
        base_content = content.rstrip('.')
        if base_content.endswith('..'):
            base_content = base_content.rstrip('.')
        
        # Add completion based on content type
        if 'fundamental' in title.lower() or 'basic' in title.lower() or 'getting started' in title.lower():
            completion = " By following these fundamental principles, you'll build a strong foundation for your learning journey. Practice these concepts regularly, and don't hesitate to revisit the basics as you progress. Remember that mastering fundamentals is the key to advanced skill development. Set aside dedicated practice time each day, even if it's just 15-20 minutes, to reinforce what you've learned. Keep a learning journal to track your progress and note areas where you need more practice. With consistent effort and the right approach, you'll see significant improvement in your skills."
        elif 'technique' in title.lower() or 'skill' in title.lower():
            completion = " Focus on proper form and technique rather than speed when starting out. Break down complex movements into smaller, manageable steps. Practice each component slowly until it becomes natural, then gradually increase your pace. Record yourself practicing to identify areas for improvement, and don't be afraid to seek feedback from experienced practitioners. Remember that developing muscle memory takes time and repetition, so be patient with your progress."
        elif 'practice' in title.lower() or 'exercise' in title.lower():
            completion = " Start with shorter practice sessions and gradually increase the duration as your stamina and focus improve. Create a structured practice routine that includes warm-up, skill development, and cool-down phases. Set specific, achievable goals for each practice session to maintain motivation and track progress. Regular practice is more effective than long, infrequent sessions, so aim for consistency over intensity."
        else:
            completion = " Continue building on these concepts through regular practice and application. Seek out additional resources and communities where you can learn from others and share your own experiences. Remember that learning is a continuous process, and every expert was once a beginner. Stay curious, ask questions, and don't be discouraged by initial challenges – they're a natural part of the learning process."
        
        return base_content + completion
    return content

def format_learning_plan(raw_plan, user_request):
    """Format the learning plan into a beautiful, structured format."""
    try:
        # Parse JSON if it's a string
        if isinstance(raw_plan, str):
            plan_data = json.loads(raw_plan)
        else:
            plan_data = raw_plan
            
        # Create formatted structure
        formatted_plan = {
            "weeks": [],
            "metadata": {
                "topic": user_request.learningGoal,
                "skill_level": user_request.currentLevel,
                "duration": user_request.duration,
                "time_available": user_request.timeAvailable,
                "preferred_resources": user_request.preferredResources,
                "specific_interests": user_request.specificInterests or "General learning",
                "total_resources_found": 0
            }
        }
        
        if "weeks" in plan_data and isinstance(plan_data["weeks"], list):
            for week_data in plan_data["weeks"]:
                week = {
                    "week": week_data.get("week", 1),
                    "objective": week_data.get("objective", "Weekly learning objectives"),
                    "resources": [],
                    "project": week_data.get("project", f"Practice project for Week {week_data.get('week', 1)}")
                }
                
                if "resources" in week_data:
                    for resource in week_data["resources"]:
                        resource_content = resource.get("content", "Educational content for this week's objectives")
                        resource_type = resource.get("type", "educational")
                        resource_title = resource.get("title", "")
                        
                        # Complete truncated content if needed
                        if resource_type == "knowledge-content":
                            print(f"🔧 Processing knowledge content: {resource_title[:50]}...")
                            print(f"🔧 Original length: {len(resource_content)}, Ends with ...: {resource_content.endswith('...')}")
                            resource_content = complete_truncated_content(resource_content, resource_title)
                            print(f"🔧 After completion: {len(resource_content)}")
                        
                        formatted_resource = {
                            "title": resource_title,
                            "type": resource_type,
                            "source": resource.get("source", "Educational Content"),
                            "link": resource.get("link", "#"),
                            "content": resource_content
                        }
                        week["resources"].append(formatted_resource)
                        formatted_plan["metadata"]["total_resources_found"] += 1
                
                formatted_plan["weeks"].append(week)
        
        return formatted_plan
        
    except Exception as e:
        print(f"Error formatting plan: {e}")
        # Return a basic structure if parsing fails
        return {
            "weeks": [{
                "week": 1,
                "objective": f"Learn {user_request.learningGoal} fundamentals",
                "resources": [{
                    "title": f"{user_request.learningGoal} Learning Guide",
                    "type": "educational",
                    "source": "AI Generated",
                    "link": "#",
                    "content": raw_plan[:500] + "..." if len(raw_plan) > 500 else raw_plan
                }],
                "project": f"Complete a beginner {user_request.learningGoal} project"
            }],
            "metadata": {
                "topic": user_request.learningGoal,
                "skill_level": user_request.currentLevel,
                "duration": user_request.duration,
                "time_available": user_request.timeAvailable,
                "preferred_resources": user_request.preferredResources,
                "specific_interests": user_request.specificInterests or "General learning",
                "total_resources_found": 1
            }
        }
@app.post("/api/generate-learning-plan", response_model=LearningPlanResponse)
async def generate_learning_plan(request: LearningPlanRequest):
    """Generate a personalized learning plan based on user input."""
    try:
        print(f"🎯 Generating plan for: {request.learningGoal}")
        print(f"📚 Preferred resources: {request.preferredResources}")
        print(f"⏰ Duration: {request.duration}")
        
        # Modify the learning style to be more specific for better processing
        modified_learning_style = request.preferredResources
        if "YouTube" in request.preferredResources:
            modified_learning_style = "video tutorials and YouTube content"
        elif "Articles" in request.preferredResources:
            modified_learning_style = "articles and blogs"
        elif "Mixed" in request.preferredResources:
            modified_learning_style = "mixed resources"
        
        # Convert API request to internal LearningRequest
        learning_request = LearningRequest(
            skill=request.learningGoal,
            experience_level=request.currentLevel,
            timeline=request.duration,
            time_budget=request.timeAvailable,
            learning_style=modified_learning_style,
            specific_goals=request.specificInterests or ""
        )
        
        # Create the workflow state with enhanced query for resource prioritization
        initial_query = f"learn {request.learningGoal} {request.currentLevel.lower()} level over {request.duration}"
        if "YouTube" in request.preferredResources:
            initial_query += f" using YouTube videos and video tutorials"
        elif "Articles" in request.preferredResources:
            initial_query += f" using articles and blogs"
        else:
            initial_query += f" using {request.preferredResources}"
            
        state = {
            "initial_query": initial_query,
            "learning_request": learning_request,
            "messages": []
        }
        
        # Run the AI workflow
        workflow = create_workflow()
        result = workflow.invoke(state)
        
        # Format the learning plan for better display
        raw_plan = result.get("final_syllabus", "No syllabus generated")
        formatted_plan = format_learning_plan(raw_plan, request)
        
        print(f"✅ Plan generated successfully with {formatted_plan['metadata']['total_resources_found']} resources")
        
        return LearningPlanResponse(
            learning_plan=json.dumps(formatted_plan, indent=2)
        )
        
    except Exception as e:
        print(f"❌ Error generating plan: {e}")
        return LearningPlanResponse(
            error=str(e)
        )

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "AI Learning Planner API is running"}

@app.get("/modern-frontend.html")
async def serve_frontend():
    """Serve the modern frontend HTML file."""
    from fastapi.responses import FileResponse
    html_path = os.path.join(parent_dir, "modern-frontend.html")
    return FileResponse(html_path, media_type="text/html")

@app.get("/")
async def serve_root():
    """Serve the modern frontend HTML file at root."""
    from fastapi.responses import FileResponse
    html_path = os.path.join(parent_dir, "modern-frontend.html")
    return FileResponse(html_path, media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)  # Removed workers for development
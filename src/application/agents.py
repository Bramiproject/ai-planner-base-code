from typing import List, TypedDict, Annotated, Optional
from pydantic import BaseModel
from dataclasses import dataclass
from langchain_core.messages import BaseMessage
import json
import re
from .prompts import (
    ANALYSIS_PROMPT,
    PLANNER_PROMPT,
    RESEARCHER_PROMPT,
    SYLLABUS_AGENT_PROMPT
)
from ..infrastructure.llm import get_model
from ..infrastructure.tools import get_tavily_search_tool, get_youtube_search_tool
from ..infrastructure.content_analyzer import ContentAnalyzer
from ..domain.user_analysis import UserAnalysis

# Structured learning request
@dataclass
class LearningRequest:
    skill: str
    experience_level: str  # "Beginner", "Intermediate", "Advanced"
    timeline: str  # "3 weeks", "2 months", etc. (NO YEARS)
    time_budget: str  # "1 hour/day", "5 hours/week", etc.
    learning_style: str  # "video", "reading", "hands-on", "mixed"
    specific_goals: Optional[str] = None  # Optional specific objectives and additional context

# Mendefinisikan state yang akan melewati graph
class LearningProfile(BaseModel):
    goal: str
    skill_level: str
    total_timeline: str
    time_budget: str
    learning_style: str
    risks: str
    additional_context: str = ""  # Store user's additional constraints/context

class GraphState(TypedDict):
    initial_query: str
    learning_request: Optional[LearningRequest]  # Structured input
    search_keywords: List[str]  # Search keywords derived from learning request
    research_results: str
    analysis_results: LearningProfile
    planning_results: str
    final_syllabus: str
    messages: Annotated[List[str], lambda x, y: x + y]

def create_search_keywords(learning_request: LearningRequest) -> List[str]:
    """Generate search keywords from learning request without transformer."""
    skill = learning_request.skill.lower()
    level = learning_request.experience_level.lower()
    specific_goals = learning_request.specific_goals
    
    keywords = [
        skill,
        f"{skill} {level}",
        f"{skill} tutorial",
        f"{skill} guide",
        f"learn {skill}",
    ]
    
    # Add level-specific keywords
    if level == "beginner":
        keywords.extend([f"{skill} basics", f"{skill} fundamentals", f"{skill} getting started"])
    elif level == "intermediate":
        keywords.extend([f"{skill} intermediate", f"{skill} improving", f"{skill} next level"])
    elif level == "advanced":
        keywords.extend([f"{skill} advanced", f"{skill} expert", f"{skill} mastery"])
    
    # Add specific goals and context to keywords if provided
    if specific_goals:
        # Extract key terms from specific goals and additional context
        goal_words = specific_goals.lower().split()
        for word in goal_words:
            if len(word) > 3:  # Skip short words like "and", "the", etc.
                keywords.append(f"{skill} {word}")
                if word not in ['budget', 'equipment', 'available', 'limitations']:  # Skip common constraint words for separate inclusion
                    keywords.append(word)
    
    return keywords[:12]  # Return top keywords

def format_knowledge_content(content: str) -> str:
    """Format LLM knowledge content into proper markdown."""
    if not content:
        return content
    
    # Clean up the content and format it properly
    lines = content.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('')
            continue
            
        # Format headings
        if line.endswith(':') and (
            'FUNDAMENTALS' in line or 'PRACTICE' in line or 'APPLICATIONS' in line or 
            'PROGRESSION' in line or 'TECHNIQUES' in line or 'MASTERY' in line or 
            'PROFESSIONAL' in line or 'INNOVATION' in line or 'EXPERTISE' in line
        ):
            formatted_lines.append(f"## {line}")
        
        # Format numbered lists
        elif line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.', '9.')):
            formatted_lines.append(f"**{line}**")
        
        # Format bullet points
        elif line.startswith('- '):
            formatted_lines.append(line)
        
        # Format important terms (words in quotes or parentheses)
        elif '"' in line or '(' in line:
            # Bold important terms in quotes
            line = re.sub(r'"([^"]+)"', r'**"\1"**', line)
            formatted_lines.append(line)
        
        # Regular paragraphs
        else:
            formatted_lines.append(line)
    
    formatted_content = '\n'.join(formatted_lines)
    
    # Add some basic structure improvements
    formatted_content = formatted_content.replace('\n\n\n', '\n\n')  # Remove triple newlines
    
    return formatted_content

def researcher_node(state: GraphState):
    """
    OPTIMIZED Researcher Agent with STRICT resource type prioritization.
    """
    print("---🔍 OPTIMIZED RESEARCH WITH STRICT RESOURCE PRIORITIZATION---")
    
    learning_request = state.get("learning_request")
    if not learning_request:
        raise ValueError("Missing learning request")
    
    topic = learning_request.skill.lower()
    skill_level = learning_request.experience_level
    preferred_resource = learning_request.learning_style
    
    print(f"🎯 Topic: {topic}")
    print(f"📈 STRICT Skill Level: {skill_level}")
    print(f"📺 PREFERRED RESOURCE TYPE: {preferred_resource}")
    
    # Initialize search tools
    search_tool = get_tavily_search_tool()
    yt_tool = get_youtube_search_tool()
    
    # STRICT Resource type prioritization logic - 3 options only
    if "YouTube" in preferred_resource or "video" in preferred_resource.lower():
        print("🎬 STRICT PRIORITY: YouTube videos (80% of resources)")
        video_weight = 0.8
        article_weight = 0.2
        max_youtube_searches = 6  # More YouTube searches
        max_web_searches = 2
    elif "Articles" in preferred_resource or "blogs" in preferred_resource.lower():
        print("📚 STRICT PRIORITY: Articles and blogs (90% of resources)")
        video_weight = 0.1
        article_weight = 0.9
        max_youtube_searches = 1
        max_web_searches = 8  # More web searches
    else:  # Default mixed approach for "Mixed resources" or any other option
        print("🔀 BALANCED: Mixed resources approach")
        video_weight = 0.5
        article_weight = 0.5
        max_youtube_searches = 4
        max_web_searches = 4
    
    # Create STRICT skill-level targeted search queries
    level_keywords = {
        "Beginner": ["beginner", "basics", "fundamentals", "getting started", "for beginners", "complete beginner"],
        "Intermediate": ["intermediate", "building skills", "improving", "next level", "intermediate level"],
        "Advanced": ["advanced", "expert", "professional", "mastery", "advanced level", "expert level"]
    }
    
    level_terms = level_keywords.get(skill_level, ["tutorial"])
    
    # Enhanced search with STRICT resource type priority
    base_queries = [
        f"{topic} {level_terms[0]} tutorial",
        f"learn {topic} {skill_level.lower()}",
        f"{topic} {level_terms[1]} guide" if len(level_terms) > 1 else f"{topic} tutorial",
        f"{skill_level.lower()} {topic} course"
    ]
    
    # Add specific goals to search queries if provided - PRIORITIZE THEM
    if learning_request.specific_goals:
        specific_goals = learning_request.specific_goals.lower()
        print(f"🎯 Including specific goals in search: {learning_request.specific_goals}")
        
        goal_queries = [
            f"{specific_goals} {topic} {level_terms[0]}",
            f"how to {specific_goals} {topic}",
            f"{specific_goals} {topic} tutorial"
        ]
        base_queries = goal_queries + base_queries[:2]  # Prioritize goal queries
    
    all_web_results = []
    all_yt_results = []
    
    # PRIORITY-BASED SEARCH EXECUTION
    if video_weight > 0.5:  # Video priority
        print(f"🎬 Prioritizing YouTube search - {max_youtube_searches} searches")
        for query in base_queries[:max_youtube_searches]:
            try:
                yt_query = f"{query} {skill_level.lower()}"
                print(f"🔍 YouTube search: '{yt_query}'")
                yt_results = yt_tool.run(yt_query)
                if yt_results and yt_results.strip():
                    all_yt_results.append(yt_results)
                    print(f"✅ YouTube results found for '{query}'")
                else:
                    print(f"❌ No YouTube results for '{query}'")
            except Exception as e:
                print(f"❌ YouTube search error for '{query}': {e}")
        
        # Limited web search when videos are priority
        print(f"🌐 Limited web search - {max_web_searches} searches")
        for query in base_queries[:max_web_searches]:
            try:
                search_query = f"{query} {skill_level.lower()}"
                print(f"🔍 DEBUG Web search query: '{search_query}'")
                web_results = search_tool.run(search_query)
                print(f"🔍 DEBUG Web search result type: {type(web_results)}")
                print(f"🔍 DEBUG Web search results: {web_results}")
                
                if isinstance(web_results, list):
                    print(f"✅ Got {len(web_results)} web results from Tavily")
                    for i, result in enumerate(web_results[:2]):  # Limit results per query
                        print(f"  Result {i+1}: {result}")
                        if result.get('url') and result.get('title'):
                            # Filter out YouTube URLs from web search
                            if 'youtube.com' in result.get('url', '').lower() or 'youtu.be' in result.get('url', '').lower():
                                print(f"    ❌ Skipped YouTube URL in web search: {result.get('title', 'No title')[:50]}...")
                            else:
                                all_web_results.append(result)
                                print(f"    ✅ Added article: {result.get('title', 'No title')[:50]}...")
                        else:
                            print(f"    ❌ Skipped: Missing URL or title")
                else:
                    print(f"❌ Web results not a list, got: {type(web_results)}")
            except Exception as e:
                print(f"❌ Web search error for '{query}': {e}")
    
    else:  # Article priority
        print(f"🌐 Prioritizing web search - {max_web_searches} searches")
        for query in base_queries[:max_web_searches]:
            try:
                search_query = f"{query} {skill_level.lower()}"
                print(f"🔍 DEBUG Web search query: '{search_query}'")
                web_results = search_tool.run(search_query)
                print(f"🔍 DEBUG Web search result type: {type(web_results)}")
                print(f"🔍 DEBUG Web search results: {web_results}")
                
                if isinstance(web_results, list):
                    print(f"✅ Got {len(web_results)} web results from Tavily")
                    for i, result in enumerate(web_results[:3]):  # More results per query
                        print(f"  Result {i+1}: {result}")
                        if result.get('url') and result.get('title'):
                            # Filter out YouTube URLs from web search
                            if 'youtube.com' in result.get('url', '').lower() or 'youtu.be' in result.get('url', '').lower():
                                print(f"    ❌ Skipped YouTube URL in web search: {result.get('title', 'No title')[:50]}...")
                            else:
                                all_web_results.append(result)
                                print(f"    ✅ Added article: {result.get('title', 'No title')[:50]}...")
                        else:
                            print(f"    ❌ Skipped: Missing URL or title")
                else:
                    print(f"❌ Web results not a list, got: {type(web_results)}")
            except Exception as e:
                print(f"❌ Web search error for '{query}': {e}")
        
        # Limited YouTube search when articles are priority
        print(f"🎬 Limited YouTube search - {max_youtube_searches} searches")
        for query in base_queries[:max_youtube_searches]:
            try:
                yt_results = yt_tool.run(f"{query} {skill_level.lower()}")
                if yt_results and yt_results.strip():
                    all_yt_results.append(yt_results)
            except Exception as e:
                print(f"❌ YouTube search error for '{query}': {e}")
    
    # Extract YouTube URLs more thoroughly
    real_youtube_urls = []
    if all_yt_results:
        for yt_result in all_yt_results:
            # Multiple URL pattern matching
            url_patterns = [
                r'https://www\.youtube\.com/watch\?v=[\w-]+',
                r'https://youtube\.com/watch\?v=[\w-]+',
                r'youtube\.com/watch\?v=[\w-]+',
                r'youtu\.be/[\w-]+'
            ]
            
            for pattern in url_patterns:
                url_matches = re.findall(pattern, str(yt_result))
                for url in url_matches:
                    # Normalize URL
                    if not url.startswith('https://'):
                        url = f"https://www.{url}"
                    if url not in real_youtube_urls:
                        real_youtube_urls.append(url)
    
    print(f"✅ Found {len(all_web_results)} web articles")
    print(f"✅ Found {len(real_youtube_urls)} YouTube videos")
    
    # STRICT resource type validation and intelligent fallback
    if video_weight > 0.5 and len(real_youtube_urls) < 3:
        print(f"⚠️ WARNING: User requested videos but only found {len(real_youtube_urls)}! Adding more web search for alternatives.")
        # Add more web searches to compensate
        for query in base_queries[max_web_searches:max_web_searches+2]:
            try:
                web_results = search_tool.run(f"{query} {skill_level.lower()}")
                if isinstance(web_results, list):
                    for result in web_results[:2]:
                        if result.get('url') and result.get('title'):
                            all_web_results.append(result)
                            print(f"🔄 Added fallback article: {result.get('title', 'Unknown')[:50]}...")
            except Exception as e:
                print(f"❌ Fallback web search error: {e}")
                
    elif article_weight > 0.5 and len(all_web_results) < 3:
        print(f"⚠️ WARNING: User requested articles but only found {len(all_web_results)}! Adding more video search for alternatives.")
        # Add more YouTube searches to compensate
        for query in base_queries[max_youtube_searches:max_youtube_searches+2]:
            try:
                yt_results = yt_tool.run(f"{query} {skill_level.lower()}")
                if yt_results and yt_results.strip():
                    all_yt_results.append(yt_results)
                    print(f"🎬 Added fallback video search results")
            except Exception as e:
                print(f"❌ Fallback YouTube search error: {e}")
        
        # Re-extract YouTube URLs after fallback searches
        if all_yt_results:
            for yt_result in all_yt_results:
                url_patterns = [
                    r'https://www\.youtube\.com/watch\?v=[\w-]+',
                    r'https://youtube\.com/watch\?v=[\w-]+',
                    r'youtube\.com/watch\?v=[\w-]+',
                    r'youtu\.be/[\w-]+'
                ]
                
                for pattern in url_patterns:
                    url_matches = re.findall(pattern, str(yt_result))
                    for url in url_matches:
                        if not url.startswith('https://'):
                            url = f"https://www.{url}"
                        if url not in real_youtube_urls:
                            real_youtube_urls.append(url)
    
    # Prepare research data with STRICT prioritization
    research_data = {
        "search_results": all_web_results[:8],
        "youtube_urls": real_youtube_urls[:10],  # Prioritize videos if requested
        "web_articles": [r for r in all_web_results if r.get('url')],
        "preferred_resource_type": preferred_resource,
        "video_priority": video_weight > 0.5,
        "article_priority": article_weight > 0.5,
        "total_resources": len(all_web_results) + len(real_youtube_urls),
        "resource_distribution": {
            "videos": len(real_youtube_urls),
            "articles": len(all_web_results),
            "video_percentage": len(real_youtube_urls) / max(1, len(all_web_results) + len(real_youtube_urls)) * 100
        }
    }
    
    print(f"📊 Resource distribution: {research_data['resource_distribution']['video_percentage']:.1f}% videos")
    print(f"🎯 Matches preference: {preferred_resource}")
    
    return {"research_results": json.dumps(research_data, indent=2)}

def analysis_node(state: GraphState):
    """
    OPTIMIZED Analysis Agent: Creates learning profile with STRICT skill level preservation.
    """
    print("---📊 ENTERING OPTIMIZED ANALYSIS NODE ---")
    
    # Get learning request and create analysis profile
    learning_request = state.get("learning_request")
    research_data = state.get("research_results", "")
    
    if not learning_request:
        raise ValueError("No learning request found")
    
    # CRITICAL: Preserve the EXACT skill level the user selected
    exact_skill_level = learning_request.experience_level
    print(f"🎯 PRESERVING EXACT skill level: {exact_skill_level}")
    
    # Create analysis profile directly from learning request WITHOUT LLM processing
    goal_description = f"Learn {learning_request.skill} at {exact_skill_level} level"
    if learning_request.specific_goals:
        goal_description += f" with specific focus: {learning_request.specific_goals}"
    
    # Enhanced risk assessment considering additional information
    risks = f"Potential challenges learning {learning_request.skill} with {learning_request.time_budget} time budget at {exact_skill_level} level"
    if learning_request.specific_goals:
        risks += f". Additional considerations: {learning_request.specific_goals}"
    
    # DIRECT mapping without LLM interpretation that could change skill level
    analysis_results = LearningProfile(
        goal=goal_description,
        skill_level=exact_skill_level,  # Use EXACTLY what user selected
        total_timeline=learning_request.timeline,
        time_budget=learning_request.time_budget,
        learning_style=learning_request.learning_style,
        risks=risks,
        additional_context=learning_request.specific_goals or ""
    )
    
    print(f"✅ Analysis complete with PRESERVED skill level: {analysis_results.skill_level}")
    print(f"📋 Goal: {analysis_results.goal}")
    
    return {
        "analysis_results": analysis_results,
        "research_results": research_data
    }

def planner_node(state: GraphState):
    """
    Planner Agent: breaks down the user's goal into major milestone steps.
    """
    print("---✍️ ENTERING PLANNER MODE---")
    analysis_data = state["analysis_results"]
    research_data = state.get("research_results", "")
    query = state["initial_query"]

    profile_json = analysis_data.model_dump_json()
    print(f"---📄 QUERY: {query}---")
    print(f"---📊 DATA ANALYSIS: {profile_json}...")
    print(f"---🔗 RESEARCH LINKS: {research_data[:200]}...") 
    
    model = get_model()
    
    prompt = PLANNER_PROMPT.format(
        analysis_json=profile_json,
        research_links=research_data  
    )
    
    report = model.invoke(prompt)
    
    print("---✅ FINAL PLAN---")
    return {
        "planning_results": report.content,
        "research_results": research_data 
        }

def calculate_resources_per_week(time_budget: str) -> int:
    """
    Calculate appropriate number of resources per week based on user's time budget.
    
    Time Budget Logic:
    - 15-30 min daily: 2-3 resources (light learning)
    - 30-60 min daily: 3-4 resources (moderate learning) 
    - 1-2 hours daily: 4-5 resources (intensive learning)
    - 2+ hours daily: 5-6 resources (very intensive learning)
    - Weekend only: 2-3 resources (concentrated learning)
    """
    if not time_budget:
        return 4  # Default
    
    time_lower = time_budget.lower()
    
    # Parse daily time commitments
    daily_minutes_match = re.search(r'(\d+)\s*(?:minutes?|mins?)\s*(?:daily|per day|a day|each day)', time_lower)
    daily_hours_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(?:daily|per day|a day|each day)', time_lower)
    
    if daily_minutes_match:
        minutes_per_day = int(daily_minutes_match.group(1))
        if minutes_per_day <= 30:
            return 2  # Light: 15-30 min daily
        elif minutes_per_day <= 60:
            return 3  # Moderate: 30-60 min daily  
        else:
            return 4  # Intensive: 60+ min daily
    
    elif daily_hours_match:
        hours_per_day = float(daily_hours_match.group(1))
        if hours_per_day <= 1:
            return 3  # Moderate: up to 1 hour daily
        elif hours_per_day <= 2:
            return 4  # Intensive: 1-2 hours daily
        elif hours_per_day <= 3:
            return 5  # Very intensive: 2-3 hours daily
        else:
            return 6  # Extremely intensive: 3+ hours daily
    
    # Parse weekly time commitments
    weekly_hours_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:hours?|hrs?)\s*(?:weekly|per week|a week|each week)', time_lower)
    if weekly_hours_match:
        hours_per_week = float(weekly_hours_match.group(1))
        if hours_per_week <= 3:
            return 2  # Light: 3 hours/week or less
        elif hours_per_week <= 7:
            return 3  # Moderate: 3-7 hours/week
        elif hours_per_week <= 14:
            return 4  # Intensive: 7-14 hours/week
        else:
            return 5  # Very intensive: 14+ hours/week
    
    # Check for weekend-only patterns
    if any(word in time_lower for word in ['weekend', 'saturday', 'sunday']):
        return 3  # Concentrated weekend learning
    
    # Check for specific mentions that indicate light/heavy workload
    if any(word in time_lower for word in ['busy', 'limited', 'little', 'minimal']):
        return 2  # Conservative approach for busy people
    
    if any(word in time_lower for word in ['intensive', 'dedicated', 'full-time', 'lots', 'plenty']):
        return 5  # More resources for dedicated learners
    
    return 4  # Default fallback

def parse_timeline_efficiently(timeline: str) -> int:
    """Fast timeline parsing - weeks and months only (NO YEARS)"""
    timeline_lower = timeline.lower()
    
    # Single regex search for supported patterns (weeks and months only)
    if 'week' in timeline_lower:
        match = re.search(r'(\d+)', timeline_lower)
        return int(match.group(1)) if match else 4
    elif 'month' in timeline_lower:
        match = re.search(r'(\d+)', timeline_lower)
        return int(match.group(1)) * 4 if match else 4
    
    # Default fallback for any other format
    return 4

def generate_progressive_week_themes(topic: str, skill_level: str, num_weeks: int, specific_goals: str = None) -> dict:
    """Generate HIGHLY UNIQUE progressive themes for each week"""
    goals_modifier = f" with {specific_goals}" if specific_goals else ""
    
    # ENHANCED skill-specific theme progressions with MORE variety
    theme_progressions = {
        "Beginner": [
            f"Foundation Setup and First Steps{goals_modifier}",
            f"Essential Safety and Basic Techniques{goals_modifier}",
            f"Core Skills Development{goals_modifier}",
            f"Confidence Building Through Practice{goals_modifier}",
            f"Connecting Fundamental Concepts{goals_modifier}",
            f"Real-World Application Introduction{goals_modifier}",
            f"Routine Building and Consistency{goals_modifier}",
            f"Error Recognition and Correction{goals_modifier}",
            f"Muscle Memory and Automaticity{goals_modifier}",
            f"Creative Expression Within Basics{goals_modifier}",
            f"Readiness for Intermediate Level{goals_modifier}",
            f"Comprehensive Beginner Assessment{goals_modifier}",
            f"Personal Style Exploration{goals_modifier}",
            f"Community and Support Systems{goals_modifier}",
            f"Goal Setting for Next Phase{goals_modifier}",
            f"Celebrating Beginner Achievements{goals_modifier}"
        ],
        "Intermediate": [
            f"Advanced Technique Refinement{goals_modifier}",
            f"Skill Integration and Combinations{goals_modifier}",
            f"Strategic Problem Solving{goals_modifier}",
            f"Individual Style Development{goals_modifier}",
            f"Efficiency and Speed Optimization{goals_modifier}",
            f"Complex Application Scenarios{goals_modifier}",
            f"Precision and Quality Enhancement{goals_modifier}",
            f"Creative Variation and Innovation{goals_modifier}",
            f"Performance Under Challenge{goals_modifier}",
            f"Knowledge Sharing and Teaching{goals_modifier}",
            f"Professional Standard Achievement{goals_modifier}",
            f"Intermediate Mastery Demonstration{goals_modifier}",
            f"Advanced Challenge Preparation{goals_modifier}",
            f"Portfolio and Documentation{goals_modifier}",
            f"Peer Collaboration and Feedback{goals_modifier}",
            f"Transition to Advanced Concepts{goals_modifier}"
        ],
        "Advanced": [
            f"Expert Technique Mastery{goals_modifier}",
            f"Original Method Innovation{goals_modifier}",
            f"Professional Excellence Standards{goals_modifier}",
            f"Complex Challenge Resolution{goals_modifier}",
            f"Industry Leadership Development{goals_modifier}",
            f"Research and Experimentation{goals_modifier}",
            f"Mentorship and Guidance Skills{goals_modifier}",
            f"Recognition and Credibility Building{goals_modifier}",
            f"Cutting-Edge Technology Integration{goals_modifier}",
            f"Community Leadership and Influence{goals_modifier}",
            f"Expert-Level Validation{goals_modifier}",
            f"Master-Class Achievement{goals_modifier}",
            f"Legacy and Knowledge Transfer{goals_modifier}",
            f"Innovation and Future Trends{goals_modifier}",
            f"Expert Network and Collaboration{goals_modifier}",
            f"Mastery Documentation and Sharing{goals_modifier}"
        ]
    }
    
    themes = theme_progressions.get(skill_level, theme_progressions["Intermediate"])
    
    # Create week mapping with enhanced variety
    week_themes = {}
    for week in range(1, num_weeks + 1):
        # Use different indexing patterns to ensure variety
        if num_weeks <= 12:
            theme_index = (week - 1) % len(themes)
        else:
            # For longer timelines, create more complex progression
            theme_index = ((week - 1) * 3) % len(themes)
        
        week_themes[week] = themes[theme_index]
    
    return week_themes

def generate_fallback_week_content(topic: str, skill_level: str, week_num: int, theme: str, specific_goals: str = None) -> str:
    """Generate detailed fallback content for a specific week"""
    goals_focus = f" focusing specifically on {specific_goals}" if specific_goals else ""
    
    skill_approaches = {
        "Beginner": {
            "intro": f"This week focuses on absolute beginner fundamentals for {topic}.",
            "exercises": [
                "Start with basic setup and equipment familiarization",
                "Practice simple foundational movements",
                "Learn proper safety procedures",
                "Complete easy confidence-building exercises"
            ],
            "tips": "Take your time, focus on form over speed, ask questions when needed."
        },
        "Intermediate": {
            "intro": f"This week builds on your existing {topic} knowledge to develop intermediate skills.",
            "exercises": [
                "Practice complex skill combinations",
                "Work on technique refinement",
                "Solve intermediate-level challenges",
                "Apply skills in practical scenarios"
            ],
            "tips": "Focus on quality and consistency, challenge yourself progressively."
        },
        "Advanced": {
            "intro": f"This week explores advanced {topic} techniques for expert-level development.",
            "exercises": [
                "Master professional-level techniques",
                "Develop innovative approaches",
                "Teach and mentor others",
                "Create original work and solutions"
            ],
            "tips": "Push boundaries, contribute to the field, maintain professional standards."
        }
    }
    
    approach = skill_approaches.get(skill_level, skill_approaches["Intermediate"])
    
    content = f"""## Week {week_num}: {theme}

{approach['intro']}{goals_focus}

**Week {week_num} Objectives:**
- Progress at {skill_level} level in {topic}
- Focus on {theme.lower()}
- Build on previous week's learning

**This Week's Exercises:**
"""
    
    for i, exercise in enumerate(approach['exercises'], 1):
        content += f"{i}. {exercise}\n"
    
    content += f"""
**{skill_level} Level Tips:**
{approach['tips']}

**Progress Indicators:**
By the end of week {week_num}, you should feel more confident with the techniques covered and ready to progress to week {week_num + 1} concepts.
"""
    
    return content

def generate_all_weeks_content_single_call(topic: str, skill_level: str, num_weeks: int, specific_goals: str = None) -> list:
    """Generate ALL week content with COMPLETELY UNIQUE content for each week"""
    print(f"🚀 Generating ALL {num_weeks} COMPLETELY UNIQUE weeks content for {skill_level} level...")
    
    model = get_model()
    
    # STRICT skill-level specific instruction templates
    skill_instructions = {
        "Beginner": "ABSOLUTE BEGINNER content - assume ZERO experience, use simple language, focus on basics and safety, step-by-step instructions",
        "Intermediate": "INTERMEDIATE content - build on existing knowledge, focus on skill improvement and practical application, moderate complexity", 
        "Advanced": "ADVANCED content - assume expertise, focus on mastery, innovation, professional techniques, complex challenges"
    }
    
    goals_section = f"\nSPECIFIC FOCUS: Every week must address {specific_goals} within {topic}." if specific_goals else ""
    
    # Generate weekly progression themes
    week_themes = generate_progressive_week_themes(topic, skill_level, num_weeks, specific_goals)
    
    # Generate each week individually with STRONG uniqueness enforcement
    unique_weeks = []
    used_content_snippets = set()  # Track used content to prevent repetition
    
    for week_num in range(1, num_weeks + 1):
        theme = week_themes.get(week_num, f"Week {week_num} progression")
        
        # Add progression context to make each week truly unique
        progression_context = ""
        if week_num == 1:
            progression_context = "This is the very first week - focus on foundations and getting started."
        elif week_num <= num_weeks // 3:
            progression_context = f"This is early stage (week {week_num} of {num_weeks}) - build on basics."
        elif week_num <= 2 * num_weeks // 3:
            progression_context = f"This is middle stage (week {week_num} of {num_weeks}) - advance skills."
        else:
            progression_context = f"This is advanced stage (week {week_num} of {num_weeks}) - mastery and application."
        
        individual_prompt = f"""Create COMPLETELY UNIQUE {skill_level} learning content for {topic} - Week {week_num} of {num_weeks}.

CRITICAL UNIQUENESS REQUIREMENTS:
- {skill_instructions[skill_level]}
- Week Theme: {theme}
- Progression Stage: {progression_context}
- Must be COMPLETELY DIFFERENT from ALL other weeks
- Week {week_num} specific progression level
- 300-500 words of detailed, unique content{goals_section}
- NO REPETITIVE PHRASES - each week must have unique language and approach

Create week {week_num} specific content with:
1. Week {week_num} unique objectives (different from other weeks)
2. Completely unique exercises ONLY for week {week_num}
3. {skill_level}-appropriate techniques specific to this stage
4. Unique progress indicators for week {week_num}
5. What makes week {week_num} completely different from weeks before and after

UNIQUENESS ENFORCEMENT:
- Use different verbs, adjectives, and structure than other weeks
- Focus on week {week_num} specific skills and challenges
- Make the content progression feel natural and distinct

Format as:
## Week {week_num}: {theme}
[Completely unique {skill_level} content with week-specific exercises and techniques]

Make this week {week_num} content absolutely unique and unrepeatable."""

        try:
            response = model.invoke(individual_prompt)
            week_content = response.content.strip()
            
            # Check for repetitive content and regenerate if needed
            content_snippet = week_content[:100].lower()
            if content_snippet in used_content_snippets:
                print(f"⚠️ Week {week_num}: Detected repetitive content, regenerating...")
                # Try again with stronger uniqueness prompt
                enhanced_prompt = individual_prompt + f"\n\nIMPORTANT: This content must be COMPLETELY different from previous weeks. Use entirely different language, examples, and approach for week {week_num}."
                response = model.invoke(enhanced_prompt)
                week_content = response.content.strip()
            
            used_content_snippets.add(content_snippet)
            formatted_content = format_knowledge_content(week_content)
            unique_weeks.append(formatted_content)
            print(f"✅ Generated UNIQUE Week {week_num} content ({len(week_content)} chars)")
            
        except Exception as e:
            print(f"⚠️ Failed Week {week_num}: {e}")
            # Detailed fallback for each week with enhanced uniqueness
            fallback_content = generate_fallback_week_content(topic, skill_level, week_num, theme, specific_goals)
            unique_weeks.append(fallback_content)
    
    print(f"✅ Generated {len(unique_weeks)} COMPLETELY UNIQUE {skill_level} weeks!")
    return unique_weeks

def extract_resources_efficiently(research_data: str, topic: str, skill_level: str) -> list:
    """Extract and categorize resources with intelligent type alternatives"""
    analyzed_resources = []
    
    try:
        research_obj = json.loads(research_data)
        youtube_urls = research_obj.get("youtube_urls", [])
        web_articles = research_obj.get("web_articles", [])
        preferred_type = research_obj.get("preferred_resource_type", "mixed")
        
        print(f"🔍 Processing {len(youtube_urls)} videos and {len(web_articles)} articles")
        
        # Process YouTube URLs with skill level tagging
        for i, url in enumerate(youtube_urls):
            analyzed_resources.append({
                "title": f"{skill_level} {topic.title()} Video Tutorial {i+1}",
                "url": url,
                "score": 75,
                "type": "video",
                "skill_level": skill_level,
                "preview": f"Video content specifically for {skill_level} learners"
            })
        
        # Process articles with skill level tagging  
        for i, article in enumerate(web_articles):
            if article.get('url'):
                analyzed_resources.append({
                    "title": article.get('title', f"{skill_level} {topic} Article {i+1}"),
                    "url": article['url'],
                    "score": 65,
                    "type": "article", 
                    "skill_level": skill_level,
                    "preview": f"Article content for {skill_level} level"
                })
        
        # Enhanced fallback: Create alternative resources if one type is severely lacking
        video_count = len([r for r in analyzed_resources if r.get("type") == "video"])
        article_count = len([r for r in analyzed_resources if r.get("type") == "article"])
        
        if "video" in preferred_type.lower() and video_count < 2 and article_count > 0:
            # User wanted videos but we have few - create video-style alternatives from articles
            print(f"🔄 Creating video alternatives from {article_count} articles")
            for i, article in enumerate([r for r in analyzed_resources if r.get("type") == "article"][:3]):
                video_alt = article.copy()
                video_alt["title"] = f"{skill_level} {topic.title()} Video-Style Guide {i+1}"
                video_alt["type"] = "video"
                video_alt["preview"] = f"Video-style learning content for {skill_level} learners"
                analyzed_resources.append(video_alt)
                
        elif "article" in preferred_type.lower() and article_count < 2 and video_count > 0:
            # User wanted articles but we have few - create article-style alternatives from videos
            print(f"📚 Creating article alternatives from {video_count} videos")
            for i, video in enumerate([r for r in analyzed_resources if r.get("type") == "video"][:3]):
                article_alt = video.copy()
                article_alt["title"] = f"{skill_level} {topic.title()} Written Guide {i+1}"
                article_alt["type"] = "article"
                article_alt["preview"] = f"Written guide content for {skill_level} learners"
                analyzed_resources.append(article_alt)
                
    except Exception as e:
        print(f"⚠️ JSON parsing failed: {e}")
        # Fallback resource extraction
        urls = re.findall(r'https://[^\s]+', research_data)
        for i, url in enumerate(urls):
            resource_type = "video" if "youtube.com" in url else "article"
            analyzed_resources.append({
                "title": f"{skill_level} {topic} Resource {i+1}",
                "url": url,
                "score": 50,
                "type": resource_type,
                "skill_level": skill_level,
                "preview": f"{skill_level} learning resource"
            })
    
    final_video_count = len([r for r in analyzed_resources if r.get("type") == "video"])
    final_article_count = len([r for r in analyzed_resources if r.get("type") == "article"])
    print(f"✅ Final resources: {final_video_count} videos, {final_article_count} articles")
    
    return analyzed_resources

def distribute_resources_across_weeks(resources: list, num_weeks: int, resources_per_week: int) -> dict:
    """Smart resource distribution with alternative resource types when preferred runs out"""
    print(f"🔄 Distributing {len(resources)} resources across {num_weeks} weeks ({resources_per_week} per week)")
    
    # Calculate total resources needed
    total_needed = num_weeks * (resources_per_week - 1)  # -1 for knowledge content
    
    # Separate resources by type for intelligent distribution
    video_resources = [r for r in resources if r.get("type") == "video"]
    article_resources = [r for r in resources if r.get("type") == "article"]
    
    print(f"📊 Available: {len(video_resources)} videos, {len(article_resources)} articles")
    
    # If we don't have enough resources, use alternative types and duplicates
    if len(resources) < total_needed:
        print(f"⚠️ Need {total_needed} resources but only have {len(resources)}. Using alternatives...")
        
        # Create expanded resource pool with type alternatives
        expanded_resources = resources.copy()
        original_count = len(resources)
        
        # Strategy: Use alternative resource types first, then duplicates
        while len(expanded_resources) < total_needed:
            # First, try to balance resource types
            current_videos = [r for r in expanded_resources if r.get("type") == "video"]
            current_articles = [r for r in expanded_resources if r.get("type") == "article"]
            
            # If we have too many of one type, create alternatives of the other type
            if len(current_videos) > len(current_articles) and article_resources:
                # Create alternative article from existing articles
                source_article = article_resources[len(current_articles) % len(article_resources)]
                alt_article = source_article.copy()
                alt_article["title"] = f"{source_article['title']} (Alternative Resource)"
                alt_article["preview"] = f"{source_article['preview']} - Additional perspective"
                expanded_resources.append(alt_article)
                print(f"🔄 Added alternative article resource")
                
            elif len(current_articles) > len(current_videos) and video_resources:
                # Create alternative video from existing videos
                source_video = video_resources[len(current_videos) % len(video_resources)]
                alt_video = source_video.copy()
                alt_video["title"] = f"{source_video['title']} (Alternative Video)"
                alt_video["preview"] = f"{source_video['preview']} - Additional tutorial"
                expanded_resources.append(alt_video)
                print(f"🎬 Added alternative video resource")
                
            else:
                # Fallback: duplicate any available resource
                if resources:
                    copy_num = (len(expanded_resources) // original_count) + 1
                    source_resource = resources[(len(expanded_resources) - original_count) % len(resources)]
                    modified_resource = source_resource.copy()
                    modified_resource["title"] = f"{source_resource['title']} (Alternative {copy_num})"
                    modified_resource["preview"] = f"{source_resource['preview']} - Additional resource"
                    expanded_resources.append(modified_resource)
                    print(f"📝 Added duplicate resource (Alternative {copy_num})")
            
            # Safety check to prevent infinite loop
            if len(expanded_resources) > total_needed * 2:
                break
        
        resources = expanded_resources[:total_needed]  # Trim to exact needed amount
        print(f"✅ Expanded to {len(resources)} resources with alternative types")
    
    # Distribute resources evenly across weeks with balanced types (MIXED distribution)
    week_resources = {}
    
    # Separate by type for intelligent mixing
    videos = [r for r in resources if r.get("type") == "video"]
    articles = [r for r in resources if r.get("type") == "article"]
    
    print(f"🔀 Mixing resources: {len(videos)} videos, {len(articles)} articles across {num_weeks} weeks")
    
    for week in range(1, num_weeks + 1):
        week_resources[week] = []
        resources_this_week = resources_per_week - 1  # -1 for knowledge content
        
        # Calculate how many of each type for this week based on proportions
        total_videos = len(videos)
        total_articles = len(articles)
        total_resources = total_videos + total_articles
        
        if total_resources > 0:
            # Distribute proportionally but ensure mixing
            target_videos = min(total_videos, max(1, int(resources_this_week * total_videos / total_resources))) if total_videos > 0 else 0
            target_articles = min(total_articles, resources_this_week - target_videos) if total_articles > 0 else 0
            
            # If we have both types, ensure at least some mixing (minimum 1 of minority type if available)
            if total_videos > 0 and total_articles > 0 and resources_this_week >= 2:
                if target_videos == 0 and total_videos > 0:
                    target_videos = 1
                    target_articles = resources_this_week - 1
                elif target_articles == 0 and total_articles > 0:
                    target_articles = 1
                    target_videos = resources_this_week - 1
            
            # Take videos for this week
            for i in range(target_videos):
                if videos:
                    week_resources[week].append(videos.pop(0))
            
            # Take articles for this week
            for i in range(target_articles):
                if articles:
                    week_resources[week].append(articles.pop(0))
        
        # Ensure each week has at least some resources if available
        if len(week_resources[week]) == 0 and (videos or articles):
            if articles:  # Prefer articles if available
                week_resources[week] = [articles.pop(0)]
            elif videos:
                week_resources[week] = [videos.pop(0)]
        
        # Log resource types for this week
        week_videos = sum(1 for r in week_resources[week] if r.get("type") == "video")
        week_articles = sum(1 for r in week_resources[week] if r.get("type") == "article")
        print(f"📋 Week {week}: {len(week_resources[week])} resources ({week_videos} videos, {week_articles} articles)")
    
    return week_resources

def get_skill_level_objectives(skill_level: str, topic: str, num_weeks: int, specific_goals: str = None) -> dict:
    """Pre-built skill-specific objectives - no LLM calls needed"""
    goals_suffix = f" focusing on {specific_goals}" if specific_goals else ""
    
    templates = {
        "Beginner": [
            f"Learn absolute basics of {topic} - complete beginner introduction{goals_suffix}",
            f"Master basic {topic} fundamentals and safety for beginners{goals_suffix}",
            f"Practice simple {topic} techniques with beginner exercises{goals_suffix}",
            f"Apply basic beginner {topic} skills in easy first projects{goals_suffix}",
            f"Build consistency in beginner {topic} practice{goals_suffix}",
            f"Prepare to advance from beginner to intermediate {topic}{goals_suffix}"
        ],
        "Intermediate": [
            f"Refine existing {topic} skills with intermediate techniques{goals_suffix}",
            f"Learn advanced intermediate {topic} methods and applications{goals_suffix}",
            f"Practice complex {topic} combinations and skill integration{goals_suffix}",
            f"Master challenging intermediate {topic} projects{goals_suffix}",
            f"Develop personal intermediate style in {topic}{goals_suffix}",
            f"Prepare for advanced {topic} learning and specialization{goals_suffix}"
        ],
        "Advanced": [
            f"Master expert-level {topic} techniques and professional methods{goals_suffix}",
            f"Develop innovative advanced {topic} approaches{goals_suffix}",
            f"Apply professional {topic} standards and industry practices{goals_suffix}",
            f"Create original advanced {topic} work and innovations{goals_suffix}",
            f"Teach {topic} to others and mentor learners{goals_suffix}",
            f"Achieve complete {topic} mastery and expertise{goals_suffix}"
        ]
    }
    
    level_objectives = templates.get(skill_level, templates["Intermediate"])
    
    # Return dictionary with week numbers
    objectives_dict = {}
    for i in range(num_weeks):
        objectives_dict[i + 1] = level_objectives[i % len(level_objectives)]
    
    return objectives_dict

def generate_skill_level_project(skill_level: str, topic: str, week_num: int, specific_goals: str = None) -> str:
    """Generate skill-appropriate project without LLM call"""
    goals_focus = f" incorporating {specific_goals}" if specific_goals else ""
    
    templates = {
        "Beginner": f"Complete a simple beginner {topic} project for week {week_num} - easy and confidence-building{goals_focus}",
        "Intermediate": f"Create an intermediate {topic} project for week {week_num} - challenging but achievable{goals_focus}",
        "Advanced": f"Design an advanced {topic} project for week {week_num} - expert-level and innovative{goals_focus}"
    }
    return templates.get(skill_level, f"Apply Week {week_num} {topic} skills in a project{goals_focus}")

def syllabus_creation_node(state: GraphState):
    """OPTIMIZED Syllabus Agent with UNIQUE content and CONSISTENT resource distribution"""
    print("---📚 GENERATING OPTIMIZED SYLLABUS WITH UNIQUE CONTENT ---")
    
    profile = state["analysis_results"]
    research_data = state.get("research_results", "")
    learning_request = state.get("learning_request")
    
    topic = learning_request.skill.lower() if learning_request else "the topic"
    
    # OPTIMIZATION 1: Fast timeline parsing
    num_weeks = parse_timeline_efficiently(profile.total_timeline)
    
    print(f"🕒 Timeline: {profile.total_timeline} -> {num_weeks} weeks")
    print(f"📊 STRICT Skill Level: {profile.skill_level}")
    
    # OPTIMIZATION 2: Extract all resources efficiently
    analyzed_resources = extract_resources_efficiently(research_data, topic, profile.skill_level)
    
    # Calculate resources per week
    time_budget = learning_request.time_budget if learning_request else ""
    resources_per_week = calculate_resources_per_week(time_budget)
    
    print(f"🎯 Time Budget: '{time_budget}' → {resources_per_week} resources per week")
    
    # OPTIMIZATION 3: Smart resource distribution across ALL weeks
    week_resource_distribution = distribute_resources_across_weeks(analyzed_resources, num_weeks, resources_per_week)
    
    # OPTIMIZATION 4: Generate UNIQUE content for each week
    specific_goals = learning_request.specific_goals if learning_request else None
    all_week_content = generate_all_weeks_content_single_call(topic, profile.skill_level, num_weeks, specific_goals)
    
    print(f"Using {len(analyzed_resources)} total resources distributed across {num_weeks} weeks")
    
    # STRICT skill level objectives
    level_objectives = get_skill_level_objectives(profile.skill_level, topic, num_weeks, specific_goals)
    
    # Build curriculum with CONSISTENT resource distribution
    weeks = []
    
    for week_num in range(1, num_weeks + 1):
        objective = level_objectives.get(week_num, f"Week {week_num} {profile.skill_level.lower()} {topic}")
        
        # Get pre-distributed resources for this week
        week_resources = []
        distributed_resources = week_resource_distribution.get(week_num, [])
        
        # Convert to proper format
        for resource in distributed_resources:
            resource_type = resource.get("type", "article")
            source = "YouTube" if resource_type == "video" else "Web Article"
            
            week_resources.append({
                "title": resource.get("title", "Learning Resource"),
                "link": resource.get("url", ""),
                "type": resource_type,
                "source": source,
                "content": f"Skill Level: {resource.get('skill_level', 'General')}. {resource.get('preview', '')}"
            })
        
        # Add unique knowledge content for this week
        if week_num <= len(all_week_content) and all_week_content[week_num - 1]:
            week_resources.append({
                "title": f"Week {week_num}: {profile.skill_level} {topic.title()} Learning Guide",
                "link": "Knowledge-Based Content",
                "type": "knowledge-content",
                "source": "LLM Knowledge",
                "content": all_week_content[week_num - 1]
            })
        
        # Ensure minimum resources per week
        while len(week_resources) < resources_per_week:
            week_resources.append({
                "title": f"Week {week_num}: Supplementary {profile.skill_level} Practice",
                "link": "Knowledge-Based Content",
                "type": "knowledge-content",
                "source": "LLM Knowledge",
                "content": f"## Week {week_num} Supplementary Practice\n\nAdditional {profile.skill_level}-level practice and review for week {week_num} of your {topic} learning journey."
            })
        
        # Skill-specific projects
        project = generate_skill_level_project(profile.skill_level, topic, week_num, specific_goals)
        
        weeks.append({
            "week": week_num,
            "objective": objective,
            "resources": week_resources,
            "project": project
        })
        
        print(f"✅ Week {week_num}: {len(week_resources)} resources assigned")
    
    # Create final JSON
    syllabus = {
        "weeks": weeks,
        "metadata": {
            "total_resources_analyzed": len(analyzed_resources),
            "topic": topic,
            "skill_level": profile.skill_level,
            "timeline": profile.total_timeline,
            "optimization": "unique_content_consistent_distribution",
            "resources_per_week": resources_per_week,
            "total_weeks": num_weeks
        }
    }
    
    print("---✅ OPTIMIZED SYLLABUS WITH UNIQUE CONTENT READY ---")
    return {"final_syllabus": json.dumps(syllabus, indent=2)}

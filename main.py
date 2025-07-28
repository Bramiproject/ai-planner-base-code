import os
from dotenv import load_dotenv
from src.application.graph import create_workflow
from src.application.user_input_handler import collect_user_inputs, create_search_query

# Muat environment variables dari file .env
load_dotenv()

def main():
    # Validasi API keys
    if not os.getenv("TAVILY_API_KEY"):
        print("Error: Pastikan GOOGLE_APPLICATION_CREDENTIALS dan TAVILY_API_KEY sudah diatur di file .env")
        return

    print("=== AI Learning Planner ===\n")
    
    # Collect structured inputs (much cleaner!)
    learning_request = collect_user_inputs()
    
    print(f"\n✅ Got it! Creating a {learning_request.timeline} learning plan for {learning_request.skill}")
    print(f"📊 Level: {learning_request.experience_level}")
    print(f"⏰ Time budget: {learning_request.time_budget}")
    print(f"🎨 Style: {learning_request.learning_style}")
    
    # Create a clean query for the system
    clean_query = create_search_query(learning_request)
    
    # Membuat alur kerja (graph)
    app = create_workflow()
    
    # Menjalankan alur kerja dengan structured data
    print("\n---Starting---")
    inputs = {
        "initial_query": clean_query,
        "learning_request": learning_request  # Pass structured data
    }
    
    # `stream` bisa digunakan untuk melihat progres, `invoke` untuk hasil akhir
    final_state = app.invoke(inputs)

    # Menampilkan laporan akhir
    print("\n\n---📄 LEARNING PLAN 📄---")
    
    # Parse JSON and convert to readable text format
    try:
        import json
        syllabus_data = json.loads(final_state["final_syllabus"])
        
        # Display metadata if available
        if "metadata" in syllabus_data:
            metadata = syllabus_data["metadata"]
            print(f"📚 Topic: {metadata.get('topic', 'N/A').title()}")
            print(f"📊 Level: {metadata.get('skill_level', 'N/A')}")
            print(f"⏰ Timeline: {metadata.get('timeline', 'N/A')}")
            print(f"🔍 Resources Analyzed: {metadata.get('total_resources_analyzed', 'N/A')}")
            print(f"🎯 Strategy: {metadata.get('research_strategy', 'N/A')}")
            print("\n" + "="*80 + "\n")
        
        # Display weeks in text format
        for week_data in syllabus_data.get("weeks", []):
            week_num = week_data.get("week", 1)
            objective = week_data.get("objective", "No objective")
            project = week_data.get("project", "No project")
            resources = week_data.get("resources", [])
            
            print(f"📅 WEEK {week_num}")
            print(f"🎯 Objective: {objective}")
            print(f"📋 Project: {project}")
            print(f"📚 Resources ({len(resources)} items):")
            print("-" * 60)
            
            for i, resource in enumerate(resources, 1):
                title = resource.get("title", "Untitled")
                link = resource.get("link", "No link")
                res_type = resource.get("type", "unknown")
                source = resource.get("source", "Unknown")
                content = resource.get("content", "No content available")
                
                print(f"\n{i}. {title}")
                print(f"   Type: {res_type.title()}")
                print(f"   Source: {source}")
                
                if link != "Knowledge-Based Content":
                    print(f"   Link: {link}")
                
                if content and content.strip():
                    print(f"   Content: {content}")
                else:
                    print(f"   Content: External resource - visit the link above")
            
            print("\n" + "="*80 + "\n")
        
    except json.JSONDecodeError:
        # Fallback: display raw output if JSON parsing fails
        print(final_state["final_syllabus"])
    
    print("---🏁 END---")

if __name__ == "__main__":
    main()
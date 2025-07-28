import os
from dotenv import load_dotenv
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from youtubesearchpython import VideosSearch

# Load environment variables
load_dotenv()

def get_tavily_search_tool():
    """Menginisialisasi dan mengembalikan tool pencarian Tavily."""
    # Tavily adalah tool pencarian yang kuat dan sering digunakan dalam alur kerja agen.

    api_key = os.getenv("TAVILY_API_KEY")
    return TavilySearchResults(
        max_results=5, 
        tavily_api_key=api_key
    )

def youtube_search(query: str, max_results: int = 3) -> str:
    print(f"🔍 Searching YouTube for: {query}")
    
    # Use Tavily to search for YouTube videos directly
    try:
        api_key = os.getenv("TAVILY_API_KEY")
        if not api_key:
            print("❌ No Tavily API key found")
            return "YouTube search unavailable (no API key)"
        
        tavily = TavilySearchResults(max_results=max_results, tavily_api_key=api_key)
        
        # Search for YouTube videos using Tavily
        search_query = f"site:youtube.com {query} tutorial"
        print(f"🔍 Tavily YouTube search: {search_query}")
        
        web_results = tavily.run(search_query)
        
        if not web_results or not isinstance(web_results, list):
            print("❌ No YouTube results from Tavily")
            return "No YouTube videos found"
        
        # Format results
        output = []
        for i, result in enumerate(web_results[:max_results]):
            if isinstance(result, dict) and result.get('url') and 'youtube.com' in result.get('url', ''):
                title = result.get('title', f'YouTube Video {i+1}')
                url = result.get('url', '')
                content = result.get('content', '')
                if len(content) > 150:
                    content = content[:150] + "..."
                
                output.append(f"Title: {title}\nURL: {url}\nDescription: {content}")
        
        if output:
            print(f"✅ Found {len(output)} YouTube videos")
            return "\n\n".join(output)
        else:
            print("❌ No valid YouTube URLs found")
            return "No YouTube videos found"
            
    except Exception as e:
        print(f"❌ YouTube search error: {e}")
        return "YouTube search temporarily unavailable"

def get_youtube_search_tool():
    return Tool(
        name="YouTubeSearch",
        func=youtube_search,
        description="Searches YouTube for videos related to the input query. Returns top results with titles and URLs."
    )

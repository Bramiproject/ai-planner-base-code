import os
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults

def get_tavily_search_tool():
    """Menginisialisasi dan mengembalikan tool pencarian Tavily."""
    # Tavily adalah tool pencarian yang kuat dan sering digunakan dalam alur kerja agen.

    api_key = os.getenv("TAVILY_API_KEY")
    return TavilySearchResults(
        max_results=5, 
        tavily_api_key=api_key
    )
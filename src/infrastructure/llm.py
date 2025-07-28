import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
# Remove the incorrect import - not needed for the current setup
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearchResults

# Load environment variables
load_dotenv()

def get_model():
    """Menginisialisasi dan mengembalikan model Gemini."""
    # Menggunakan model yang mendukung pemanggilan fungsi (tool calling) dengan baik
    
    api_key = os.getenv("QWEN_API_KEY")
    api_base = os.getenv("QWEN_BASE_URL")
    model = os.getenv("QWEN_MODEL")
    return ChatOpenAI(
        openai_api_key=api_key,
        openai_api_base=api_base,
        model_name=model,
        temperature=0.5,  # Moderate temperature for balanced creativity
        top_p=0.1,        # Very low for extremely focused responses
        max_tokens=16000,  # Maximum limit for complete content generation
    )
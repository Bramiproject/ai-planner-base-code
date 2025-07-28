import re
import requests
from youtube_transcript_api import YouTubeTranscriptApi
from bs4 import BeautifulSoup
from typing import Dict, Optional, List
import time

class ContentAnalyzer:
    """Analyzes YouTube videos and web articles to extract relevant content."""
    
    def __init__(self):
        self.max_transcript_length = 2000  # Limit transcript length
        self.max_article_length = 1500     # Limit article content length
    
    def extract_youtube_video_id(self, url: str) -> Optional[str]:
        """Extract video ID from YouTube URL."""
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
            r'youtube\.com/watch\?.*v=([^&\n?#]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_youtube_transcript(self, video_url: str) -> Dict[str, str]:
        """Get YouTube video transcript and basic info."""
        try:
            video_id = self.extract_youtube_video_id(video_url)
            if not video_id:
                return {"error": "Invalid YouTube URL", "content": ""}
            
            # Get transcript
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine transcript text
            full_transcript = " ".join([entry['text'] for entry in transcript_list])
            
            # Truncate if too long
            if len(full_transcript) > self.max_transcript_length:
                full_transcript = full_transcript[:self.max_transcript_length] + "..."
            
            # Get video title from URL (basic extraction)
            title = self.get_youtube_title(video_url)
            
            return {
                "title": title,
                "content": full_transcript,
                "type": "youtube_video",
                "url": video_url,
                "video_id": video_id
            }
            
        except Exception as e:
            return {
                "error": f"Failed to get transcript: {str(e)}",
                "content": "",
                "url": video_url
            }
    
    def get_youtube_title(self, video_url: str) -> str:
        """Extract YouTube video title."""
        try:
            video_id = self.extract_youtube_video_id(video_url)
            if not video_id:
                return "YouTube Video"
            
            # Simple title extraction using requests
            response = requests.get(f"https://www.youtube.com/watch?v={video_id}", timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.replace(' - YouTube', '').strip()
                    return title[:100]  # Limit title length
            
            return "YouTube Video"
            
        except Exception:
            return "YouTube Video"
    
    def get_article_content(self, article_url: str) -> Dict[str, str]:
        """Extract content from web article."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(article_url, headers=headers, timeout=15)
            if response.status_code != 200:
                return {"error": "Failed to fetch article", "content": "", "url": article_url}
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "header", "footer", "aside"]):
                script.decompose()
            
            # Get title
            title_tag = soup.find('title')
            title = title_tag.text.strip() if title_tag else "Web Article"
            title = title[:100]  # Limit title length
            
            # Get main content (try different selectors)
            content_selectors = [
                'article', 'main', '.content', '.post-content', 
                '.entry-content', '.article-content', 'div.content'
            ]
            
            content = ""
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    content = elements[0].get_text(strip=True, separator=' ')
                    break
            
            # Fallback to body if no specific content found
            if not content:
                body = soup.find('body')
                if body:
                    content = body.get_text(strip=True, separator=' ')
            
            # Clean and truncate content
            content = re.sub(r'\s+', ' ', content)  # Remove extra whitespace
            if len(content) > self.max_article_length:
                content = content[:self.max_article_length] + "..."
            
            return {
                "title": title,
                "content": content,
                "type": "web_article",
                "url": article_url
            }
            
        except Exception as e:
            return {
                "error": f"Failed to extract article: {str(e)}",
                "content": "",
                "url": article_url
            }
    
    def analyze_content_relevance(self, content_data: Dict[str, str], target_topic: str, target_level: str) -> Dict[str, any]:
        """Analyze how relevant the content is to the target topic and level."""
        content = content_data.get("content", "").lower()
        title = content_data.get("title", "").lower()
        target_topic = target_topic.lower()
        target_level = target_level.lower()
        
        # Calculate relevance score
        relevance_score = 0
        
        # Topic relevance (40% of score)
        topic_matches = content.count(target_topic) + title.count(target_topic) * 2
        relevance_score += min(topic_matches * 10, 40)
        
        # Level relevance (30% of score)
        level_keywords = {
            "beginner": ["beginner", "basic", "introduction", "getting started", "fundamentals"],
            "intermediate": ["intermediate", "advanced", "next level", "improve", "enhance"],
            "advanced": ["advanced", "expert", "professional", "master", "complex"]
        }
        
        if target_level in level_keywords:
            for keyword in level_keywords[target_level]:
                if keyword in content or keyword in title:
                    relevance_score += 6
        
        # Quality indicators (30% of score)
        quality_keywords = ["tutorial", "guide", "how to", "step by step", "learn", "course"]
        for keyword in quality_keywords:
            if keyword in content or keyword in title:
                relevance_score += 5
        
        # Cap score at 100
        relevance_score = min(relevance_score, 100)
        
        return {
            **content_data,
            "relevance_score": relevance_score,
            "is_relevant": relevance_score >= 30  # Threshold for relevance
        }
    
    def analyze_multiple_resources(self, urls: List[str], target_topic: str, target_level: str) -> List[Dict[str, any]]:
        """Analyze multiple resources and return them sorted by relevance."""
        analyzed_resources = []
        
        for url in urls:
            print(f"🔍 Analyzing: {url[:50]}...")
            
            try:
                if "youtube.com" in url or "youtu.be" in url:
                    content_data = self.get_youtube_transcript(url)
                else:
                    content_data = self.get_article_content(url)
                
                # Analyze relevance
                if content_data.get("content"):
                    analyzed_resource = self.analyze_content_relevance(content_data, target_topic, target_level)
                    analyzed_resources.append(analyzed_resource)
                    print(f"  ✅ Score: {analyzed_resource.get('relevance_score', 0)}/100")
                else:
                    print(f"  ❌ No content extracted")
                
                # Add small delay to be respectful
                time.sleep(1)
                
            except Exception as e:
                print(f"  ❌ Error analyzing {url}: {str(e)}")
        
        # Sort by relevance score (highest first)
        analyzed_resources.sort(key=lambda x: x.get('relevance_score', 0), reverse=True)
        
        return analyzed_resources

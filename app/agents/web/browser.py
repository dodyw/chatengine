"""
Web browsing functionality using newspaper3k and BeautifulSoup.
"""

from newspaper import Article
from bs4 import BeautifulSoup
import requests
from typing import Dict, Optional
from .utils import clean_text

def browse_web(url: str, task: str = "summarize") -> Dict[str, str]:
    """
    Browse a webpage and extract/process its content based on the task.
    
    Args:
        url: The URL to browse
        task: The task to perform ("summarize", "extract", etc.)
    
    Returns:
        Dict containing the processed content and metadata
    """
    try:
        # Initialize article
        article = Article(url)
        
        # Download and parse
        article.download()
        article.parse()
        
        # Get basic content
        content = {
            "title": article.title,
            "text": article.text,
            "url": url,
            "authors": article.authors,
            "publish_date": str(article.publish_date) if article.publish_date else None,
        }
        
        # Perform NLP if summarization is needed
        if task == "summarize":
            article.nlp()
            content["summary"] = article.summary
            content["keywords"] = article.keywords
        
        return {
            "status": "success",
            "content": content
        }
        
    except Exception as e:
        # Fallback to basic HTML parsing if newspaper3k fails
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content and clean it
            text = clean_text(soup.get_text())
            
            return {
                "status": "success",
                "content": {
                    "title": soup.title.string if soup.title else "No title found",
                    "text": text[:5000],  # Limit text length
                    "url": url,
                }
            }
            
        except Exception as inner_e:
            return {
                "status": "error",
                "error": str(inner_e)
            } 
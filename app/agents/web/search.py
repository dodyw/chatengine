"""
Web search functionality using Google Custom Search API.
"""

import os
from typing import Dict, List
from googleapiclient.discovery import build
from .browser import browse_web
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_web(query: str, num_results: int = 5) -> Dict[str, any]:
    """
    Search the web using Google Custom Search API and return relevant results.
    
    Args:
        query: The search query
        num_results: Number of results to return (max 10)
    
    Returns:
        Dict containing search results or error message
    """
    try:
        # Get API credentials from environment variables
        api_key = os.getenv('GOOGLE_API_KEY')
        cx = os.getenv('GOOGLE_CSE_ID')
        
        if not api_key or not cx:
            return {
                "status": "error",
                "error": "Google API credentials not found. Please set GOOGLE_API_KEY and GOOGLE_CSE_ID environment variables."
            }
        
        # Build the service
        service = build('customsearch', 'v1', developerKey=api_key)
        
        # Execute the search
        result = service.cse().list(q=query, cx=cx, num=min(num_results, 10)).execute()
        
        if 'items' not in result:
            return {
                "status": "error",
                "error": "No results found"
            }
            
        # Process results
        processed_results = []
        for item in result['items']:
            # Try to get more detailed content using browse_web
            try:
                detailed_content = browse_web(item['link'])
                if detailed_content['status'] == 'success':
                    content = detailed_content['content']
                else:
                    content = {
                        'title': item.get('title', ''),
                        'text': item.get('snippet', ''),
                        'url': item.get('link', '')
                    }
            except:
                content = {
                    'title': item.get('title', ''),
                    'text': item.get('snippet', ''),
                    'url': item.get('link', '')
                }
            
            processed_results.append(content)
        
        return {
            "status": "success",
            "results": processed_results
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        } 
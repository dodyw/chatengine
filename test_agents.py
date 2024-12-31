"""
Test script for agent functionality.
"""

from app.agents import browse_web, search_web
import os

def test_web_browse():
    print("\nTesting web browsing...")
    # Test with a reliable website
    result = browse_web("https://example.com")
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        content = result['content']
        print(f"\nTitle: {content['title']}")
        print(f"Text excerpt: {content['text'][:200]}...")
    else:
        print(f"Error: {result.get('error')}")

def test_web_search():
    print("\nTesting web search...")
    result = search_web("USD to IDR exchange rate today", num_results=2)
    print(f"Status: {result['status']}")
    if result['status'] == 'success':
        for idx, item in enumerate(result['results'], 1):
            print(f"\n--- Result {idx} ---")
            print(f"Title: {item['title']}")
            print(f"URL: {item['url']}")
            # Try to extract exchange rate information
            text = item['text'].lower()
            rate_lines = [line.strip() for line in text.split('\n') 
                         if ('usd' in line.lower() or 'dollar' in line.lower()) 
                         and ('idr' in line.lower() or 'rupiah' in line.lower())
                         and any(x in line.lower() for x in ['=', 'rate', 'price'])]
            if rate_lines:
                print("\nExchange Rate Information:")
                for line in rate_lines[:2]:
                    print(f"  {line}")
    else:
        print(f"Error: {result.get('error')}")
        print("\nDebug info:")
        print(f"API Key length: {len(os.getenv('GOOGLE_API_KEY', ''))}")
        print(f"CSE ID length: {len(os.getenv('GOOGLE_CSE_ID', ''))}")

if __name__ == "__main__":
    print("Testing Agent Functions")
    print("=" * 50)
    
    test_web_browse()
    test_web_search() 
"""
FastAPI server with chat endpoint for web search and browsing.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agents import search_web, browse_web
from typing import Optional
import re

app = FastAPI()

class ChatMessage(BaseModel):
    message: str

def extract_exchange_rate(text: str) -> Optional[str]:
    # Look for patterns like "1 USD = X IDR" or "1.00 US dollar = X Indonesian rupiah"
    patterns = [
        r'1(?:\.00)?\s*(?:USD|US dollar)\s*=\s*([\d,\.]+)\s*(?:IDR|Indonesian rupiah)',
        r'1(?:\.00)?\s*(?:USD|US dollar)\s*=\s*([\d,\.]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            rate = match.group(1)
            # Clean up the rate
            rate = rate.replace(',', '')
            try:
                rate_float = float(rate)
                return f"1 USD = IDR {rate_float:,.2f}"
            except ValueError:
                continue
    return None

@app.post("/chat")
async def chat(chat_message: ChatMessage):
    try:
        message = chat_message.message.lower()
        
        # Handle exchange rate query
        if "exchange rate" in message or ("usd" in message and "idr" in message):
            result = search_web("current USD to IDR exchange rate today", num_results=2)
            
            if result['status'] == 'success':
                for item in result['results']:
                    text = item['text'].lower()
                    # Try to extract a clean exchange rate
                    rate = extract_exchange_rate(text)
                    if rate:
                        return {
                            "status": "success",
                            "message": f"Current Exchange Rate:\n{rate}",
                            "source": item['url'],
                            "timestamp": "Data from XE.com"
                        }
            
            return {
                "status": "error",
                "message": "Could not find current exchange rate information."
            }
        
        # Handle web browsing query
        elif "browse" in message or "visit" in message or "open" in message:
            # Extract URL from message
            words = message.split()
            for word in words:
                if word.startswith(("http://", "https://")):
                    result = browse_web(word)
                    if result['status'] == 'success':
                        content = result['content']
                        return {
                            "status": "success",
                            "message": f"Title: {content['title']}\n\nContent: {content['text'][:500]}..."
                        }
        
        return {
            "status": "error",
            "message": "I'm not sure how to handle that request. Try asking about exchange rates or browsing a website."
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

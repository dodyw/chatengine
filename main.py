from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.agents import search_web, browse_web
from typing import Optional

app = FastAPI()

class ChatMessage(BaseModel):
    message: str

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
                    rate_lines = [line.strip() for line in text.split('\n') 
                                if ('usd' in line.lower() or 'dollar' in line.lower()) 
                                and ('idr' in line.lower() or 'rupiah' in line.lower())
                                and any(x in line.lower() for x in ['=', 'rate', 'price'])]
                    if rate_lines:
                        return {
                            "status": "success",
                            "message": f"Exchange Rate Information:\n{rate_lines[0]}",
                            "source": item['url']
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
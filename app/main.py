import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from openai import AzureOpenAI, OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize AI client based on provider
provider = os.getenv("AI_PROVIDER", "azure").lower()  # Default to azure if not specified

if provider == "azure":
    client = AzureOpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("OPENAI_API_BASE")
    )
else:  # OpenAI or other providers using OpenAI's API format
    client = OpenAI(
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url=os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")  # Default to OpenAI's API
    )

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories for each session
chat_histories: Dict[str, List[Dict[str, str]]] = {}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str

def get_history(session_id: str = "default") -> List[Dict[str, str]]:
    if session_id not in chat_histories:
        # Initialize with system message
        chat_histories[session_id] = [{
            "role": "system",
            "content": "You are a helpful AI assistant. Remember to keep track of user details they share with you, like their name."
        }]
    return chat_histories[session_id]

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Chat API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Get or create history for this session
        history = get_history(request.session_id)
        
        # Add the new message to history
        last_message = {
            "role": request.messages[-1].role,
            "content": request.messages[-1].content
        }
        history.append(last_message)

        # Get response from the model
        if provider == "azure":
            model = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        else:
            model = os.getenv("OPENAI_MODEL_NAME", "gpt-4")  # Default to gpt-4 if not specified
            
        response = client.chat.completions.create(
            model=model,
            messages=history,
            temperature=0.7,
        )
        
        # Extract and store the assistant's response
        assistant_message = {
            "role": "assistant",
            "content": response.choices[0].message.content
        }
        history.append(assistant_message)
        
        return ChatResponse(response=assistant_message["content"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        history = get_history(session_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    try:
        if session_id in chat_histories:
            # Reset history with system message
            chat_histories[session_id] = [{
                "role": "system",
                "content": "You are a helpful AI assistant. Remember to keep track of user details they share with you, like their name."
            }]
            return {"message": f"History cleared for session {session_id}"}
        return {"message": f"No history found for session {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

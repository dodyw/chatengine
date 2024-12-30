import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict
from langchain_openai import AzureChatOpenAI
from langchain.memory import ChatMessageHistory
from langchain.schema import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Debug prints
print("Environment variables:")
print(f"AZURE_OPENAI_API_KEY: {os.getenv('AZURE_OPENAI_API_KEY')}")
print(f"AZURE_OPENAI_API_BASE: {os.getenv('AZURE_OPENAI_API_BASE')}")
print(f"AZURE_OPENAI_API_VERSION: {os.getenv('AZURE_OPENAI_API_VERSION')}")
print(f"AZURE_OPENAI_DEPLOYMENT_NAME: {os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')}")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store chat histories for each session
chat_histories: Dict[str, ChatMessageHistory] = {}

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str

def get_history(session_id: str = "default") -> ChatMessageHistory:
    if session_id not in chat_histories:
        history = ChatMessageHistory()
        # Add a system message to help with context
        history.add_message(SystemMessage(content="You are a helpful AI assistant. Remember to keep track of user details they share with you, like their name."))
        chat_histories[session_id] = history
    return chat_histories[session_id]

@app.get("/")
def read_root():
    return {"Hello": "Welcome to the Chat API"}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        # Initialize Azure OpenAI chat model
        chat = AzureChatOpenAI(
            openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
            azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),
            openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            temperature=0.7,
        )

        # Get or create history for this session
        history = get_history(request.session_id)
        
        # Add the new message to history
        last_message = request.messages[-1].content
        history.add_user_message(last_message)

        # Create messages list from history
        messages = history.messages

        # Get response from the model
        response = chat.invoke(messages)
        
        # Add the AI's response to history
        history.add_ai_message(response.content)
        
        return ChatResponse(response=response.content)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    try:
        history = get_history(session_id)
        formatted_history = []
        
        for message in history.messages:
            if isinstance(message, HumanMessage):
                formatted_history.append({"role": "user", "content": message.content})
            elif isinstance(message, AIMessage):
                formatted_history.append({"role": "assistant", "content": message.content})
            elif isinstance(message, SystemMessage):
                formatted_history.append({"role": "system", "content": message.content})
                
        return {"history": formatted_history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/chat/history/{session_id}")
async def clear_chat_history(session_id: str):
    try:
        if session_id in chat_histories:
            chat_histories[session_id] = ChatMessageHistory()
            return {"message": f"History cleared for session {session_id}"}
        return {"message": f"No history found for session {session_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

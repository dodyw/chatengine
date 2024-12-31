# Chatbot API

A FastAPI-based chatbot API that uses Azure OpenAI's official Python library.

## Capabilities

- Stateful chat conversations with Azure OpenAI's GPT models
- Session-based chat history management
- Multiple concurrent chat sessions support
- RESTful API endpoints for chat interactions
- Real-time message processing
- Secure credential management through environment variables
- Easy-to-use API with comprehensive documentation

## Session Management

The API uses a simple but effective in-memory session management system:

- Each conversation is identified by a unique `session_id`
- Sessions maintain their chat history, including system, user, and assistant messages
- Sessions persist until explicitly cleared or server restart
- Each session starts with a system message that sets the AI's behavior
- Multiple sessions can run concurrently with isolated histories

Example session flow:
1. Start a new chat with a session ID
2. Send messages within the same session to maintain context
3. Retrieve history at any time
4. Clear history to start fresh while keeping the session
5. Use different session IDs for different conversations

Note: Current implementation uses in-memory storage, so histories are cleared on server restart.

## Setup

### Requirements
- Python 3.11 or higher

### Configuration
1. Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials:
```bash
cp .env.example .env
```

2. Update the following variables in `.env`:
```env
# AI Provider (azure, openai, groq)
AI_PROVIDER=azure

# OpenAI API Key (required for all providers)
OPENAI_API_KEY=your_api_key_here

# API Base URL
# For Azure: https://your-resource.openai.azure.com
# For OpenAI: https://api.openai.com/v1
# For Groq: https://api.groq.com/openai/v1
OPENAI_API_BASE=your_api_base_here

# Azure-specific settings (only needed if AI_PROVIDER=azure)
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Model name for non-Azure providers (e.g., gpt-4, llama2-70b-4096)
OPENAI_MODEL_NAME=gpt-4
```

Note: 
- For Azure OpenAI, make sure your deployment is properly set up in your Azure resource
- The API version should match your Azure OpenAI resource's supported version
- The deployment name should match your model deployment in Azure OpenAI
- When using other providers, only `OPENAI_API_KEY`, `OPENAI_API_BASE`, and `OPENAI_MODEL_NAME` are needed

## Running the Application

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn app.main:app --reload --port 8080
```

The API will be available at http://localhost:8080

## Testing the API

You can test the API using curl commands or any HTTP client. Here are some examples:

### Using Postman

A Postman collection is provided for easy testing of all API endpoints:

1. Download [Postman](https://www.postman.com/downloads/)
2. Import the `postman_collection.json` file:
   - Open Postman
   - Click "Import" button
   - Drop the `postman_collection.json` file or browse to select it
   - Click "Import"
3. The collection includes all endpoints with example requests

### 1. Test the Welcome Endpoint
```bash
curl http://localhost:8080/
```
Expected response:
```json
{"Hello": "Welcome to the Chat API"}
```

### 2. Send a Chat Message
```bash
curl -X POST http://localhost:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"messages": [{"role": "user", "content": "Hello, how are you?"}], "session_id": "test1"}'
```
Expected response:
```json
{
    "response": "AI response here..."
}
```

### 3. Get Chat History
```bash
curl http://localhost:8080/chat/history/test1
```
Expected response:
```json
{
    "history": [
        {"role": "system", "content": "..."},
        {"role": "user", "content": "..."},
        {"role": "assistant", "content": "..."}
    ]
}
```

### 4. Clear Chat History
```bash
curl -X DELETE http://localhost:8080/chat/history/test1
```
Expected response:
```json
{
    "message": "History cleared for session test1"
}
```

## API Documentation

### Endpoints

1. `GET /`
   - Welcome endpoint
   - Returns: `{"Hello": "Welcome to the Chat API"}`

2. `POST /chat`
   - Send a message to the chatbot
   - Request body:
     ```json
     {
       "messages": [
         {
           "role": "user",
           "content": "Your message here"
         }
       ],
       "session_id": "unique_session_id"  // Optional, defaults to "default"
     }
     ```
   - Returns: `{"response": "AI's response"}`

3. `GET /chat/history/{session_id}`
   - Get chat history for a specific session
   - Returns:
     ```json
     {
       "history": [
         {"role": "system", "content": "..."},
         {"role": "user", "content": "..."},
         {"role": "assistant", "content": "..."}
       ]
     }
     ```

4. `DELETE /chat/history/{session_id}`
   - Clear chat history for a specific session
   - Returns: `{"message": "History cleared for session {session_id}"}`

### Interactive Documentation

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8080/docs
- Alternative documentation: http://localhost:8080/redoc

## Development

The application uses:
- FastAPI for the web framework
- OpenAI library for Azure OpenAI integration
- Python-dotenv for environment variables
- Uvicorn as the ASGI server

## Contact

For consultation and further development:
- **Developer**: Dody Rachmat Wicaksono
- **Email**: dody@nicecoder.com
- **Website**: nicecoder.com

## License

MIT License

Copyright (c) 2024 Dody Rachmat Wicaksono

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

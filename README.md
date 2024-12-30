# Chatbot API

A FastAPI-based chatbot API that uses Azure OpenAI through LangChain.

## Capabilities

- Stateful chat conversations with Azure OpenAI's GPT models
- Session-based chat history management
- Multiple concurrent chat sessions support
- RESTful API endpoints for chat interactions
- Real-time message processing
- Secure credential management through environment variables
- Easy-to-use API with comprehensive documentation

## Setup

### Requirements
- Python 3.11 or higher

### Configuration
1. Copy `.env.example` to `.env` and fill in your Azure OpenAI credentials:
```bash
cp .env.example .env
```

2. Update the following variables in `.env`:
- AZURE_OPENAI_API_KEY: Your Azure OpenAI API key
- AZURE_OPENAI_API_BASE: Your Azure OpenAI endpoint
- AZURE_OPENAI_API_VERSION: API version (default is 2023-05-15)
- AZURE_OPENAI_DEPLOYMENT_NAME: Your Azure OpenAI deployment name

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

Once the server is running, you can access:
- Interactive API documentation: http://localhost:8080/docs
- Alternative documentation: http://localhost:8080/redoc

## Development

The application uses:
- FastAPI for the web framework
- LangChain for AI model integration
- Azure OpenAI for the language model
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

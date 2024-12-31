# Chat Engine

A powerful chat engine with web search and browsing capabilities.

## Features

- Chat with AI using Azure OpenAI
- Web search functionality using Google Custom Search API
- Web browsing and content extraction
- Real-time exchange rate information
- Clean and structured API responses

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/chatengine.git
cd chatengine
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables in `.env`:
```env
# Azure OpenAI Configuration
AI_PROVIDER=azure
OPENAI_API_KEY=your_api_key
OPENAI_API_BASE=your_api_base
AZURE_OPENAI_API_VERSION=2024-10-21
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Google Custom Search API credentials
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_search_engine_id
```

5. Start the server:
```bash
cd app
uvicorn main:app --reload
```

## API Usage

### Chat Endpoint

`POST /chat`

Send messages to interact with the AI. The chat endpoint now supports:

1. Exchange Rate Queries:
```json
{
    "message": "what is the current exchange rate of 1 USD to IDR?"
}
```

Response:
```json
{
    "status": "success",
    "message": "Current Exchange Rate:\n1 USD = IDR 16,142.17",
    "source": "https://www.xe.com/currencyconverter/convert/?Amount=1&From=USD&To=IDR",
    "timestamp": "Data from XE.com"
}
```

2. Web Browsing:
```json
{
    "message": "browse https://example.com"
}
```

Response:
```json
{
    "status": "success",
    "message": "Title: Example Domain\n\nContent: Example Domain Example Domain This domain is for use in illustrative examples in documents..."
}
```

## Project Structure

```
chatengine/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── agents/
│       ├── __init__.py
│       └── web/
│           ├── __init__.py
│           ├── browser.py
│           ├── search.py
│           └── utils.py
├── requirements.txt
├── README.md
└── chatengine.postman_collection.json
```

## Development

The project uses FastAPI for the backend and includes several agent modules for different functionalities:

- `agents/web/browser.py`: Web browsing and content extraction
- `agents/web/search.py`: Google Custom Search integration
- `agents/web/utils.py`: Common utilities for web operations

## Testing

Test the API using the included Postman collection or curl commands:

```bash
# Test exchange rate query
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "what is the current exchange rate of 1 USD to IDR?"}'

# Test web browsing
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "browse https://example.com"}'
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

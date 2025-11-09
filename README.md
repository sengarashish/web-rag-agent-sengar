#Author: Ashish Sengar
# Web RAG Agent Setup

## Prerequisites
- Python 3.9+
- Google Gemini API key

## Installation

1. Clone the repo and navigate to directory
```bash
cd web-rag-agent-sengar
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Configure settings
- Open `config.properties`
- Add your Gemini API key to `GEMINI_API_KEY`
- Adjust URLs if needed (comma-separated)
- Modify `REQUEST_DELAY` if hitting rate limits

## Running

Start the agent:
```bash
python main.py
```

The app will:
1. Scrape URLs from config (with rate limiting)
2. Build vector index
3. Start interactive console

Type your questions and press Enter. Type 'exit' or 'quit' to stop.

## Troubleshooting

- If you get rate limit errors, increase `REQUEST_DELAY` in config
- Make sure API key is valid
- Check URLs are accessible
- If using free API tier on google, dont use url with lot of content to avoid quota issues.
- Sign up for free gemini api key at: https://aistudio.google.com/api-keys

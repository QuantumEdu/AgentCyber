# AgentCyber - Quick Start Guide

## System Requirements

- Python 3.8 or higher
- Google API Key for Generative AI
- Internet connection

## Installation Steps

### 1. Clone the Repository
```bash
git clone https://github.com/QuantumEdu/AgentCyber.git
cd AgentCyber
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit the `.env` file and add your Google API key:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

To get a Google API key:
1. Go to https://makersuite.google.com/app/apikey
2. Create a new API key
3. Copy the key to your `.env` file

## Running the System

### Option 1: Using the Run Script (Recommended)
```bash
chmod +x run.sh
./run.sh
```

### Option 2: Manual Start
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The server will start on http://localhost:8000

## Accessing the API

### Interactive API Documentation
Once the server is running, open your browser and go to:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Testing the API

#### Using cURL

**1. Check System Health:**
```bash
curl http://localhost:8000/health
```

**2. Security Agent:**
```bash
curl -X POST http://localhost:8000/agent/security \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Suspicious login activity detected from IP 192.168.1.100",
    "context": "Multiple failed attempts on admin account"
  }'
```

**3. Analysis Agent:**
```bash
curl -X POST http://localhost:8000/agent/analysis \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze potential SQL injection attack",
    "context": "Unusual patterns in web server logs"
  }'
```

**4. Response Agent:**
```bash
curl -X POST http://localhost:8000/agent/response \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Create response plan for ransomware detection",
    "context": "Files being encrypted on network share"
  }'
```

**5. Full Multi-Agent Analysis:**
```bash
curl -X POST http://localhost:8000/agent/full-analysis \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Unusual network traffic pattern detected",
    "context": "High volume of outbound connections to unknown IPs"
  }'
```

#### Using Python

```python
import requests

url = "http://localhost:8000/agent/security"
data = {
    "query": "Detect malware activity",
    "context": "Unknown process consuming high CPU"
}

response = requests.post(url, json=data)
print(response.json())
```

## Running Tests

```bash
pytest test_main.py -v
```

Expected output: 7 tests should pass

## Running the Example Script

```bash
python example.py
```

This will demonstrate all three agents working together on a sample security scenario.

## Project Structure

```
AgentCyber/
├── app/                    # Main application package
│   ├── agents/            # Agent implementations
│   │   ├── base_agent.py      # Base agent class
│   │   ├── security_agent.py  # Security monitoring agent
│   │   ├── analysis_agent.py  # Threat analysis agent
│   │   └── response_agent.py  # Incident response agent
│   ├── models/            # Data models
│   │   └── schemas.py         # Pydantic models
│   ├── utils/             # Utilities
│   │   └── config.py          # Configuration
│   └── main.py            # FastAPI application
├── test_main.py           # Test suite
├── example.py             # Usage example
├── run.sh                 # Server startup script
├── requirements.txt       # Python dependencies
├── README.md             # Main documentation
├── ARCHITECTURE.md       # Architecture details
└── QUICKSTART.md         # This file
```

## API Endpoints Summary

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | System information |
| GET | `/health` | Health check |
| POST | `/agent/security` | Security monitoring |
| POST | `/agent/analysis` | Threat analysis |
| POST | `/agent/response` | Incident response |
| POST | `/agent/full-analysis` | Complete multi-agent analysis |

## Common Use Cases

### 1. Analyze Suspicious Login Activity
```json
{
  "query": "Multiple failed login attempts from IP 10.0.0.50",
  "context": "Target account: administrator, Time: 02:00 AM"
}
```

### 2. Investigate Malware Detection
```json
{
  "query": "Antivirus detected potential malware in system32",
  "context": "File: suspicious.exe, Hash: abc123..."
}
```

### 3. Response to DDoS Attack
```json
{
  "query": "DDoS attack detected on web server",
  "context": "Traffic spike from multiple IPs, 1000+ req/sec"
}
```

## Troubleshooting

### Error: "Google API key not configured"
- Make sure you created a `.env` file
- Verify the API key is correctly set in `.env`
- Restart the server after updating `.env`

### Import Errors
- Ensure you're in the virtual environment
- Run `pip install -r requirements.txt` again

### Port Already in Use
- Change the port in the uvicorn command:
  ```bash
  uvicorn app.main:app --reload --port 8001
  ```

## Security Notes

- Never commit your `.env` file or API keys to version control
- The `.env` file is in `.gitignore` by default
- Use environment variables in production environments
- Implement rate limiting in production
- Use HTTPS in production deployments

## Next Steps

1. Explore the API documentation at `/docs`
2. Try different security scenarios
3. Integrate with your existing security tools
4. Customize agent prompts for your specific needs
5. Add logging and monitoring

## Support

For issues or questions:
- Check the ARCHITECTURE.md for system details
- Review the README.md for comprehensive documentation
- Open an issue on GitHub

---

**AgentCyber** - Multi-Agent Cybersecurity System
Version 1.0.0

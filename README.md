# Python Code Executor API

## Quick Start

### Live Demo
**Service URL:** https://python-code-executor-oz6xf3fctq-uc.a.run.app

### Local Development
```bash
# Clone the repository
git clone <your-repo-url>
cd python-code-executor

# Build and run locally
docker build -t python-code-executor .
docker run -p 8080:8080 python-code-executor

# Test the API
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello World!\"}"}'
```

### Deploy to Google Cloud Run
```bash
# Make deploy script executable
chmod +x deploy.sh

# Deploy (replace with your project ID)
./deploy.sh your-project-id us-central1
```

## Repository Structure

```
python-code-executor/
├── app/                    # Main application code
│   ├── __init__.py
│   ├── main.py            # Flask application
│   ├── executor.py        # Script execution with nsjail
│   └── validator.py       # Input validation
├── Dockerfile             # Container definition
├── requirements.txt       # Python dependencies
├── README.md             # Documentation
├── IMPLEMENTATION_SUMMARY.md  # Implementation details
├── deploy.sh             # Deployment script
├── test_script.py        # Test suite
├── cloudbuild.yaml       # Cloud Build configuration
├── .dockerignore         # Docker optimization
└── .gitignore           # Git ignore rules
```

## Key Features

- **nsjail Security**: Google's security sandbox for code execution
- **Flask API**: RESTful API with JSON responses
- **Docker Ready**: Lightweight container with Python 3.11
- **Cloud Run Deployed**: Live demo available
- **Comprehensive Testing**: Full test suite included
- **Production Ready**: Gunicorn WSGI server

## Requirements Met

- Lightweight Docker image
- Single `docker run` command
- Comprehensive README with cURL examples
- Basic input validation
- Safe execution with nsjail
- Access to basic libraries (pandas, numpy, etc.)
- Flask + nsjail implementation
- Deployed on Google Cloud Run

## Testing

```bash
# Test local instance
python test_script.py

# Test Cloud Run instance
python test_script.py https://python-code-executor-oz6xf3fctq-uc.a.run.app
```

## Documentation

- **README.md**: Complete setup and usage guide
- **IMPLEMENTATION_SUMMARY.md**: Technical implementation details
- **test_script.py**: Comprehensive test examples

## Security

- nsjail sandboxing for code execution
- Input validation and security checks
- Non-root container execution
- Timeout protection (10 seconds)
- Process isolation

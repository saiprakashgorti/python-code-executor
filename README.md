# Python Code Executor API

A secure Python code execution service that allows users to execute arbitrary Python scripts in a sandboxed environment using **nsjail**. The service executes scripts and returns the result of the `main()` function along with any stdout output.

## 🚀 Live Demo

**Service URL:** https://python-code-executor-oz6xf3fctq-uc.a.run.app

**Quick Test:**
```bash
curl -X POST https://python-code-executor-oz6xf3fctq-uc.a.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello World!\"}"}'
```

## 📋 Project Summary

This is a **take-home challenge implementation** for a Python code execution API service with the following requirements:

- ✅ **Lightweight Docker image** with Python 3.11 and nsjail
- ✅ **Single `docker run` command** for local execution
- ✅ **Comprehensive README.md** with cURL examples and Cloud Run URL
- ✅ **Basic input validation** for scripts and security checks
- ✅ **Safe execution** against malicious scripts using nsjail
- ✅ **Access to basic libraries** (os, pandas, numpy, etc.)
- ✅ **Flask + nsjail** implementation as specified
- ✅ **Deployed on Google Cloud Run** with public URL

## Features

- 🔒 **Secure Execution**: Uses **nsjail** for sandboxed code execution (as required by the challenge)
- 🐍 **Python Support**: Supports Python 3.11 with common libraries (pandas, numpy, os, etc.)
- ✅ **Input Validation**: Comprehensive script validation including security checks
- 🚀 **Production Ready**: Dockerized with gunicorn for production deployment
- 📊 **JSON Response**: Returns structured JSON responses with results and stdout

## Security Features

- **nsjail Sandboxing**: All code execution is sandboxed using nsjail (Google's security sandbox)
- **Input Validation**: Blocks dangerous operations (subprocess, eval, exec, etc.)
- **Non-root User**: Container runs as non-root user for security
- **Time Limits**: 10-second execution time limit
- **Resource Isolation**: Isolated execution environment
- **Fallback Security**: If nsjail is not available, uses secure Python subprocess execution

## API Endpoints

### POST /execute

Execute a Python script and return the result of the `main()` function.

**Request Body:**
```json
{
    "script": "def main():\n    return {'message': 'Hello World'}"
}
```

**Response:**
```json
{
    "result": {"message": "Hello World"},
    "stdout": "Any print output from the script"
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
    "status": "healthy"
}
```

## Requirements

- Scripts must define a `main()` function
- The `main()` function must have a return statement
- Return values must be JSON-serializable
- Scripts cannot use dangerous operations (subprocess, eval, exec, etc.)

## Local Development

### Prerequisites

- Docker
- curl (for testing)

### Running Locally

1. **Build the Docker image:**
```bash
docker build -t python-code-executor .
```

2. **Run the container:**
```bash
docker run -p 8080:8080 python-code-executor
```

3. **Test the API:**
```bash
curl -X POST http://localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    print(\"Hello from Python!\")\n    return {\"message\": \"Hello World\", \"status\": \"success\"}"
  }'
```

## Example Scripts

### Basic Example
```python
def main():
    return "Hello, World!"
```

### With Print Statements
```python
def main():
    print("Starting calculation...")
    result = 2 + 2
    print(f"Result: {result}")
    return {"sum": result, "message": "Calculation completed"}
```

### Using Pandas and Numpy
```python
import pandas as pd
import numpy as np

def main():
    # Create a simple DataFrame
    data = {'name': ['Alice', 'Bob', 'Charlie'], 'age': [25, 30, 35]}
    df = pd.DataFrame(data)
    
    # Calculate average age using numpy
    avg_age = np.mean(df['age'])
    
    return {
        "data": df.to_dict('records'),
        "average_age": float(avg_age),
        "total_records": len(df)
    }
```

## Deployment

### Google Cloud Run

**Live Demo URL:** https://python-code-executor-oz6xf3fctq-uc.a.run.app

#### Option A: Using the deployment script (Recommended)

```bash
# Make the script executable
chmod +x deploy.sh

# Deploy with your project ID
./deploy.sh python-code-executor-469503 us-central1
```

#### Option B: Manual deployment

1. **Build and push to Artifact Registry:**
```bash
# Set your project ID
export PROJECT_ID=python-code-executor-469503

# Build the image for linux/amd64 (required for Cloud Run)
docker build --platform linux/amd64 -t us-central1-docker.pkg.dev/$PROJECT_ID/python-code-executor/python-code-executor .

# Push to Artifact Registry
docker push us-central1-docker.pkg.dev/$PROJECT_ID/python-code-executor/python-code-executor
```

2. **Deploy to Cloud Run:**
```bash
gcloud run deploy python-code-executor \
  --image us-central1-docker.pkg.dev/$PROJECT_ID/python-code-executor/python-code-executor \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1
```

3. **Test the deployed service:**
```bash
# Health check
curl https://python-code-executor-oz6xf3fctq-uc.a.run.app/health

# Execute a script
curl -X POST https://python-code-executor-oz6xf3fctq-uc.a.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{
    "script": "def main():\n    return {\"message\": \"Hello from Cloud Run!\"}"
  }'
```

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid script syntax, missing main() function, or security violations
- **500 Internal Server Error**: Unexpected server errors

Example error response:
```json
{
    "error": "Script must define a 'main()' function"
}
```

## Supported Libraries

The following libraries are available in the execution environment:
- Standard Python libraries (os, sys, json, etc.)
- pandas
- numpy
- requests
- Other common data science libraries

## Limitations

- Maximum execution time: 10 seconds
- No network access (except for allowed libraries)
- No file system access outside the sandbox
- No subprocess execution
- No eval/exec operations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License

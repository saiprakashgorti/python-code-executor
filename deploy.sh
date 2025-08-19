#!/bin/bash

# Deployment script for Python Code Executor API
# Usage: ./deploy.sh [PROJECT_ID] [REGION]
# Example: ./deploy.sh python-code-executor-469503 us-central1

set -e

# Default values
PROJECT_ID=${1:-"python-code-executor-469503"}
REGION=${2:-"us-central1"}
SERVICE_NAME="python-code-executor"

echo "🚀 Deploying Python Code Executor API to Google Cloud Run"
echo "Project ID: $PROJECT_ID"
echo "Region: $REGION"
echo "Service Name: $SERVICE_NAME"
echo ""

# Check if project ID is set
if [ "$PROJECT_ID" = "your-project-id" ]; then
    echo "❌ Error: Please provide your project ID"
    echo "Usage: ./deploy.sh YOUR_PROJECT_ID [REGION]"
    echo ""
    echo "To find your project ID, run:"
    echo "  gcloud projects list"
    echo "  gcloud config get-value project"
    echo ""
    echo "Example:"
    echo "  ./deploy.sh python-code-executor-469503 us-central1"
    exit 1
fi

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Error: gcloud CLI is not installed. Please install it first:"
    echo "  https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed. Please install it first."
    exit 1
fi

# Set the project
echo "🔧 Setting project to: $PROJECT_ID"
gcloud config set project $PROJECT_ID

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Configure Docker for Artifact Registry
echo "🔧 Configuring Docker for Artifact Registry..."
gcloud auth configure-docker $REGION-docker.pkg.dev

echo "📦 Building Docker image for linux/amd64..."
docker build --platform linux/amd64 -t $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME .

echo "📤 Pushing to Artifact Registry..."
docker push $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image $REGION-docker.pkg.dev/$PROJECT_ID/$SERVICE_NAME/$SERVICE_NAME \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 1Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🌐 Your service URL:"
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")
echo $SERVICE_URL

echo ""
echo "🧪 Test your service:"
echo "curl -X POST $SERVICE_URL/execute \\"
echo "  -H \"Content-Type: application/json\" \\"
echo "  -d '{\"script\": \"def main():\\n    return {\\\"message\\\": \\\"Hello from Cloud Run!\\\"}\"}'"
echo ""
echo "🏥 Health check:"
echo "curl $SERVICE_URL/health"

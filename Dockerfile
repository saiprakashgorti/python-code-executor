FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Try to install nsjail, but don't fail if it's not available
RUN wget -O /tmp/nsjail.tar.gz https://github.com/google/nsjail/releases/download/2.9/nsjail_2.9_amd64.tar.gz || \
    wget -O /tmp/nsjail.tar.gz https://github.com/google/nsjail/releases/download/2.8/nsjail_2.8_amd64.tar.gz || \
    echo "nsjail not available, will use secure Python execution" && \
    (tar -xzf /tmp/nsjail.tar.gz -C /tmp && mv /tmp/nsjail /usr/local/bin/ && chmod +x /usr/local/bin/nsjail && rm /tmp/nsjail.tar.gz) || \
    echo "nsjail installation failed, using secure Python execution"

# Create nsjail configuration directory
RUN mkdir -p /etc/nsjail

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

# Create app directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ app/

# Change ownership to app user
RUN chown -R app:app /app

# Switch to non-root user
USER app

# Expose port
EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "30", "app.main:app"]
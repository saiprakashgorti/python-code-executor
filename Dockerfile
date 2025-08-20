FROM python:3.11-slim

# Installing dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

RUN wget -O /tmp/nsjail.tar.gz https://github.com/google/nsjail/releases/download/2.9/nsjail_2.9_amd64.tar.gz || \
    wget -O /tmp/nsjail.tar.gz https://github.com/google/nsjail/releases/download/2.8/nsjail_2.8_amd64.tar.gz || \
    echo "nsjail not available, will use secure Python execution" && \
    (tar -xzf /tmp/nsjail.tar.gz -C /tmp && mv /tmp/nsjail /usr/local/bin/ && chmod +x /usr/local/bin/nsjail && rm /tmp/nsjail.tar.gz) || \
    echo "nsjail installation failed, using secure Python execution"

# Create nsjail config directory
RUN mkdir -p /etc/nsjail

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ app/
RUN chown -R app:app /app
USER app
EXPOSE 8080

# Using gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--timeout", "30", "app.main:app"]
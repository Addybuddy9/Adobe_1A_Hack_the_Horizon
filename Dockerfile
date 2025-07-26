# Adobe Hackathon 2025 - Challenge 1a: PDF Outline Extraction
FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies with optimizations
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py ./
COPY config.json ./

# Create input and output directories
RUN mkdir -p /app/input /app/output /app/cache

# Set permissions
RUN chmod +x main.py

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Default command
CMD ["python", "main.py"]

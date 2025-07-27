# Adobe Hackathon 2025 - Challenge 1a: PDF Outline Extraction
FROM --platform=linux/amd64 python:3.13-slim

WORKDIR /app

# Install minimal system dependencies for PyMuPDF
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Copy and install Python dependencies (now just PyMuPDF)
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY main.py ./
COPY config.json ./

# Create input and output directories with proper permissions
RUN mkdir -p /app/input /app/output /app/cache && \
    chmod 755 /app/input /app/output /app/cache

# Set executable permissions
RUN chmod +x main.py

# Add non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser && \
    chown -R appuser:appuser /app
USER appuser

# Health check - simplified for single dependency
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import fitz; import sys; sys.exit(0)"

# Environment variables for optimization
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random

# Default command
CMD ["python", "main.py"]

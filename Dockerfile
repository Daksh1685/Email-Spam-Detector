# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p flask_session

# Expose port
EXPOSE 8080

# Set environment variables
ENV FLASK_APP=app.py
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Run the Flask app
CMD ["python", "app.py"]

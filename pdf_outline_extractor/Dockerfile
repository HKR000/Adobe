# Base image with explicit AMD64 architecture
FROM --platform=linux/amd64 python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all source code into the container
COPY . .

# Install system-level dependencies (for some fonts/pdf support)
RUN apt-get update && apt-get install -y \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Pre-download the SentenceTransformer model during build (offline runtime compliance)
RUN python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-MiniLM-L6-v2')"

# Set the default command to run Round 1B (can override to run 1A)
CMD ["python3", "main.py", "1b"]


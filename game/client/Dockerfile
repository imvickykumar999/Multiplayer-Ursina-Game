# Use official Python image with minimal footprint
FROM python:3.10-slim

# Metadata
LABEL maintainer="imvickykumar999"

# Set working directory inside container
WORKDIR /usr/src/app

# Install system dependencies required for Ursina and GUI support,
# general build tools for Python packages with C extensions,
# and Tkinter runtime libraries.
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libxrender1 \
    libxrandr2 \
    libxcursor1 \
    libxi6 \
    libxcomposite1 \
    libasound2 \
    libpulse0 \
    ffmpeg \
    build-essential \
    python3-dev \
    python3-tk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements first (for Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the game files
COPY . .

# Run the game
CMD ["python", "main.py"]

# Use an official Python image with system package support
FROM python:3.10-slim

# Install system dependencies (including xvfb, xauth, and x11-utils)
RUN apt-get update && apt-get install -y xvfb x11-utils xauth && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /app

# Copy game files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the game using a virtual display
CMD ["xvfb-run", "python", "main.py"]

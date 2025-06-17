# Base Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install ffmpeg for video/audio processing
RUN apt-get update && apt-get install -y ffmpeg

# Copy backend code
COPY backend/ ./backend

# Expose Flask port
EXPOSE 5000

# Run Flask app
CMD ["python", "backend/app.py"]

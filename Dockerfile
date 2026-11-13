FROM python:3.10-slim

# Install system dependencies (ffmpeg is required for yt-dlp audio extraction)
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python dependencies
RUN pip install --no-cache-dir flask flask-cors yt-dlp ffmpeg-python gunicorn

COPY . .

EXPOSE 5000

CMD gunicorn --bind 0.0.0.0:$PORT main:app

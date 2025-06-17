FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --no-cache-dir -r backend/requirements.txt

EXPOSE 10000

CMD ["python", "backend/app.py"]

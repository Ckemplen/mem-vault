FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg imagemagick build-essential libpq-dev && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONUNBUFFERED=1 PORT=8000 DJANGO_SETTINGS_MODULE=config.settings
CMD ["gunicorn","config.asgi:application","-k","uvicorn.workers.UvicornWorker","-b","0.0.0.0:8000","--workers","3","--timeout","120"]

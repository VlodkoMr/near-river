FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    cmake  \
    build-essential  \
    pkg-config  \
    libgoogle-perftools-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

RUN chmod +x ./scripts/start_api.sh

# Run app.py when the container launches
CMD ["sh", "-c", "./scripts/start_api.sh"]

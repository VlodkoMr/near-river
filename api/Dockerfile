FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    cmake \
    build-essential \
    pkg-config \
    libgoogle-perftools-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt requirements.txt
COPY scripts/start_api.sh scripts/start_api.sh

RUN pip install torch --index-url https://download.pytorch.org/whl/cu124
RUN pip install -r requirements.txt

EXPOSE 3000

RUN chmod +x ./scripts/start_api.sh

# Run app.py when the container launches
CMD ["sh", "-c", "./scripts/start_api.sh"]

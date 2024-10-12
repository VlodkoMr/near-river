FROM nvidia/cuda:12.6.1-cudnn-runtime-ubuntu24.04

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    cmake \
    build-essential \
    pkg-config \
    libgoogle-perftools-dev \
    gfortran \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /venv
RUN python3 -m venv venv

WORKDIR /app
ENV PATH="/venv/venv/bin:$PATH"

COPY requirements.txt requirements.txt
COPY scripts/ scripts/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

EXPOSE 3000

RUN chmod +x ./scripts/start_api.sh

# Run app.py when the container launches
CMD ["sh", "-c", "./scripts/start_api.sh"]

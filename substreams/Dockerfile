FROM rust:1.72-slim

# Install necessary tools
RUN apt-get update && apt-get install -y \
    curl \
    ca-certificates \
    build-essential \
    make \
    jq \
    && rm -rf /var/lib/apt/lists/*

# Install buf CLI for protobuf generation
RUN curl -sSL "https://github.com/bufbuild/buf/releases/download/v1.19.0/buf-Linux-x86_64" -o /usr/local/bin/buf && \
    chmod +x /usr/local/bin/buf

# Install substreams and substreams-sink-sql for x86_64 architecture
RUN curl -L https://github.com/streamingfast/substreams/releases/download/v1.10.6/substreams_linux_x86_64.tar.gz | tar -xz -C /usr/local/bin
RUN curl -L https://github.com/streamingfast/substreams-sink-sql/releases/download/v4.2.1/substreams-sink-sql_linux_x86_64.tar.gz | tar -xz -C /usr/local/bin

RUN rustup target add wasm32-unknown-unknown

WORKDIR /app
COPY . .

RUN chmod +x ./scripts/start_substreams.sh

CMD ["sh", "-c", "./scripts/start_substreams.sh"]
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create workspace directory and set permissions
RUN mkdir -p /workspace && chmod 777 /workspace

# Create a non-root user
RUN useradd -ms /bin/bash vscode && \
    chown -R vscode:vscode /workspace

# Set working directory
WORKDIR /workspace

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set Python path
ENV PYTHONPATH=/workspace

# Switch to non-root user
USER vscode 
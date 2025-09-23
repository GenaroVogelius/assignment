# Use Python 3.13 slim image
FROM python:3.13-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Create workspace directory
WORKDIR /workspace

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen --no-dev

# Copy application code
COPY . .

# Set Python path
ENV PYTHONPATH=/workspace

# Create non-root user
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /workspace


# Create log file and set permissions
RUN touch /workspace/app.log && chown appuser:appuser /workspace/app.log

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000


# Run the application
CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 
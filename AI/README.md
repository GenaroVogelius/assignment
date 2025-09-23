# AI Microservice

## Description

This microservice is a backend API developed with FastAPI that implements Clean Architecture. The system receives user input and processes actions through a manager agent.

## Features

- **FastAPI**: Modern and fast web framework for APIs
- **Clean Architecture**: Clear separation of responsibilities between layers
- **Dev Container**: Complete configuration for local development
- **Testing**: Automated test suite

## Project Structure

```
app/
├── core/           # Entities and business rules
├── use_cases/      # Use cases for different scenarios
├── interfaces/     # Abstraction layer for objects
├── infrastructure/ # Concrete implementations of methods
└── config/         # General application configuration
```

## Local Development

### Prerequisites

- Docker
- Docker Compose
- VS Code with Dev Containers extension (recommended)

### Dev Container Setup

1. Clone the repository
2. Open the project in VS Code
3. When the notification appears, click "Reopen in Container"
4. Or manually: `Ctrl+Shift+P` → "Dev Containers: Reopen in Container"

The dev container includes all necessary dependencies and environment configurations.

### Running the Application

#### Option 1: Using Docker Compose (Recommended)

```bash
# From the AI directory
docker-compose -f .devcontainer/docker-compose.local.yml up --build
```

This will start the application with MongoDB database. The API will be available at `http://localhost:8000`

#### Option 2: Inside the Dev Container

```bash
# Inside the dev container
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## Environment Variables

The application uses environment variables for configuration. Create a `.env` file in the `AI` directory with the following variables:

### Required Variables

| Variable          | Description                 | Example                          |
| ----------------- | --------------------------- | -------------------------------- |
| `AI_PROVIDER`     | AI provider name            | `groq`                           |
| `AI_MODEL`        | AI model name               | `meta-llama/llama-4-scout-17b-16e-instruct`       |
| `OPENAI_API_KEY`  | API key for the AI provider | `gsk_...`                        |
| `OPENAI_BASE_URL` | Base URL for the AI API     | `https://api.groq.com/openai/v1` |

### Optional Variables

#### Application Settings

| Variable        | Description          | Default |
| --------------- | -------------------- | ------- |
| `DEBUG`         | Enable debug mode    | `True`  |
| `ALLOW_ORIGINS` | CORS allowed origins | `*`     |
| `API_PREFIX`    | API route prefix     | `/api`  |

#### Database Configuration

| Variable           | Description                        | Default                                                                 |
| ------------------ | ---------------------------------- | ----------------------------------------------------------------------- |
| `DATABASE_TYPE`    | Database type (mongodb/postgresql) | `mongodb`                                                               |
| `DATABASE_URL`     | MongoDB connection URL             | `mongodb://admin:password123@mongodb:27017/ai_service?authSource=admin` |
| `MONGODB_DATABASE` | MongoDB database name              | `ai_service`                                                            |
| `POSTGRESQL_URL`   | PostgreSQL connection URL          | ``                                                                      |

#### Authentication

| Variable         | Description       | Default                                     |
| ---------------- | ----------------- | ------------------------------------------- |
| `SECRET_KEY`     | JWT secret key    | `your-secret-key-change-this-in-production` |
| `HASH_ALGORITHM` | Hashing algorithm | `HS256`                                     |

#### AI Model Configuration

| Variable               | Description                        | Default                    |
| ---------------------- | ---------------------------------- | -------------------------- |
| `TEMPERATURE`          | AI model temperature               | `0.7`                      |
| `TIMEOUT`              | Request timeout in seconds         | `30`                       |
| `MAX_TOKENS`           | Maximum tokens per response        | `1000`                     |
| `PRESENCE_PENALTY`     | Presence penalty for AI responses  | `0.1`                      |
| `FREQUENCY_PENALTY`    | Frequency penalty for AI responses | `0.1`                      |
| `EXPERT_REVIEW_PROMPT` | Custom expert review prompt        | Uses default system prompt |

### Example .env File

```env
# Required AI Configuration
AI_PROVIDER=groq
AI_MODEL=/llama-3.1-70b-versatile
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://api.groq.com/openai/v1

# Optional Configuration
DEBUG=True
DATABASE_TYPE=mongodb
SECRET_KEY=your-secure-secret-key-here
TEMPERATURE=0.7
MAX_TOKENS=1000
```

## Testing

**Important**: Tests must be run inside the dev container.

```bash
# Inside the dev container
uv run pytest
```

To run tests with more detail:

```bash
uv run pytest -v
```

To run specific tests:

```bash
uv run pytest tests/test_auth_registration.py
```

## API Documentation

Once the application is running, you can access:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

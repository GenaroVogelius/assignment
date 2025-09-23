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
```bash
# Inside the dev container
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

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

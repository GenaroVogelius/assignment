from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

from app.config.settings import Settings
from app.infrastructure.api.auth_routes import AuthRoutes
from app.infrastructure.api.main_routes import MainRoutes
from app.infrastructure.db.main import close_database_connection, initialize_database
from app.infrastructure.dependencies import limiter
from app.infrastructure.logger import logger

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        # Initialize database connection using the centralized database module
        await initialize_database()

        main_routes = MainRoutes()
        app.include_router(
            main_routes.router, prefix=settings.API_PREFIX, tags=["api rest"]
        )

        auth_routes = AuthRoutes()
        app.include_router(
            auth_routes.router, prefix=settings.API_PREFIX, tags=["auth"]
        )

        logger.info("Aplicación iniciada correctamente")
        logger.info("API disponible en: http://localhost:8000")
        logger.info("Documentación disponible en: http://localhost:8000/docs")
        logger.info("Autenticación disponible en: http://localhost:8000/api/v1/auth")
    except Exception as e:
        logger.error(f"Error en startup: {str(e)}")
        raise

    yield

    # Shutdown
    try:
        await close_database_connection()
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    debug=settings.DEBUG,
    description="AI Service with database integration",
    lifespan=lifespan,
)


# Add rate limiter to the app
app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    lambda request, exc: JSONResponse(
        status_code=429, content={"error": "Rate limit exceeded", "status_code": 429}
    ),
)

# Configuración de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOW_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Manejo global de errores
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500, content={"error": "Internal server error", "status_code": 500}
    )

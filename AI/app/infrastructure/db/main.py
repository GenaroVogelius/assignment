"""
Database initialization module.
This module provides database-agnostic initialization functions.
"""

from app.config.settings import Settings
from app.infrastructure.factories.repository_factory import DatabaseType
from app.infrastructure.logger import logger


settings = Settings()

async def initialize_database():
    """
    Initialize database connection based on configuration.
    This function is database-agnostic and will use the configured database type.
    """
    try:
        db_type = DatabaseType(settings.DATABASE_TYPE.lower())

        if db_type == DatabaseType.MONGODB:
            from app.infrastructure.db.mongo.database import connect_to_mongo

            await connect_to_mongo()
            logger.info("MongoDB connection established")

        elif db_type == DatabaseType.POSTGRESQL:
            # TODO: Implement PostgreSQL connection
            logger.info("PostgreSQL connection not yet implemented")
            raise NotImplementedError("PostgreSQL connection not yet implemented")

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise


async def close_database_connection():
    """
    Close database connection based on configuration.
    This function is database-agnostic and will use the configured database type.
    """
    try:
        db_type = DatabaseType(settings.DATABASE_TYPE.lower())

        if db_type == DatabaseType.MONGODB:
            from app.infrastructure.db.mongo.database import close_mongo_connection

            await close_mongo_connection()
            logger.info("MongoDB connection closed")

        elif db_type == DatabaseType.POSTGRESQL:
            # TODO: Implement PostgreSQL connection closing
            logger.info("PostgreSQL connection closing not yet implemented")

        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    except Exception as e:
        logger.error(f"Error closing database connection: {str(e)}")
        raise

from typing import Optional

from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ServerSelectionTimeoutError

from app.config.settings import Settings
from app.infrastructure.db.mongo.models import BlackListToken, User, Review


settings = Settings()

class Database:
    client: Optional[AsyncIOMotorClient] = None
    database = None


# Global database instance
db = Database()


async def connect_to_mongo():
    """Create database connection"""
    try:
        # Create MongoDB client
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            serverSelectionTimeoutMS=5000,  # 5 second timeout
            connectTimeoutMS=5000,
            socketTimeoutMS=5000,
        )

        # Test the connection
        await db.client.admin.command("ping")
        print(f"✅ Connected to MongoDB at {settings.MONGODB_URL}")

        # Get database
        db.database = db.client[settings.MONGODB_DATABASE]

        # Initialize Beanie with document models
        await init_beanie(
            database=db.database, document_models=[User, BlackListToken, Review]
        )

        print(f"✅ Beanie initialized for database: {settings.MONGODB_DATABASE}")

    except ServerSelectionTimeoutError:
        print("❌ Failed to connect to MongoDB: Server selection timeout")
        raise
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection"""
    if db.client:
        db.client.close()
        print("✅ MongoDB connection closed")


async def get_database():
    """Get database instance"""
    if db.database is None:
        await connect_to_mongo()
    return db.database


async def get_client():
    """Get MongoDB client instance"""
    if db.client is None:
        await connect_to_mongo()
    return db.client


# Health check function
async def check_mongo_health() -> bool:
    """Check if MongoDB connection is healthy"""
    try:
        if db.client is None:
            return False
        await db.client.admin.command("ping")
        return True
    except Exception:
        return False

from typing import Optional, Type

from app.config.settings import Settings
from app.core.enums import DatabaseType
from app.interfaces.repositories.review_repository_interface import (
    ReviewRepositoryInterface,
)
from app.interfaces.repositories.user_repository_interface import (
    UserRepositoryInterface,
)


class RepositoryFactory:
    """Factory for creating repository instances based on database type"""

    _user_repositories: dict[DatabaseType, Type[UserRepositoryInterface]] = {}
    _review_repositories: dict[DatabaseType, Type[ReviewRepositoryInterface]] = {}

    @classmethod
    def register_user_repository(
        cls, db_type: DatabaseType, repository_class: Type[UserRepositoryInterface]
    ) -> None:
        """Register a user repository implementation for a specific database type"""
        cls._user_repositories[db_type] = repository_class

    @classmethod
    def register_review_repository(
        cls, db_type: DatabaseType, repository_class: Type[ReviewRepositoryInterface]
    ) -> None:
        """Register a review repository implementation for a specific database type"""
        cls._review_repositories[db_type] = repository_class

    @classmethod
    def create_user_repository(
        cls, db_type: Optional[DatabaseType] = None
    ) -> UserRepositoryInterface:
        """
        Create a user repository instance based on the database type

        Args:
            db_type: Database type to use. If None, will use the configured database type

        Returns:
            UserRepositoryInterface: Repository instance

        Raises:
            ValueError: If the database type is not supported or not registered
        """
        if db_type is None:
            db_type = cls._get_database_type_from_config()

        if db_type not in cls._user_repositories:
            raise ValueError(
                f"No user repository implementation registered for database type: {db_type.value}"
            )

        repository_class = cls._user_repositories[db_type]
        return repository_class()

    @classmethod
    def create_review_repository(
        cls, db_type: Optional[DatabaseType] = None
    ) -> ReviewRepositoryInterface:
        """
        Create a review repository instance based on the database type

        Args:
            db_type: Database type to use. If None, will use the configured database type

        Returns:
            ReviewRepositoryInterface: Repository instance

        Raises:
            ValueError: If the database type is not supported or not registered
        """
        if db_type is None:
            db_type = cls._get_database_type_from_config()

        if db_type not in cls._review_repositories:
            raise ValueError(
                f"No review repository implementation registered for database type: {db_type.value}"
            )

        repository_class = cls._review_repositories[db_type]
        return repository_class()

    @classmethod
    def _get_database_type_from_config(cls) -> DatabaseType:
        """Get database type from configuration"""
        # Get database type from settings
        settings = Settings()
        db_type_str = settings.DATABASE_TYPE.lower()

        try:
            return DatabaseType(db_type_str)
        except ValueError:
            # Fallback to checking URLs if DATABASE_TYPE is not valid
            if settings.MONGODB_URL:
                return DatabaseType.MONGODB
            elif settings.POSTGRESQL_URL or (
                settings.POSTGRESQL_URL and "postgresql" in settings.POSTGRESQL_URL
            ):
                return DatabaseType.POSTGRESQL
            else:
                # Default to MongoDB
                return DatabaseType.MONGODB

    @classmethod
    def get_supported_database_types(cls) -> list[DatabaseType]:
        """Get list of supported database types"""
        return list(DatabaseType)

    @classmethod
    def is_database_type_supported(cls, db_type: DatabaseType) -> bool:
        """Check if a database type is supported"""
        return db_type in cls._user_repositories


# Auto-register MongoDB repositories if available
try:
    from app.infrastructure.db.mongo.mongo_repository import (
        MongoReviewRepository,
        MongoUserRepository,
    )

    RepositoryFactory.register_user_repository(
        DatabaseType.MONGODB, MongoUserRepository
    )
    RepositoryFactory.register_review_repository(
        DatabaseType.MONGODB, MongoReviewRepository
    )
except ImportError:
    pass


# # Auto-register PostgreSQL repository if available
# try:
#     from app.infrastructure.repositories.postgres_user_repository import (
#         PostgresUserRepository,
#     )

#     RepositoryFactory.register_repository(
#         DatabaseType.POSTGRESQL, PostgresUserRepository
#     )
# except ImportError:
#     pass

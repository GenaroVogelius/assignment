# Repository Factory Pattern

Este módulo implementa el patrón Factory para crear instancias de repositorios de manera dinámica basándose en la configuración de la base de datos.

## Características

- **Flexibilidad**: Permite cambiar entre diferentes tipos de base de datos sin modificar el código de negocio
- **Configuración**: Se basa en variables de entorno para determinar qué repositorio usar
- **Extensibilidad**: Fácil agregar nuevos tipos de base de datos
- **Auto-registro**: Los repositorios se registran automáticamente si están disponibles

## Tipos de Base de Datos Soportados

- **MongoDB**: Implementación usando Motor/Beanie
- **PostgreSQL**: Implementación usando asyncpg
- **SQLite**: Implementación usando aiosqlite (ejemplo)

## Configuración

### Variables de Entorno

```bash
# Tipo de base de datos a usar
DATABASE_TYPE=mongodb  # opciones: mongodb, postgresql, sqlite

# URLs de conexión (opcional, se usan como fallback)
MONGODB_URL=mongodb://user:password@localhost:27017/database
POSTGRESQL_URL=postgresql://user:password@localhost:5432/database
```

### Uso en el Código

```python
from app.infrastructure.factories.repository_factory import RepositoryFactory, DatabaseType

# Crear repositorio usando la configuración por defecto
user_repo = RepositoryFactory.create_user_repository()

# Crear repositorio específico
user_repo = RepositoryFactory.create_user_repository(DatabaseType.POSTGRESQL)
```

## Agregar un Nuevo Tipo de Base de Datos

1. **Crear la implementación del repositorio**:
```python
# app/infrastructure/repositories/mysql_user_repository.py
class MySQLUserRepository(UserRepositoryInterface):
    # Implementar todos los métodos de la interfaz
    pass
```

2. **Registrar en el factory**:
```python
# En repository_factory.py
from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository

# Agregar al enum
class DatabaseType(Enum):
    MYSQL = "mysql"

# Auto-registrar
try:
    from app.infrastructure.repositories.mysql_user_repository import MySQLUserRepository
    RepositoryFactory.register_repository(DatabaseType.MYSQL, MySQLUserRepository)
except ImportError:
    pass
```

3. **Actualizar la configuración**:
```python
# En settings.py
DATABASE_TYPE: str = os.getenv("DATABASE_TYPE", "mongodb")  # Agregar mysql a las opciones
```

## Beneficios

1. **Separación de Responsabilidades**: El código de negocio no depende de implementaciones específicas
2. **Facilidad de Testing**: Fácil crear mocks o implementaciones de prueba
3. **Flexibilidad de Despliegue**: Cambiar de base de datos sin recompilar
4. **Mantenibilidad**: Código más limpio y organizado
5. **Escalabilidad**: Fácil agregar nuevas implementaciones

## Ejemplo de Uso en Dependencias

```python
# app/infrastructure/db/mongo/dependencies.py
from app.infrastructure.factories.repository_factory import RepositoryFactory

def get_user_repository() -> UserRepositoryInterface:
    """Get user repository instance using factory pattern"""
    return RepositoryFactory.create_user_repository()
```

## Migración de Base de Datos

Para cambiar de MongoDB a PostgreSQL:

1. Configurar la variable de entorno:
```bash
export DATABASE_TYPE=postgresql
export POSTGRESQL_URL=postgresql://user:password@localhost:5432/database
```

2. Asegurarse de que el repositorio PostgreSQL esté implementado y registrado
3. Reiniciar la aplicación

¡Eso es todo! El resto del código no necesita cambios.

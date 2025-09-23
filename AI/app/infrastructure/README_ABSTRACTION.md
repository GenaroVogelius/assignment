# Database Abstraction Layer

Este documento explica cómo funciona la nueva capa de abstracción de base de datos que hace que la aplicación sea agnóstica a la implementación específica de base de datos.

## Estructura de Archivos

```
app/infrastructure/
├── dependencies.py              # Dependencias abstractas (NUEVO)
├── database/
│   └── __init__.py             # Inicialización abstracta de BD (NUEVO)
├── db/
│   └── mongo/
│       ├── dependencies.py     # Dependencias específicas de MongoDB (LEGACY)
│       └── database.py         # Implementación específica de MongoDB
└── factories/
    └── repository_factory.py   # Factory para crear repositorios
```

## Cambios Realizados

### 1. Dependencias Abstractas (`dependencies.py`)

**Antes:**
```python
# En auth_routes.py
from app.infrastructure.db.mongo.dependencies import get_authenticator, get_user_repository
```

**Después:**
```python
# En auth_routes.py
from app.infrastructure.dependencies import get_authenticator, get_user_repository
```

### 2. Inicialización de Base de Datos (`database/__init__.py`)

**Antes:**
```python
# En main.py
from app.infrastructure.db.mongo.database import connect_to_mongo, close_mongo_connection

@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()  # Hardcoded para MongoDB

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()  # Hardcoded para MongoDB
```

**Después:**
```python
# En main.py
from app.infrastructure.database import initialize_database, close_database_connection

@app.on_event("startup")
async def startup_event():
    await initialize_database()  # Agnóstico a la BD

@app.on_event("shutdown")
async def shutdown_event():
    await close_database_connection()  # Agnóstico a la BD
```

## Cómo Funciona la Abstracción

### 1. Factory Pattern

El `RepositoryFactory` determina qué implementación de repositorio usar basándose en la configuración:

```python
# En settings.py
DATABASE_TYPE = "mongodb"  # o "postgresql"

# El factory automáticamente selecciona la implementación correcta
repository = RepositoryFactory.create_user_repository()
```

### 2. Inyección de Dependencias

Las funciones de dependencia son ahora agnósticas:

```python
def get_user_repository() -> UserRepositoryInterface:
    """Agnóstico a la implementación específica"""
    return RepositoryFactory.create_user_repository()

def get_authenticator() -> AuthenticatorInterface:
    """Usa el repositorio configurado automáticamente"""
    user_repository = get_user_repository()
    return AuthenticatorJWT(user_repository=user_repository)
```

### 3. Inicialización de Base de Datos

La inicialización se basa en la configuración:

```python
async def initialize_database():
    db_type = DatabaseType(settings.DATABASE_TYPE.lower())
    
    if db_type == DatabaseType.MONGODB:
        from app.infrastructure.db.mongo.database import connect_to_mongo
        await connect_to_mongo()
    elif db_type == DatabaseType.POSTGRESQL:
        # Implementación futura de PostgreSQL
        pass
```

## Beneficios

### 1. **Agnóstico a la Base de Datos**
- Fácil cambio entre MongoDB, PostgreSQL, etc.
- Solo cambiar `DATABASE_TYPE` en la configuración

### 2. **Separación de Responsabilidades**
- Lógica de negocio separada del acceso a datos
- Interfaces claras entre capas

### 3. **Fácil Testing**
- Mock de dependencias sin acoplamiento
- Testing independiente de la implementación de BD

### 4. **Mantenibilidad**
- Código más limpio y organizado
- Cambios localizados en implementaciones específicas

## Cómo Cambiar de Base de Datos

### Para cambiar de MongoDB a PostgreSQL:

1. **Crear implementación de PostgreSQL:**
   ```python
   # app/infrastructure/repositories/postgres_user_repository.py
   class PostgresUserRepository(UserRepositoryInterface):
       # Implementar métodos de la interfaz
   ```

2. **Registrar en el Factory:**
   ```python
   # En repository_factory.py
   RepositoryFactory.register_repository(
       DatabaseType.POSTGRESQL, 
       PostgresUserRepository
   )
   ```

3. **Actualizar configuración:**
   ```python
   # En settings.py o .env
   DATABASE_TYPE = "postgresql"
   POSTGRESQL_URL = "postgresql://user:pass@localhost/db"
   ```

4. **Implementar inicialización:**
   ```python
   # En database/__init__.py
   elif db_type == DatabaseType.POSTGRESQL:
       from app.infrastructure.db.postgres.database import connect_to_postgres
       await connect_to_postgres()
   ```

**¡Eso es todo!** El resto del código no necesita cambios.

## Archivos Modificados

- ✅ `app/infrastructure/dependencies.py` (NUEVO)
- ✅ `app/infrastructure/database/__init__.py` (NUEVO)
- ✅ `app/infrastructure/api/auth_routes.py` (ACTUALIZADO)
- ✅ `app/main.py` (ACTUALIZADO)

## Archivos Legacy (Mantener para Compatibilidad)

- `app/infrastructure/db/mongo/dependencies.py` (LEGACY - puede eliminarse)
- `app/infrastructure/db/mongo/database.py` (Mantener - implementación específica)

La aplicación ahora es completamente agnóstica a la base de datos y puede cambiar fácilmente entre diferentes implementaciones sin modificar el código de negocio.

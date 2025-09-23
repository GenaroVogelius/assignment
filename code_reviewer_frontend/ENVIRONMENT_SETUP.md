# Configuración de Variables de Entorno

Este proyecto utiliza variables de entorno para configurar la URL de la API y otros parámetros según el entorno de ejecución.

## Configuración

### 1. Archivos de Entorno

- `env.example` - Archivo de ejemplo con todas las variables disponibles
- `.env.local` - Variables para desarrollo local (no se incluye en git)
- `.env.production` - Variables para producción (no se incluye en git)

### 2. Variables Disponibles

| Variable            | Descripción              | Valor por Defecto       |
| ------------------- | ------------------------ | ----------------------- |
| `VITE_API_BASE_URL` | URL base de la API       | `http://127.0.0.1:8000` |
| `VITE_APP_VERSION`  | Versión de la aplicación | `1.0.0`                 |

### 3. Configuración por Entorno

#### Desarrollo Local

```bash
# Crear archivo .env.local
cp env.example .env.local

# Editar .env.local
VITE_API_BASE_URL=http://127.0.0.1:8000
VITE_APP_VERSION=1.0.0
```

#### Producción

```bash
# Crear archivo .env.production
cp env.example .env.production

# Editar .env.production
VITE_API_BASE_URL=https://your-api-domain.com
VITE_APP_VERSION=1.0.0
```

#### Staging

```bash
# Crear archivo .env.staging
cp env.example .env.staging

# Editar .env.staging
VITE_API_BASE_URL=https://staging-api.your-domain.com
VITE_APP_VERSION=1.0.0
```

### 4. Uso en el Código

Las variables se acceden a través del archivo de configuración:

```typescript
import { config, getApiUrl } from "@/config/env";

// Usar la URL base
console.log(config.API_BASE_URL);

// Construir URL completa
const apiUrl = getApiUrl("/api/reviews");
```

### 5. Comandos de Build

```bash
# Desarrollo
npm run dev

# Build para producción
npm run build

# Build para staging
npm run build --mode staging
```

### 6. Notas Importantes

- Las variables de entorno en Vite deben comenzar con `VITE_` para ser accesibles en el cliente
- Los archivos `.env.local`, `.env.production`, etc. no se incluyen en el control de versiones
- Siempre usa `env.example` como referencia para las variables disponibles
- La función `getApiUrl()` maneja automáticamente las barras diagonales en las URLs

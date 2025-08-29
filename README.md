# Books API - Python FastAPI + PostgreSQL

Una API RESTful moderna y escalable para gestión de libros, desarrollada con FastAPI, PostgreSQL y diseñada para ejecutarse como Web Service en Render.

## 🚀 Características

- ✅ **CRUD completo** para libros
- ✅ **Paginación** inteligente
- ✅ **Búsqueda textual** en título, autor y descripción
- ✅ **Filtrado avanzado** por autor y rango de precios
- ✅ **Soft delete** (eliminación lógica)
- ✅ **Respuestas estandarizadas** en JSON
- ✅ **Documentación automática** con Swagger UI
- ✅ **Asíncrono** para alto rendimiento
- ✅ **Validación robusta** con Pydantic
- ✅ **Compatible con Docker** y Render

## 🛠 Stack Tecnológico

- **Framework**: FastAPI
- **Base de datos**: PostgreSQL
- **ORM**: SQLAlchemy 2.0 (async)
- **Validación**: Pydantic
- **Servidor**: Uvicorn
- **Contenedores**: Docker + Docker Compose

## 📦 Instalación

### 1. Clonar el repositorio
```bash
git clone <repository-url>
cd books-api
```

### 2. Crear archivo de entorno
```bash
cp .env.example .env
# Editar .env con tus credenciales de base de datos
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL local
```sql
-- Conectar a PostgreSQL y ejecutar:
CREATE DATABASE library;
```

## 🚀 Ejecución

### Opción 1: Ejecución Local (Desarrollo)
```bash
# Ejecutar las migraciones
python scripts/seed_data.py

# Iniciar el servidor
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Opción 2: Docker Compose (Recomendado)
```bash
# Iniciar API + PostgreSQL en contenedores
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

### Opción 3: Solo Docker
```bash
# Construir imagen
docker build -t books-api .

# Ejecutar contenedor
docker run -d -p 8000:8000 \
  -e DB_HOST=tu_host \
  -e DB_PASSWORD=tu_password \
  books-api
```

## 🌐 Acceso a la API

- **API**: http://localhost:8000
- **Documentación**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

## 📚 Endpoints

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/health` | Estado de la API |
| `GET` | `/api/v1/books/` | Listar libros con filtros |
| `GET` | `/api/v1/books/{id}` | Obtener libro por ID |
| `POST` | `/api/v1/books/` | Crear nuevo libro |
| `PUT` | `/api/v1/books/{id}` | Actualizar libro |
| `DELETE` | `/api/v1/books/{id}` | Eliminar libro (soft delete) |

## 📝 Ejemplos de uso

### 1. Listar libros con paginación
```bash
curl -X GET "http://localhost:8000/api/v1/books/?page=1&limit=5"
```

### 2. Buscar libros
```bash
curl -X GET "http://localhost:8000/api/v1/books/?q=cortázar&limit=10"
```

### 3. Filtrar por autor y precio
```bash
curl -X GET "http://localhost:8000/api/v1/books/?author=borges&min_price=15&max_price=25"
```

### 4. Crear libro
```bash
curl -X POST "http://localhost:8000/api/v1/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rayuela",
    "author": "Julio Cortázar",
    "price": 22.50,
    "description": "Una novela experimental única."
  }'
```

### 5. Actualizar libro
```bash
curl -X PUT "http://localhost:8000/api/v1/books/{book_id}" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 25.00,
    "description": "Descripción actualizada"
  }'
```

### 6. Eliminar libro
```bash
curl -X DELETE "http://localhost:8000/api/v1/books/{book_id}"
```

## 🔧 Variables de Entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DB_HOST` | Host de PostgreSQL | `localhost` |
| `DB_PORT` | Puerto de PostgreSQL | `5432` |
| `DB_NAME` | Nombre de la base de datos | `library` |
| `DB_USER` | Usuario de PostgreSQL | `postgres` |
| `DB_PASSWORD` | Contraseña de PostgreSQL | `1` |
| `DB_SSLMODE` | Modo SSL de PostgreSQL | `disable` |
| `APP_ENV` | Entorno de la aplicación | `development` |
| `APP_DEBUG` | Modo debug | `true` |
| `PORT` | Puerto de la aplicación | `8000` |

## 🌍 Despliegue en Render

### Con PostgreSQL en Neon.tech (Recomendado)

1. **Crear base de datos en [Neon.tech](https://neon.tech)**
2. **Configurar variables de entorno en Render**:
   ```
   DB_HOST=tu-host.neon.tech
   DB_PORT=5432
   DB_NAME=tu-database
   DB_USER=tu-usuario
   DB_PASSWORD=tu-password
   DB_SSLMODE=require
   APP_ENV=production
   PORT=10000
   ```

3. **Desplegar en Render**:
   - Conectar tu repositorio de GitHub
   - Seleccionar "Web Service"
   - Runtime: Docker
   - Build Command: `docker build -t books-api .`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Con render.yaml (Automático)
```bash
# Render detectará automáticamente el render.yaml y desplegará
git push origin main
```

## 🧪 Pruebas de las 3 Configuraciones

### 1. PostgreSQL Local
```bash
# .env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=library
DB_USER=postgres
DB_PASSWORD=1
DB_SSLMODE=disable

# Ejecutar
uvicorn main:app --reload
```

### 2. PostgreSQL en Neon.tech
```bash
# .env
DB_HOST=ep-xxx-xxx.us-east-1.aws.neon.tech
DB_PORT=5432
DB_NAME=neondb
DB_USER=tu-usuario
DB_PASSWORD=tu-password
DB_SSLMODE=require

# Ejecutar
uvicorn main:app --reload
```

### 3. Docker + Render
```bash
# Usar docker-compose.yml para prueba local
docker-compose up -d

# Para Render, usar render.yaml con variables de entorno
```

## 📊 Estructura del Proyecto

```
/
├── api/                      # Endpoints
│   ├── health.py            # Health check
│   └── books.py             # Books CRUD
├── controllers/             # Lógica de negocio
│   └── book_controller.py   # Controlador de libros
├── models/                  # Modelos SQLAlchemy
│   └── book_model.py        # Modelo Book
├── schemas/                 # Esquemas Pydantic
│   └── book_schema.py       # Validaciones y respuestas
├── config/                  # Configuración
│   ├── database.py          # Conexión asíncrona PostgreSQL
│   └── settings.py          # Variables de entorno
├── scripts/                 # Scripts auxiliares
│   ├── create_tables.sql    # DDL de tablas
│   └── seed_data.py         # Datos de prueba
├── .env.example             # Variables de entorno ejemplo
├── .gitignore               # Archivos ignorados
├── Dockerfile               # Imagen Docker
├── docker-compose.yml       # Orquestación local
├── render.yaml              # Despliegue Render
├── requirements.txt         # Dependencias Python
└── main.py                  # Punto de entrada
```

## 🔍 Respuestas de la API

### Éxito
```json
{
  "success": true,
  "data": [...],
  "pagination": {
    "page": 1,
    "limit": 10,
    "total": 150,
    "total_pages": 15
  }
}
```

### Error
```json
{
  "success": false,
  "error": "Book not found",
  "code": 404
}
```

## 🛡 Seguridad y Buenas Prácticas

- ✅ **Validación de entrada** con Pydantic
- ✅ **Manejo de errores** robusto
- ✅ **Conexiones async** para mejor rendimiento
- ✅ **Pool de conexiones** con reciclaje automático
- ✅ **Soft delete** para preservar datos
- ✅ **Índices de base de datos** para consultas rápidas
- ✅ **Usuario no-root** en Docker
- ✅ **Variables de entorno** para configuración
- ✅ **Health checks** para monitoreo

## 🐛 Solución de Problemas

### Error de conexión a base de datos
```bash
# Verificar que PostgreSQL esté ejecutándose
pg_isready -h localhost -p 5432

# Verificar credenciales en .env
cat .env
```

### Error en Docker
```bash
# Ver logs del contenedor
docker logs books_api

# Verificar estado de servicios
docker-compose ps
```

### Error en Render
- Verificar variables de entorno en el dashboard
- Revisar los logs de despliegue
- Asegurar que `PORT` esté configurado como `10000`

## 📈 Rendimiento

- **Async/Await**: Manejo de múltiples peticiones concurrentes
- **Connection Pooling**: Reutilización eficiente de conexiones
- **Índices de base de datos**: Consultas optimizadas
- **Paginación**: Evita cargar grandes datasets en memoria

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit los cambios (`git commit -m 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.
# Manual Técnico: Administrador de Proyecto (Dueño)

Este manual está dirigido al Product Owner / Technical Lead y describe la arquitectura general, el despliegue y la administración técnica del Bot de Telegram.

## 1. Arquitectura General
El proyecto sigue una estructura limpia, separando las responsabilidades de la siguiente manera:
- `bot/`: Contiene la capa de presentación hacia Telegram (Handlers de aiogram 3, teclados y middlewares).
- `core/`: Configuraciones centrales, variables de entorno (`settings.py`) y seguridad.
- `db/`: Configuración de la base de datos PostgreSQL, modelos de SQLAlchemy y motor de conexión.
- `services/`: La capa de lógica de negocio (por ejemplo, `bracket_service.py` para la generación de llaves).
- `api/`: Opcional para exponer endpoints (FastAPI), utilizado principalmente para Healthchecks en Railway.
- `docs/`: Manuales operativos y documentación del proyecto.

## 2. Base de Datos y Migraciones (Alembic)
El proyecto utiliza SQLAlchemy como ORM y Alembic para el control de versiones (migraciones) de la base de datos PostgreSQL.
- **Generar una Migración:** Cuando se realiza un cambio en los modelos en `db/models.py`, se debe generar una migración:
  ```bash
  alembic revision --autogenerate -m "Descripción del cambio"
  ```
- **Aplicar Migraciones:** Para impactar la base de datos con los cambios:
  ```bash
  alembic upgrade head
  ```
- **Resolución de Bloqueos (Locks):** Si las migraciones fallan por `AccessExclusiveLock`, utiliza el script `python fix_db.py` para matar conexiones colgadas en PostgreSQL.

## 3. Despliegue en Railway
El bot está diseñado para ser hospedado en contenedores a través de Railway.
- **Dockerfile:** Orquesta la construcción de la imagen. Instala las dependencias y corre `main.py`.
- **Healthcheck (FastAPI):** Railway requiere que un puerto se exponga para validar que la app está viva. `main.py` lanza Uvicorn para responder en el `$PORT` asignado por Railway, mientras en segundo plano el bot de aiogram escucha a Telegram.
- **railway.toml:** Configura los parámetros de despliegue, asignando un Start Command o delegando la ejecución directamente al Dockerfile.

## 4. Variables de Entorno (.env)
Asegúrese de tener configuradas las siguientes variables clave en el entorno de producción (Railway Variables):
- `BOT_TOKEN`: El token proporcionado por BotFather.
- `DATABASE_URL`: URI de conexión a PostgreSQL (formato `postgresql+asyncpg://...`).
- `PORT`: Asignado automáticamente por Railway.
- `ENVIRONMENT`: Puede ser `development` o `production`.

## 5. Prevención de Errores Críticos (Blindaje)
- La ejecución del bot en `main.py` está rodeada por bloques `try/except` que atrapan problemas de red o tokens inválidos para evitar que Uvicorn se caiga e impida el Healthcheck de Railway.
